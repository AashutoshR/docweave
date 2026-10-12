"""Detect documentation that no longer matches the code.

Five independent detectors, from most to least certain:

1. **Claim checking** - parameters, return values and exceptions a docstring documents are
   compared with what static analysis finds in the signature and body.
2. **Reference rot** - identifiers and paths mentioned in hand-written Markdown are resolved
   against the code; ones that used to exist are traced to the commit that removed them.
3. **Blame staleness** - a docstring is suspect when the code it describes was rewritten by later
   commits. Commit intent weights the evidence: a ``fix`` or ``feat`` counts, a reformat does not.
4. **Prose staleness** - the same test applied to Markdown lines that mention a symbol.
5. **Anchored signatures** - without git, a state file remembers the signature each docstring
   was written against.
"""

from __future__ import annotations

import difflib
import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from .analyzers import ANALYZERS, discover
from .config import Config
from .gitrepo import UNCOMMITTED, Removal
from .linker import BlameInfo
from .model import Issue, Message, Project, Symbol
from .nlp.docstring import parse_docstring
from .nlp.intent import DOC_IMPACT

SEVERITIES = ("high", "medium", "low")
_SEVERITY_WEIGHT = {"high": 1.0, "medium": 0.5, "low": 0.15}
_FENCE = re.compile(r"^\s*(```|~~~)")
_SPAN = re.compile(r"`([^`\n]+)`")
_IDENT = re.compile(r"^[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*(?:\(\))?$")
_PATH = re.compile(r"^[\w.-]+(?:/[\w.-]+)*/?(?::\d+)?$")
_REGION = re.compile(r"<!-- docweave:(begin|end) \S+ -->\s*$")
_DOC_EXTS = (".md", ".rst", ".txt", ".toml", ".json", ".yml", ".yaml", ".cfg", ".ini", ".sh")
_GENERIC_ERRORS = {"Exception", "BaseException", "Error"}
_HISTORY_FILES =re.compile(r"^(changelog|history|changes|news|release[-_ ]?notes)", re.I)

ISSUE_HELP = {
    "param-not-in-signature": "The docstring documents a parameter the function no longer accepts.",
    "param-undocumented": "The docstring lists parameters but leaves some out.",
    "returns-mismatch": "The docstring describes a return value the function never produces.",
    "raises-mismatch": "The docstring promises an exception the body no longer raises.",
    "dangling-reference": "Hand-written docs mention code that no longer exists.",
    "missing-path": "Hand-written docs point at a file that is not there.",
    "stale-docstring": "The code changed in later commits but its docstring did not.",
    "stale-prose": "Hand-written docs describe code that has substantially changed since they were written.",
    "signature-drift": "The signature changed since the docstring was last edited.",
    "undocumented-hotspot": "Complex public code with no documentation at all.",
    "parse-error": "The file could not be analysed.",
}


@dataclass
class Reference:
    """A mention of code found in hand-written Markdown."""

    file: str
    line: int
    text: str
    targets: list[str] = field(default_factory=list)  # resolved symbol ids


@dataclass
class Health:
    """Documentation quality in numbers."""

    score: int
    public: int
    documented: int
    counts: dict[str, int]

    @property
    def coverage(self) -> float:
        """Share of public symbols that have documentation."""
        return self.documented / self.public if self.public else 1.0


def _names(items) -> str:
    return ", ".join(f"`{i}`" for i in sorted(items))


def check_claims(sym: Symbol) -> list[Issue]:
    """Compare what a docstring claims about a function with what the code does."""
    if not sym.docstring or sym.kind == "constant":
        return []
    info = parse_docstring(sym.docstring)
    line = sym.doc_range[0] if sym.doc_range else sym.lineno
    issues: list[Issue] = []
    checkable = sym.kind != "class" or bool(sym.params)
    open_ended = any(p.kind == "kwarg" for p in sym.params)
    actual = {p.name for p in sym.params}
    documented = set(info.params)
    if checkable and documented:
        ghosts = set() if open_ended else documented - actual
        missing = {p.name for p in sym.params if p.kind in ("positional", "keyword") and not p.name.startswith("_")} - documented
        if ghosts:
            detail = []
            candidates = sorted(actual - documented)  # includes *args / **kwargs names
            for ghost in sorted(ghosts):
                guess = difflib.get_close_matches(ghost, candidates, n=1, cutoff=0.5)
                if guess or len(candidates) == len(ghosts) == 1:
                    detail.append(f"`{ghost}` was probably renamed to `{guess[0] if guess else candidates[0]}`")
            issues.append(Issue("param-not-in-signature", "high", sym.file, line,
                                f"`{sym.qualname}` documents {_names(ghosts)}, which is not in its signature", sym.id, detail))
        if missing:
            issues.append(Issue("param-undocumented", "medium", sym.file, line,
                                f"`{sym.qualname}` does not document parameter(s) {_names(missing)}", sym.id))
    if sym.kind in ("function", "method") and not sym.is_stub:
        if info.returns and not sym.returns_value and sym.returns in (None, "None", "void"):
            issues.append(Issue("returns-mismatch", "medium", sym.file, line,
                                f"`{sym.qualname}` documents a return value but never returns one", sym.id))
        # A documented exception counts as raised if a raised name contains it (import aliases such
        # as ``JSONDecodeError as RequestsJSONDecodeError``); catch-all names promise nothing checkable.
        gone = {r for r in info.raises if r not in _GENERIC_ERRORS and not any(r in a or a in r for a in sym.raises)}
        if gone and sym.raises:
            issues.append(Issue("raises-mismatch", "low", sym.file, line,
                                f"`{sym.qualname}` documents raising {_names(gone)}, but only raises {_names(sym.raises)}", sym.id))
    return issues


def _later_changes(info: BlameInfo, since: float, skip: set[str], messages: dict[str, Message]) -> tuple[float, bool, list[Message]]:
    """Code lines written after ``since``: (impact-weighted share, signature changed?, commits)."""
    total = sum(info.code.values())
    weighted = 0.0
    sig_changed = False
    commits: list[Message] = []
    for sha, n in info.code.items():
        msg = messages.get(f"commit:{sha}")
        if msg is None or sha in skip or msg.timestamp <= since:
            continue
        impact = DOC_IMPACT.get(msg.intent, 0.7)
        weighted += n * impact
        if impact >= 0.5:
            commits.append(msg)
            sig_changed = sig_changed or sha in info.sig
    commits.sort(key=lambda m: -m.timestamp)
    return (weighted / total if total else 0.0), sig_changed, commits


def _evidence(commits: list[Message]) -> list[str]:
    return [f"{m.day} {m.label} ({m.intent}, {m.author}): {m.title}" for m in commits[:4]]


def check_staleness(sym: Symbol, info: BlameInfo | None, messages: dict[str, Message]) -> Issue | None:
    """Flag a docstring whose code was rewritten by meaningful commits after it was last edited."""
    if info is None or not info.doc or not sym.doc_range or sym.kind == "constant":
        return None
    doc_times = [messages[f"commit:{sha}"].timestamp for sha in info.doc if f"commit:{sha}" in messages]
    if not doc_times:
        return None
    share, sig_changed, commits = _later_changes(info, max(doc_times), set(info.doc), messages)
    if not commits:
        return None
    if sig_changed and share >= 0.5:
        severity = "high"
    elif sig_changed or share >= 0.5:
        severity = "medium"
    elif share >= 0.25:
        severity = "low"
    else:
        return None
    what = "its signature and " if sig_changed else ""
    return Issue("stale-docstring", severity, sym.file, sym.doc_range[0],
                 f"`{sym.qualname}`: {what}{share:.0%} of its code changed after the docstring was last edited",
                 sym.id, _evidence(commits))


def name_index(project: Project) -> dict[str, list[str]]:
    """Every way prose might spell a symbol: bare name, qualified name, fully dotted path."""
    index: dict[str, list[str]] = {}
    for sym in project.symbols.values():
        if sym.name != "__init__":
            for key in {sym.name, sym.qualname, f"{sym.module}.{sym.qualname}"}:
                index.setdefault(key, []).append(sym.id)
    return index


def resolve_name(name: str, index: dict[str, list[str]], module_names: set[str]) -> list[str]:
    """Resolve a dotted name from prose to symbol ids, tolerating a partial module prefix."""
    if name in index:
        return index[name]
    parts = name.split(".")
    if len(parts) > 1 and parts[0] in module_names | {m.split(".")[0] for m in module_names}:
        for i in range(1, len(parts)):
            if hit := index.get(".".join(parts[i:])):
                return hit
    return []


def scan_markdown(cfg: Config, project: Project) -> tuple[list[Reference], list[tuple[str, int, str]]]:
    """Find code references in hand-written Markdown.

    Returns resolved/unresolved identifier references, plus ``(file, line, path)`` for path-like
    spans. Generated output, changelogs and DocWeave-managed regions are skipped.
    """
    index = name_index(project)
    module_names = set(project.modules) | {m.rpartition(".")[2] for m in project.modules}
    references: list[Reference] = []
    paths: list[tuple[str, int, str]] = []
    for rel in discover(cfg, (".md",), sources=["."]):
        if rel.startswith((cfg.out_dir + "/", cfg.comms_dir + "/")) or _HISTORY_FILES.match(rel.rsplit("/", 1)[-1]):
            continue
        fenced = managed = False
        for lineno, line in enumerate((cfg.root / rel).read_text(encoding="utf-8", errors="replace").split("\n"), 1):
            if m := _REGION.match(line):
                managed = m[1] == "begin"
            if _FENCE.match(line):
                fenced = not fenced
            if fenced or managed:
                continue
            for span in _SPAN.findall(line):
                span = span.strip()
                if span.startswith("./"):
                    span = span[2:]
                target = span.split(":")[0]
                is_path = bool(_PATH.match(span)) and ("/" in target or target.lower().endswith(tuple(ANALYZERS) + _DOC_EXTS))
                if is_path and not span.startswith("."):
                    paths.append((rel, lineno, target))
                elif _IDENT.match(span):
                    name = span.removesuffix("()")
                    if name not in module_names:
                        references.append(Reference(rel, lineno, name, resolve_name(name, index, module_names)))
    return references, paths


def check_references(
    cfg: Config, project: Project, references: list[Reference], paths: list[tuple[str, int, str]],
    graveyard: dict[str, Removal], deleted: dict[str, str], messages: dict[str, Message],
    blame: dict[str, list[str]], blame_info: dict[str, BlameInfo],
) -> list[Issue]:
    """Turn Markdown references into issues: dangling names, missing paths and stale prose."""
    issues: list[Issue] = []
    current = sorted({s.name for s in project.symbols.values()})
    roots = {m.split(".")[0] for m in project.modules}
    index = name_index(project)
    basenames = {f.rsplit("/", 1)[-1] for f in discover(cfg, ("",), sources=["."])}
    seen: set[tuple[str, str]] = set()

    def describe(sha: str) -> str:
        msg = messages.get(f"commit:{sha}")
        return f"{msg.label} on {msg.day} by {msg.author}: \"{msg.title}\"" if msg else sha[:7]

    for ref in references:
        last = ref.text.rpartition(".")[2]
        if not ref.targets:
            gone = graveyard.get(ref.text) or graveyard.get(last)
            if gone and (ref.file, ref.text) not in seen:
                seen.add((ref.file, ref.text))
                options = [r for r in gone.replacements if r in current] or difflib.get_close_matches(last, current, n=1, cutoff=0.6)
                detail = [f"removed in {describe(gone.sha)}"]
                if options:
                    detail.append(f"did you mean `{options[0]}`?")
                issues.append(Issue("dangling-reference", "high", ref.file, ref.line,
                                    f"`{ref.text}` is mentioned here but no longer exists in the code", None, detail))
            elif "." in ref.text and ref.text.split(".")[0] in roots and (ref.file, ref.text) not in seen:
                parts = ref.text.split(".")
                if any(".".join(parts[:k]) in index for k in range(1, len(parts))):
                    continue  # an attribute of a known class or constant, which is not tracked
                seen.add((ref.file, ref.text))
                guess = difflib.get_close_matches(last, current, n=1, cutoff=0.6)
                issues.append(Issue("dangling-reference", "medium", ref.file, ref.line,
                                    f"`{ref.text}` looks like project code but does not resolve to anything", None,
                                    [f"did you mean `{guess[0]}`?"] if guess else []))
            continue
        # Resolved: was the prose written before the symbol materially changed?
        lines = blame.get(ref.file)
        if not lines or ref.line > len(lines) or len(ref.targets) != 1 or (ref.file, ref.targets[0]) in seen:
            continue
        written = messages.get(f"commit:{lines[ref.line - 1]}")
        info = blame_info.get(ref.targets[0])
        if written is None or info is None or lines[ref.line - 1] == UNCOMMITTED:
            continue
        share, sig_changed, commits = _later_changes(info, written.timestamp, set(), messages)
        if commits and (sig_changed or share >= 0.5):
            seen.add((ref.file, ref.targets[0]))
            what = "its signature changed" if sig_changed else f"{share:.0%} of it was rewritten"
            issues.append(Issue("stale-prose", "medium" if sig_changed and share >= 0.3 else "low", ref.file, ref.line,
                                f"this text mentions `{ref.text}`, but {what} since the line was written ({written.day})",
                                ref.targets[0], _evidence(commits)))

    for file, line, path in paths:
        here = file.rpartition("/")[0]
        candidates = {path.rstrip("/"), f"{here}/{path}".strip("/").rstrip("/")}
        if path.startswith(cfg.out_dir + "/"):
            continue  # generated output comes and goes with the project's features
        if any((cfg.root / c).exists() for c in candidates) or path.rsplit("/", 1)[-1] in basenames or (file, path) in seen:
            continue
        seen.add((file, path))
        sha = next((deleted[c] for c in candidates if c in deleted), None)
        if sha:
            issues.append(Issue("missing-path", "medium", file, line, f"`{path}` is referenced here but was deleted", None,
                                [f"deleted in {describe(sha)}"]))
        elif path.lower().endswith(tuple(ANALYZERS)) or ("/" in path and (cfg.root / path.split("/")[0]).is_dir()):
            issues.append(Issue("missing-path", "low", file, line, f"`{path}` is referenced here but does not exist"))
    return issues


# --- anchored signatures (works without git) ---------------------------------------------------

def _doc_hash(sym: Symbol) -> str:
    return hashlib.sha1((sym.docstring or "").encode("utf-8")).hexdigest()[:12]


def load_state(cfg: Config) -> dict:
    """Read the signature anchors saved by the last ``generate`` (empty if there are none)."""
    path = cfg.state_dir / "state.json"
    try:
        return json.loads(path.read_text(encoding="utf-8")).get("symbols", {})
    except (OSError, ValueError):
        return {}


def next_state(project: Project, previous: dict) -> dict:
    """Remember, per symbol, the signature its current docstring was written against."""
    state: dict = {}
    for sym in project.symbols.values():
        doc = _doc_hash(sym)
        prev = previous.get(sym.id)
        anchor = prev["anchor"] if prev and prev.get("doc") == doc else sym.interface_hash
        state[sym.id] = {"doc": doc, "anchor": anchor}
    return state


def save_state(cfg: Config, state: dict) -> None:
    """Persist signature anchors so the next run can compare against them."""
    cfg.state_dir.mkdir(exist_ok=True)
    payload = json.dumps({"version": 1, "symbols": dict(sorted(state.items()))}, indent=1)
    (cfg.state_dir / "state.json").write_text(payload + "\n", encoding="utf-8", newline="\n")


def check_anchors(project: Project, state: dict) -> list[Issue]:
    """Flag documented symbols whose signature differs from the one their docstring was written for."""
    issues = []
    for sym in project.symbols.values():
        entry = state.get(sym.id)
        if entry and sym.docstring and sym.kind != "constant" and entry["anchor"] != sym.interface_hash:
            issues.append(Issue("signature-drift", "medium", sym.file, sym.lineno,
                                f"`{sym.qualname}`: signature changed since its docstring was last edited", sym.id))
    return issues


# --- putting it together -----------------------------------------------------------------------

def is_documented(sym: Symbol) -> bool:
    """True if the symbol has a non-empty docstring."""
    return bool(sym.docstring and sym.docstring.strip())


def detect(
    cfg: Config, project: Project, messages: dict[str, Message], blame: dict[str, list[str]],
    blame_info: dict[str, BlameInfo], graveyard: dict[str, Removal], deleted: dict[str, str], state: dict,
) -> tuple[list[Issue], list[Reference]]:
    """Run every detector and return de-duplicated issues, most severe first."""
    issues: list[Issue] = []
    for module in project.modules.values():
        if module.error:
            issues.append(Issue("parse-error", "medium", module.file, 1, f"could not analyse: {module.error}"))
    stale: set[str] = set()
    for sym in project.symbols.values():
        if not sym.is_public and not cfg.include_private:
            continue
        issues += check_claims(sym)
        if issue := check_staleness(sym, blame_info.get(sym.id), messages):
            issues.append(issue)
            stale.add(sym.id)
        if not is_documented(sym) and sym.kind != "constant" and sym.complexity >= 10:
            issues.append(Issue("undocumented-hotspot", "low", sym.file, sym.lineno,
                                f"`{sym.qualname}` is public, complex (cyclomatic complexity {sym.complexity}) and undocumented", sym.id))
    issues += [i for i in check_anchors(project, state) if i.symbol not in stale
               and (cfg.include_private or project.symbols[i.symbol].is_public)]
    references, paths = scan_markdown(cfg, project)
    issues += check_references(cfg, project, references, paths, graveyard, deleted, messages, blame, blame_info)
    return sorted(issues, key=Issue.sort_key), references


def health(cfg: Config, project: Project, issues: list[Issue]) -> Health:
    """Summarise documentation quality as a 0-100 score: 40% coverage, 60% freshness.

    Coverage counts classes, functions and methods; constants are documented when they have a
    comment but are not held against the score when they do not.
    """
    public = [s for s in project.symbols.values() if (s.is_public or cfg.include_private) and s.kind != "constant"]
    documented = sum(1 for s in public if is_documented(s))
    counts = {sev: sum(1 for i in issues if i.severity == sev) for sev in SEVERITIES}
    penalty = sum(_SEVERITY_WEIGHT[i.severity] for i in issues if i.kind != "undocumented-hotspot")
    freshness = max(0.0, 1.0 - penalty / max(8.0, len(public) * 0.5))
    coverage = documented / len(public) if public else 1.0
    return Health(round(100 * (0.4 * coverage + 0.6 * freshness)), len(public), documented, counts)
