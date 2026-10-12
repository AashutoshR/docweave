"""The analysis pipeline: code structure + developer communication -> one linked model."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

from . import drift
from .analyzers import discover, scan
from .comms import load_comms
from .config import Config
from .gitrepo import UNCOMMITTED, GitRepo, Removal, worktree_message
from .graph import internal_edges
from .linker import BlameInfo, Linker, symbol_blame
from .model import Issue, Link, Message, Project, Symbol
from .nlp.intent import classify


@dataclass
class Analysis:
    """Everything known about a project after one run: code, communication, links and drift."""

    cfg: Config
    project: Project
    has_git: bool
    messages: dict[str, Message]
    commits: list[Message]  # newest first
    blame_info: dict[str, BlameInfo]
    links: dict[str, list[Link]]
    issues: list[Issue]
    references: list[drift.Reference]
    health: drift.Health
    edges: dict[str, set[str]]
    state: dict
    graveyard: dict[str, Removal] = field(default_factory=dict)
    summaries: dict[str, str] = field(default_factory=dict)  # optional AI-written summaries

    def visible(self, sym: Symbol) -> bool:
        """Whether a symbol belongs in the generated docs."""
        return sym.is_public or self.cfg.include_private

    def symbols_of(self, message_id: str) -> list[tuple[str, float]]:
        """Symbols a message is linked to, strongest link first."""
        if not hasattr(self, "_by_message"):
            by_message: dict[str, list[tuple[str, float]]] = defaultdict(list)
            for sid, links in self.links.items():
                for link in links:
                    by_message[link.message_id].append((sid, link.confidence))
            self._by_message = {m: sorted(v, key=lambda t: (-t[1], t[0])) for m, v in by_message.items()}
        return self._by_message.get(message_id, [])

    def issues_for(self, symbol_id: str) -> list[Issue]:
        """Drift issues attached to one symbol."""
        return [i for i in self.issues if i.symbol == symbol_id]


def analyze(cfg: Config, use_git: bool = True) -> Analysis:
    """Run static analysis, read history and communication, link them, and detect drift."""
    project = scan(cfg)
    repo = GitRepo.open(cfg.root) if use_git else None

    commits: list[Message] = []
    blame: dict[str, list[str]] = {}
    graveyard: dict[str, Removal] = {}
    deleted: dict[str, str] = {}
    if repo is not None:
        commits = repo.log(cfg.history_limit)
        prose = [f for f in discover(cfg, (".md",), sources=["."]) if not f.startswith(cfg.out_dir + "/")]
        blame = repo.blame_many(sorted({m.file for m in project.modules.values()} | set(prose)))
        known = {c.sha for c in commits}
        missing = sorted({sha for shas in blame.values() for sha in shas} - known - {UNCOMMITTED})
        commits += repo.show(missing)
        graveyard = repo.removed_definitions(cfg.history_limit)
        deleted = repo.deleted_files(cfg.history_limit)
        current = {s.name for s in project.symbols.values()}
        graveyard = {name: r for name, r in graveyard.items() if name not in current}

    messages: dict[str, Message] = {c.id: c for c in commits}
    if any(UNCOMMITTED in shas for shas in blame.values()):
        wip = worktree_message()
        messages[wip.id] = wip
    for msg in load_comms(cfg.root / cfg.comms_dir):
        messages.setdefault(msg.id, msg)
    for msg in messages.values():
        if msg.source != "worktree":
            msg.intent, msg.scope, msg.breaking, msg.confidence, msg.subject = classify(msg.title, msg.body)

    blame_info = symbol_blame(project, blame)
    links = Linker(project, messages, blame_info).run()
    state = drift.next_state(project, drift.load_state(cfg))
    issues, references = drift.detect(cfg, project, messages, blame, blame_info, graveyard, deleted, state)
    commits.sort(key=lambda c: -c.timestamp)
    return Analysis(
        cfg=cfg, project=project, has_git=repo is not None, messages=messages, commits=commits,
        blame_info=blame_info, links=links, issues=issues, references=references,
        health=drift.health(cfg, project, issues), edges=internal_edges(project),
        state=state, graveyard=graveyard,
    )
