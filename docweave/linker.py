"""Link developer communication to the code it is about.

Three independent kinds of evidence are combined (noisy-OR) into one confidence per
``(message, symbol)`` pair:

* **blame** - the commit is the last writer of lines that still exist in the symbol;
* **mention** - the message names the symbol (``in backticks``, as a call, or as a distinctive
  identifier in running text);
* **similarity** - TF-IDF cosine between the message and the symbol's name and docstring.

Pull requests and issues additionally inherit the links of commits that reference them (``#12``).
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field

from .gitrepo import UNCOMMITTED
from .model import Link, Message, Project, Symbol
from .nlp.index import TextIndex
from .nlp.text import split_identifier, tokenize

_TICKED = re.compile(r"`([^`\n]+)`")
_TOKEN = re.compile(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*")
_REF = re.compile(r"#(\d+)\b")
MIN_CONFIDENCE = 0.3


@dataclass
class BlameInfo:
    """Which commits last wrote each part of a symbol."""

    code: Counter = field(default_factory=Counter)  # sha -> surviving non-docstring lines
    doc: Counter = field(default_factory=Counter)  # sha -> docstring lines
    sig: set[str] = field(default_factory=set)  # shas that last wrote the signature lines


def symbol_blame(project: Project, blame: dict[str, list[str]]) -> dict[str, BlameInfo]:
    """Attribute every line of every symbol to the commit that last wrote it."""
    children: dict[str, list[Symbol]] = defaultdict(list)
    for sym in project.symbols.values():
        if sym.parent:
            children[sym.parent].append(sym)
    out: dict[str, BlameInfo] = {}
    for sym in project.symbols.values():
        shas = blame.get(sym.file)
        if not shas:
            continue
        doc_lines = set(range(sym.doc_range[0], sym.doc_range[1] + 1)) if sym.doc_range else set()
        span = set(range(sym.lineno, sym.end_lineno + 1)) - doc_lines
        for child in children.get(sym.id, []):
            span -= set(range(min(child.lineno, child.doc_range[0] if child.doc_range else child.lineno), child.end_lineno + 1))
        info = BlameInfo()
        for line in span:
            if line <= len(shas):
                info.code[shas[line - 1]] += 1
        for line in doc_lines:
            if line <= len(shas):
                info.doc[shas[line - 1]] += 1
        info.sig = {shas[line - 1] for line in range(sym.lineno, sym.sig_end + 1) if line <= len(shas)}
        out[sym.id] = info
    return out


def is_distinctive(name: str) -> bool:
    """Would this name, seen in running prose, plausibly be a reference to code?"""
    core = name.strip("_")
    return "_" in core or bool(re.search(r"[a-z][A-Z]", core)) or (core[:1].isupper() and len(split_identifier(core)) >= 2)


def _noisy_or(values: list[float]) -> float:
    miss = 1.0
    for v in values:
        miss *= 1.0 - min(max(v, 0.0), 0.99)
    return round(1.0 - miss, 3)


class Linker:
    """Scores every (message, symbol) pair from blame, mentions and wording similarity."""

    def __init__(self, project: Project, messages: dict[str, Message], blame_info: dict[str, BlameInfo]) -> None:
        self.symbols = project.symbols
        self.messages = messages
        self.blame_info = blame_info
        self.names: dict[str, list[str]] = defaultdict(list)
        self.by_file: dict[str, set[str]] = defaultdict(set)
        self.index = TextIndex()
        for sym in self.symbols.values():
            if sym.name != "__init__":
                self.names[sym.name].append(sym.id)
            if sym.qualname != sym.name:
                self.names[sym.qualname].append(sym.id)
            self.names[f"{sym.module}.{sym.qualname}"].append(sym.id)
            self.by_file[sym.file].add(sym.id)
            self.index.add(sym.id, tokenize(sym.qualname) * 3 + tokenize(sym.docstring or "") + tokenize(sym.module))
        self.index.finalize()

    def mentions(self, message: Message) -> dict[str, float]:
        """Symbols a message names explicitly, with the strength of each mention."""
        text = message.text
        ticked = {m.group(0) for span in _TICKED.findall(text) for m in [_TOKEN.match(span.strip())] if m}
        touched = {sid for path, _a, _d in message.files for sid in self.by_file.get(path, ())}
        found: dict[str, float] = {}
        for m in _TOKEN.finditer(text):
            token = m.group(0)
            strong = token in ticked or text[m.end() : m.end() + 1] == "("
            parts = token.split(".")
            for key in dict.fromkeys([token, ".".join(parts[-2:]), parts[-1]]):
                ids = self.names.get(key)
                if not ids or not (strong or is_distinctive(parts[-1])):
                    continue
                narrowed = [i for i in ids if i in touched] or ids
                if len(narrowed) > 4:
                    continue
                weight = (0.9 if strong else 0.75) / len(narrowed)
                for sid in narrowed:
                    found[sid] = max(found.get(sid, 0.0), weight)
                break
        return found

    def run(self) -> dict[str, list[Link]]:
        """Compute links for every symbol, newest message first."""
        evidence: dict[tuple[str, str], list[tuple[float, str]]] = defaultdict(list)
        lines: dict[tuple[str, str], int] = {}

        for sid, info in self.blame_info.items():
            total = sum(info.code.values()) + sum(info.doc.values())
            for sha, n in (info.code + info.doc).items():
                mid = f"commit:{sha}"
                if mid in self.messages and total:
                    evidence[(mid, sid)].append((0.4 + 0.6 * n / total, f"wrote {n} of {total} current lines"))
                    lines[(mid, sid)] = n

        for mid, message in self.messages.items():
            if message.source == "worktree":
                continue
            for sid, weight in self.mentions(message).items():
                evidence[(mid, sid)].append((weight, "mentions it by name"))
            # Wording similarity is noisy, so on its own it must be strong; it mostly serves to
            # reinforce a link that blame or a mention already established.
            tokens = tokenize(message.text)
            if message.source == "commit":
                restrict = {sid for path, _a, _d in message.files for sid in self.by_file.get(path, ())}
                hits = self.index.cosine(tokens, restrict, k=3) if restrict else []
                alone = 0.6
            else:
                hits, alone = self.index.cosine(tokens, k=3), 0.4
            for sid, score in hits:
                if score >= alone or (score >= 0.2 and (mid, sid) in evidence):
                    evidence[(mid, sid)].append((min(0.6, score), f"similar wording ({score:.2f})"))

        # PRs / issues inherit from the commits that reference them.
        per_message: dict[str, list[tuple[str, float]]] = defaultdict(list)
        for (mid, sid), found in evidence.items():
            per_message[mid].append((sid, _noisy_or([v for v, _ in found])))
        for mid, message in self.messages.items():
            if message.source != "commit":
                continue
            for number in set(_REF.findall(message.text)):
                for target in (f"pr:{number}", f"issue:{number}"):
                    if target in self.messages:
                        for sid, strength in per_message.get(mid, []):
                            evidence[(target, sid)].append((0.9 * strength, f"via commit {message.label}"))

        links: dict[str, list[Link]] = defaultdict(list)
        for (mid, sid), found in evidence.items():
            confidence = _noisy_or([v for v, _ in found])
            if confidence >= MIN_CONFIDENCE:
                reasons = list(dict.fromkeys(reason for _, reason in found))
                links[sid].append(Link(mid, confidence, reasons, lines.get((mid, sid), 0)))
        for sid in links:
            links[sid].sort(key=lambda l: (-self.messages[l.message_id].timestamp, l.message_id))
        return dict(links)


def owners(info: BlameInfo | None, messages: dict[str, Message], top: int = 3) -> list[tuple[str, float]]:
    """Authors of the surviving lines of a symbol, as ``(name, share)`` pairs."""
    if info is None:
        return []
    by_author: Counter = Counter()
    for sha, n in (info.code + info.doc).items():
        if sha != UNCOMMITTED and (msg := messages.get(f"commit:{sha}")):
            by_author[msg.author] += n
    total = sum(by_author.values())
    return [(name, n / total) for name, n in by_author.most_common(top)] if total else []
