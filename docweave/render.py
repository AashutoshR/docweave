"""Render an :class:`~docweave.engine.Analysis` as a Markdown documentation site.

Every page is a list of ``(block_id, markdown)`` pairs. Blocks are written inside managed-region
markers (see :mod:`docweave.regions`), which is what lets regeneration update the page in place
while keeping anything a person added around them. Output is deterministic - no timestamps - so
an unchanged project regenerates byte-identical docs and ``git diff`` stays quiet.
"""

from __future__ import annotations

import posixpath
import re
from pathlib import Path

from . import regions
from .changelog import build_changelog, is_docs_only
from .drift import ISSUE_HELP, SEVERITIES, is_documented
from .engine import Analysis
from .graph import cycles, external_dependencies, mermaid
from .linker import owners
from .model import Message, Module, Symbol
from .nlp.describe import describe
from .nlp.docstring import parse_docstring
from .nlp.intent import INTENT_TITLES
from .nlp.rationale import decision_score, rationale
from .nlp.text import first_sentence

Blocks = list[tuple[str, str]]
_QUIET_INTENTS = {"style", "chore", "test", "docs"}
_SEVERITY_ICON = {"high": "🔴", "medium": "🟠", "low": "🟡"}
_FENCE_LANG = {"python": "python", "javascript": "ts"}


def _cell(text: str | None) -> str:
    return re.sub(r"\s+", " ", (text or "").replace("|", "\\|")).strip()


def _slug(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]", "_", text)


def _clip(text: str, limit: int = 220) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


class Renderer:
    """Turns one analysis into the blocks of every documentation page."""

    def __init__(self, analysis: Analysis) -> None:
        self.a = analysis
        self.cfg = analysis.cfg
        self.out = self.cfg.out_dir
        self.symbols = analysis.project.symbols
        self.has_messages = any(m.source != "worktree" for m in analysis.messages.values())

    # --- linking helpers -----------------------------------------------------------------------

    def module_page(self, module: str) -> str:
        """Path of the API page for a module."""
        return f"{self.out}/api/{_slug(module)}.md"

    def rel(self, page: str, target: str) -> str:
        """Relative link from ``page`` to ``target`` (both relative to the project root)."""
        return posixpath.relpath(target, posixpath.dirname(page))

    def symbol_link(self, page: str, sid: str) -> str:
        """Markdown link to a symbol's reference entry, or plain code if it has none."""
        sym = self.symbols[sid]
        if not self.a.visible(sym):
            return f"`{sym.qualname}`"
        return f"[`{sym.qualname}`]({self.rel(page, self.module_page(sym.module))}#{sym.anchor})"

    def message_ref(self, msg: Message) -> str:
        """A message's label, linked to its URL when it has one."""
        label = f"`{msg.label}`"
        return f"[{label}]({msg.url})" if msg.url else label

    def summary_of(self, sym: Symbol) -> tuple[str, str]:
        """One-line description of a symbol and where it came from: doc | ai | inferred."""
        if is_documented(sym):
            return parse_docstring(sym.docstring).summary or first_sentence(sym.docstring or ""), "doc"
        if sym.id in self.a.summaries:
            return self.a.summaries[sym.id], "ai"
        return describe(sym.name, sym.kind), "inferred"

    def module_summary(self, module: Module) -> str:
        """First sentence of the module docstring, or a list of what it defines."""
        if module.docstring:
            return first_sentence(module.docstring)
        names = [s.name for s in module.symbols if self.a.visible(s) and not s.parent][:4]
        return f"Defines {', '.join(f'`{n}`' for n in names)}." if names else ""

    def module_owners(self, module: Module) -> list[tuple[str, float]]:
        """The top three authors of a module by surviving lines."""
        total: dict[str, float] = {}
        for sym in module.symbols:
            info = self.a.blame_info.get(sym.id)
            lines = sum(info.code.values()) + sum(info.doc.values()) if info else 0
            for name, share in owners(info, self.a.messages, top=10):
                total[name] = total.get(name, 0.0) + share * lines
        grand = sum(total.values())
        return sorted(((n, v / grand) for n, v in total.items()), key=lambda t: -t[1])[:3] if grand else []

    @staticmethod
    def _owner_text(pairs: list[tuple[str, float]]) -> str:
        return ", ".join(f"{name} ({share:.0%})" for name, share in pairs)

    def coverable(self, module: Module) -> list[Symbol]:
        """The module's visible classes, functions and methods - what documentation coverage counts."""
        return [s for s in module.symbols if self.a.visible(s) and s.kind != "constant"]

    def visible_modules(self) -> list[Module]:
        """Modules that get a page: those with visible symbols or a docstring."""
        return [m for _, m in sorted(self.a.project.modules.items()) if any(self.a.visible(s) for s in m.symbols) or m.docstring]

    # --- pages ---------------------------------------------------------------------------------

    def pages(self) -> dict[str, Blocks]:
        """Every page of the site, keyed by its path relative to the project root."""
        pages = {
            f"{self.out}/index.md": self.index_page(),
            f"{self.out}/architecture.md": self.architecture_page(),
            f"{self.out}/health.md": self.health_page(),
        }
        if self.a.has_git:
            pages[f"{self.out}/CHANGELOG.md"] = self.changelog_page()
        if self.has_messages:
            pages[f"{self.out}/decisions.md"] = self.decisions_page()
        for module in self.visible_modules():
            pages[self.module_page(module.name)] = self.api_page(module)
        return pages

    def health_line(self, page: str) -> str:
        """One-line health badge linking to the full report."""
        h = self.a.health
        drift_count = sum(h.counts.values())
        link = self.rel(page, f"{self.out}/health.md")
        return (f"**Documentation health: {h.score}/100** · {h.coverage:.0%} of {h.public} public symbols documented · "
                f"{drift_count} drift issue{'s' if drift_count != 1 else ''} ([report]({link}))")

    def module_table(self, page: str) -> str:
        """Table of modules with summary, API size, coverage and main authors."""
        authors = self.a.has_git  # without history there is nobody to credit
        rows = ["| Module | What it does | Public API | Documented |" + (" Main authors |" if authors else ""),
                "| --- | --- | ---: | ---: |" + (" --- |" if authors else "")]
        for module in self.visible_modules():
            public = self.coverable(module)
            documented = sum(1 for s in public if is_documented(s))
            pct = f"{documented / len(public):.0%}" if public else "-"
            row = (f"| [`{module.name}`]({self.rel(page, self.module_page(module.name))}) | {_cell(self.module_summary(module))} "
                   f"| {len(public)} | {pct} |")
            rows.append(row + (f" {_cell(self._owner_text(self.module_owners(module))) or '-'} |" if authors else ""))
        return "\n".join(rows)

    def recent_changes(self, page: str, limit: int = 8) -> str:
        """The latest meaningful commits (formatting and chores are skipped) with the API they touch."""
        lines = []
        for commit in self.a.commits:
            if commit.intent in _QUIET_INTENTS or is_docs_only(self.cfg, commit):
                continue
            touched = [self.symbol_link(page, sid) for sid, conf in self.a.symbols_of(commit.id) if conf >= 0.5 and self.a.visible(self.symbols[sid])][:3]
            suffix = f" - touches {', '.join(touched)}" if touched else ""
            lines.append(f"- {commit.day} · **{commit.intent}** · {commit.subject} ({self.message_ref(commit)}, {commit.author}){suffix}")
            if len(lines) >= limit:
                break
        return "\n".join(lines)

    def index_page(self) -> Blocks:
        """Landing page: health, project size, module table and recent changes."""
        page = f"{self.out}/index.md"
        p = self.a.project
        langs = sorted({m.language for m in p.modules.values()})
        blocks: Blocks = [
            ("title", f"# {self.cfg.name} documentation"),
            ("health", self.health_line(page)),
            ("overview", f"{len(p.modules)} modules · {len(p.symbols)} symbols · {sum(m.loc for m in p.modules.values())} lines of {' + '.join(langs) or 'code'}"
                         + ("" if self.a.has_git else " · no git history available, so rationale and staleness tracking are limited")
                         + "\n\n[Architecture](architecture.md) · [Health report](health.md)"
                         + (" · [Changelog](CHANGELOG.md)" if self.a.has_git else "")
                         + (" · [Decision log](decisions.md)" if self.has_messages else "")),
            ("modules", "## Modules\n\n" + self.module_table(page)),
        ]
        if recent := self.recent_changes(page):
            blocks.append(("recent", "## Recent changes\n\n" + recent))
        return blocks

    def symbol_block(self, page: str, sym: Symbol) -> str:
        """Reference entry for one symbol: signature, drift warnings, description, parameters, history."""
        level = "####" if sym.parent else "###"
        badges = [sym.kind] + (["async"] if sym.is_async else []) + ([] if sym.is_public else ["private"])
        out = [f'<a id="{sym.anchor}"></a>', f"{level} `{sym.qualname}` <sup>{' · '.join(badges)}</sup>", ""]
        decorators = "".join(f"@{d}\n" for d in sym.decorators) if sym.language == "python" else ""
        out += [f"```{_FENCE_LANG.get(sym.language, '')}", f"{decorators}{sym.signature}", "```", ""]

        for issue in self.a.issues_for(sym.id):
            if issue.kind == "undocumented-hotspot" or issue.file != sym.file:
                continue  # prose issues are reported against the Markdown file, not here
            out.append(f"> ⚠️ **Docs may be out of date** ({issue.severity}): {issue.message}")
            out += [f"> - {d}" for d in issue.detail]
            out.append("")

        info = parse_docstring(sym.docstring)
        summary, origin = self.summary_of(sym)
        if origin == "doc":
            out += [info.description or summary, ""]
        elif origin == "ai":
            out += [summary, "", "*No docstring in the source - this summary was AI-generated from the code and its history.*", ""]
        elif summary:
            out += [summary, "", "*No docstring in the source - this description is inferred from the name.*", ""]

        params = [p for p in sym.params if p.name != "{...}"]
        if params and sym.kind != "constant":
            rows = []
            for p in params:
                stars = {"vararg": "*", "kwarg": "**"}.get(p.kind, "") if sym.language == "python" else ("..." if p.kind == "vararg" else "")
                typ = p.annotation or info.param_types.get(p.name)
                rows.append({"Parameter": f"`{stars}{p.name}`", "Type": f"`{_cell(typ)}`" if typ else "",
                             "Default": f"`{_cell(p.default)}`" if p.default else "", "Description": _cell(info.params.get(p.name))})
            columns = ["Parameter"] + [c for c in ("Type", "Default", "Description") if any(r[c] for r in rows)]
            out += ["| " + " | ".join(columns) + " |", "|" + " --- |" * len(columns)]
            out += ["| " + " | ".join(r[c] for c in columns) + " |" for r in rows]
            out.append("")
        if sym.returns or info.returns:
            returns = " - ".join(x for x in (f"`{sym.returns}`" if sym.returns else "", info.returns if info.returns != "(documented)" else "") if x)
            out += [f"**Returns:** {returns}", ""]
        raises = sorted(set(sym.raises) | set(info.raises))
        if raises:
            out += ["**Raises:** " + "; ".join(f"`{r}`" + (f" - {info.raises[r]}" if info.raises.get(r) else "") for r in raises), ""]

        history = self.history(page, sym)
        if history:
            out += [f"<details><summary>History and rationale ({len(history)})</summary>", "", *history, "", "</details>", ""]

        facts = [f"[`{sym.file}:{sym.lineno}`]({self.rel(page, sym.file)}#L{sym.lineno})"]
        if sym.kind in ("function", "method"):
            facts.append(f"complexity {sym.complexity}")
        if who := owners(self.a.blame_info.get(sym.id), self.a.messages):
            facts.append("written by " + self._owner_text(who))
        out.append("<sub>" + " · ".join(facts) + "</sub>")
        return "\n".join(out)

    def history(self, page: str, sym: Symbol, limit: int = 6) -> list[str]:
        """The communication linked to a symbol, phrased as an annotated timeline."""
        links = [l for l in self.a.links.get(sym.id, []) if self.a.messages[l.message_id].source != "worktree"]
        loud = [l for l in links if self.a.messages[l.message_id].intent not in _QUIET_INTENTS]
        lines = []
        for link in (loud or links)[:limit]:
            msg = self.a.messages[link.message_id]
            why = rationale(msg.title, msg.body)
            if msg.source == "commit":
                head = f"{msg.day} · **{msg.intent}** · {msg.subject} ({self.message_ref(msg)}, {msg.author})"
            else:
                who = f", {msg.author}" if msg.author else ""
                text = msg.title if msg.source in ("pr", "issue", "note") else _clip(msg.body, 120)
                head = f"{msg.day} · **{msg.source}** · {text} ({self.message_ref(msg)}{who})"
            if why and (reason := _clip(" ".join(why))) not in head:
                head += f"<br>*Why:* {reason}"
            lines.append(f"- {head}")
        return lines

    def api_page(self, module: Module) -> Blocks:
        """Reference page for one module: header, table of contents, then one block per symbol."""
        page = self.module_page(module.name)
        head = [f"# `{module.name}`", ""]
        if module.docstring:
            head += [module.docstring.strip(), ""]
        facts = [f"Source: [`{module.file}`]({self.rel(page, module.file)})", f"{module.loc} lines"]
        if who := self.module_owners(module):
            facts.append("main authors: " + self._owner_text(who))
        head.append(" · ".join(facts))
        uses = sorted(self.a.edges.get(module.name, ()))
        used_by = sorted(src for src, targets in self.a.edges.items() if module.name in targets)
        link = lambda m: f"[`{m}`]({self.rel(page, self.module_page(m))})"  # noqa: E731
        pages = {m.name for m in self.visible_modules()}
        if uses:
            head += ["", "**Imports:** " + ", ".join(link(m) if m in pages else f"`{m}`" for m in uses)]
        if used_by:
            head += ["", "**Imported by:** " + ", ".join(link(m) if m in pages else f"`{m}`" for m in used_by)]
        if module.error:
            head += ["", f"> ⚠️ This file could not be analysed: {module.error}"]
        blocks: Blocks = [("module", "\n".join(head))]
        visible = [s for s in module.symbols if self.a.visible(s)]
        if visible:
            toc = ["| Symbol | Kind | Summary |", "| --- | --- | --- |"]
            for sym in visible:
                toc.append(f"| [`{sym.qualname}`](#{sym.anchor}) | {sym.kind} | {_cell(self.summary_of(sym)[0])} |")
            blocks.append(("contents", "## Contents\n\n" + "\n".join(toc) + "\n\n## Reference"))
        blocks += [(f"sym:{sym.qualname}", self.symbol_block(page, sym)) for sym in visible]
        return blocks

    def architecture_page(self) -> Blocks:
        """Dependency graph, import cycles, coupling table and churn-times-complexity hotspots."""
        page = f"{self.out}/architecture.md"
        edges = self.a.edges
        blocks: Blocks = [("title", "# Architecture"), ("health", self.health_line(page))]
        if edges:
            blocks.append(("graph", "## Module dependencies\n\nAn arrow means *imports*.\n\n```mermaid\n" + mermaid(edges) + "\n```"))
        loops = cycles(edges)
        text = "\n".join("- " + " → ".join(f"`{m}`" for m in loop) for loop in loops) if loops else "None found."
        blocks.append(("cycles", "## Import cycles\n\n" + text))
        if external := external_dependencies(self.a.project):
            blocks.append(("external", "## External dependencies\n\n" + ", ".join(f"`{d}`" for d in external)))

        fan_in = {m: sum(1 for t in edges.values() if m in t) for m in edges}
        rows = ["| Module | Imported by | Imports | Lines |", "| --- | ---: | ---: | ---: |"]
        for name in sorted(edges, key=lambda m: (-fan_in[m], m))[:15]:
            rows.append(f"| `{name}` | {fan_in[name]} | {len(edges[name])} | {self.a.project.modules[name].loc} |")
        blocks.append(("coupling", "## Most depended-upon modules\n\nChanges here ripple furthest, so these deserve the best documentation.\n\n" + "\n".join(rows)))

        churn: dict[str, int] = {}
        for commit in self.a.commits:
            for path, _a, _d in commit.files:
                churn[path] = churn.get(path, 0) + 1
        hot = []
        for module in self.a.project.modules.values():
            complexity = sum(s.complexity for s in module.symbols if s.kind in ("function", "method"))
            public = self.coverable(module)
            undocumented = sum(1 for s in public if not is_documented(s))
            if churn.get(module.file) and complexity:
                hot.append((churn[module.file] * complexity, module, churn[module.file], complexity, undocumented, len(public)))
        if hot:
            rows = ["| File | Commits | Complexity | Undocumented public symbols |", "| --- | ---: | ---: | ---: |"]
            for _score, module, commits, complexity, undocumented, public in sorted(hot, key=lambda t: (-t[0], t[1].file))[:10]:
                rows.append(f"| [`{module.file}`]({self.rel(page, self.module_page(module.name))}) | {commits} | {complexity} | {undocumented} of {public} |")
            blocks.append(("hotspots", "## Hotspots\n\nFiles that are both complex and frequently changed - where stale documentation costs the most.\n\n" + "\n".join(rows)))
        return blocks

    def changelog_page(self) -> Blocks:
        """Changelog with one block per release, each entry annotated with the API it touched."""
        page = f"{self.out}/CHANGELOG.md"
        blocks: Blocks = [("title", "# Changelog\n\nGenerated from commit history. Changes are grouped by what each commit *does*, "
                                    "classified from its message, and annotated with the public API it touches.")]

        def entry(commit: Message) -> str:
            scope = f"**{commit.scope}:** " if commit.scope else ""
            touched = [self.symbol_link(page, sid) for sid, conf in self.a.symbols_of(commit.id) if conf >= 0.5 and self.a.visible(self.symbols[sid])][:3]
            suffix = f" - {', '.join(touched)}" if touched else ""
            return f"- {scope}{commit.subject} ({self.message_ref(commit)}, {commit.author}){suffix}"

        for release in build_changelog(self.cfg, self.a.commits):
            out = [f"## {release.name}" + (f" - {release.date}" if release.date else "")]
            if release.breaking:
                out += ["", "### ⚠️ Breaking changes", "", *map(entry, release.breaking)]
            for intent in self.cfg.changelog_sections:
                if commits := release.sections.get(intent):
                    out += ["", f"### {INTENT_TITLES.get(intent, intent.title())}", "", *map(entry, commits)]
            blocks.append((f"release:{_slug(release.name)}", "\n".join(out)))
        return blocks

    def decisions_page(self) -> Blocks:
        """Decision log: messages that explain a choice, newest first, linked to the code they shaped."""
        page = f"{self.out}/decisions.md"
        blocks: Blocks = [("title", "# Decision log\n\nDesign decisions and their reasoning, mined from commit messages, pull requests, "
                                    "chat and notes. Each entry links the code it shaped.")]
        scored = []
        for msg in self.a.messages.values():
            # Housekeeping commits (docs, formatting, chores, tests) describe upkeep, not design.
            if msg.source == "worktree" or (msg.source == "commit" and (is_docs_only(self.cfg, msg) or msg.intent in _QUIET_INTENTS)):
                continue
            score = decision_score(msg.title, msg.body)
            if score >= 3.5:
                scored.append((msg.timestamp, msg.id, msg))
        for _ts, _id, msg in sorted(scored, key=lambda t: (-t[0], t[1])):
            title = msg.subject or msg.title or _clip(msg.body, 80)
            if msg.source == "chat":
                title = _clip(first_sentence(msg.body) or msg.body, 90)
            out = [f"### {title}", "", f"{msg.day} · {msg.source} {self.message_ref(msg)}" + (f" · {msg.author}" if msg.author else ""), ""]
            out += [f"> {_clip(s, 400)}" for s in rationale(msg.title, msg.body, limit=3)]
            shaped = [self.symbol_link(page, sid) for sid, conf in self.a.symbols_of(msg.id) if conf >= 0.4][:5]
            if shaped:
                out += ["", "Shaped: " + ", ".join(shaped)]
            blocks.append((f"decision:{_slug(msg.id)}", "\n".join(out)))
        if len(blocks) == 1:
            blocks.append(("empty", "No explained decisions were found yet. Commit bodies that say *why* (\"because…\", \"instead of…\") will appear here."))
        return blocks

    def health_page(self) -> Blocks:
        """Health report: score, every drift issue by severity, and per-module coverage."""
        page = f"{self.out}/health.md"
        h = self.a.health
        blocks: Blocks = [
            ("title", "# Documentation health"),
            ("score", self.health_line(page).replace(f" ([report]({self.rel(page, page)}))", "")
                      + "\n\nThe score is 40% coverage (public symbols with documentation) and 60% freshness (drift issues, weighted by severity)."),
        ]
        if self.a.issues:
            for severity in SEVERITIES:
                found = [i for i in self.a.issues if i.severity == severity]
                if not found:
                    continue
                out = [f"## {_SEVERITY_ICON[severity]} {severity.title()} ({len(found)})", ""]
                for issue in found:
                    out.append(f"- [`{issue.file}:{issue.line}`]({self.rel(page, issue.file)}#L{issue.line}) **{issue.kind}** - {issue.message}")
                    out += [f"  - {d}" for d in issue.detail]
                blocks.append((f"issues:{severity}", "\n".join(out)))
            kinds = sorted({i.kind for i in self.a.issues})
            blocks.append(("legend", "## What the checks mean\n\n" + "\n".join(f"- **{k}** - {ISSUE_HELP.get(k, '')}" for k in kinds)))
        else:
            blocks.append(("issues:none", "No drift detected: every documented claim matches the code."))

        rows = ["| Module | Documented | Undocumented public symbols |", "| --- | ---: | --- |"]
        for module in self.visible_modules():
            public = self.coverable(module)
            missing = [s for s in public if not is_documented(s)]
            if public:
                names = ", ".join(f"`{s.qualname}`" for s in missing[:8]) + (f" and {len(missing) - 8} more" if len(missing) > 8 else "")
                rows.append(f"| `{module.name}` | {len(public) - len(missing)}/{len(public)} | {names} |")
        blocks.append(("coverage", "## Coverage\n\n" + "\n".join(rows)))
        return blocks

    def inject_blocks(self, page: str) -> Blocks:
        """Blocks that can be embedded in hand-written files (README etc.) via region markers."""
        blocks: Blocks = [("health", self.health_line(page)), ("modules", self.module_table(page))]
        if self.a.edges:
            blocks.append(("architecture", "```mermaid\n" + mermaid(self.a.edges) + "\n```"))
        if recent := self.recent_changes(page):
            blocks.append(("recent", recent))
        return blocks


def render(analysis: Analysis) -> dict[str, str]:
    """Produce the final text of every documentation file, merged with what is already on disk."""
    cfg = analysis.cfg
    renderer = Renderer(analysis)
    files: dict[str, str] = {}
    for rel, blocks in renderer.pages().items():
        path = cfg.root / rel
        existing = path.read_text(encoding="utf-8") if path.is_file() else None
        files[rel] = regions.merge(existing, blocks)
    # Refresh managed regions that people have placed in their own Markdown files.
    for path in sorted(cfg.root.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        if regions.region_ids(text):
            merged = regions.merge(text, renderer.inject_blocks(path.name), inject_only=True)
            if merged.strip() != text.strip():
                files[path.name] = merged
    return files


def stale_pages(cfg, files: dict[str, str]) -> tuple[list[str], list[str]]:
    """Compare rendered ``files`` with disk: returns (changed or new files, orphaned API pages)."""
    changed = []
    for rel, text in files.items():
        path = cfg.root / rel
        if not path.is_file() or path.read_text(encoding="utf-8").replace("\r\n", "\n") != text:
            changed.append(rel)
    api = cfg.root / cfg.out_dir / "api"
    orphans = []
    for path in sorted(api.glob("*.md")) if api.is_dir() else []:
        rel = f"{cfg.out_dir}/api/{path.name}"
        text = path.read_text(encoding="utf-8", errors="replace")
        # Only fully generated pages are removed; one carrying hand-written notes is left alone.
        if rel not in files and regions.region_ids(text) and not regions.strip_regions(text).strip():
            orphans.append(rel)
    return sorted(changed), orphans


def write(cfg, files: dict[str, str]) -> tuple[list[str], list[str]]:
    """Write changed files, delete API pages for modules that no longer exist; return both lists."""
    changed, orphans = stale_pages(cfg, files)
    for rel in changed:
        path = cfg.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(files[rel], encoding="utf-8", newline="\n")
    for rel in orphans:
        Path(cfg.root / rel).unlink()
    return changed, orphans
