"""Core data model shared by analyzers, the linker, drift detection and renderers."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Param:
    """One parameter of a function signature."""

    name: str
    annotation: str | None = None
    default: str | None = None
    kind: str = "positional"  # positional | keyword | vararg | kwarg


@dataclass
class Symbol:
    """One documentable unit of code: a class, function, method or constant."""

    id: str  # "<module>:<qualname>"
    name: str
    qualname: str
    kind: str  # class | function | method | constant
    module: str
    file: str  # posix path relative to the project root
    language: str
    lineno: int
    end_lineno: int
    sig_end: int  # last line of the signature (before the body/docstring)
    signature: str
    params: list[Param] = field(default_factory=list)
    returns: str | None = None
    docstring: str | None = None
    doc_range: tuple[int, int] | None = None
    decorators: list[str] = field(default_factory=list)
    bases: list[str] = field(default_factory=list)
    parent: str | None = None
    is_public: bool = True
    is_async: bool = False
    is_stub: bool = False
    returns_value: bool = False
    complexity: int = 1
    calls: list[str] = field(default_factory=list)
    raises: list[str] = field(default_factory=list)
    interface_hash: str = ""
    body_hash: str = ""

    @property
    def anchor(self) -> str:
        """HTML anchor used for this symbol on its API page."""
        return self.qualname.lower().replace(".", "-").replace("_", "-")


@dataclass
class Module:
    """One analysed source file."""

    name: str
    file: str
    language: str
    docstring: str | None = None
    imports: list[str] = field(default_factory=list)  # raw imported module names
    symbols: list[Symbol] = field(default_factory=list)
    loc: int = 0
    error: str | None = None


@dataclass
class Project:
    """All analysed modules of one project."""

    name: str
    modules: dict[str, Module] = field(default_factory=dict)

    @property
    def symbols(self) -> dict[str, Symbol]:
        """Every symbol in the project, keyed by id."""
        return {s.id: s for m in self.modules.values() for s in m.symbols}

    def by_file(self) -> dict[str, Module]:
        """Modules keyed by file path."""
        return {m.file: m for m in self.modules.values()}


@dataclass
class Message:
    """A unit of developer communication: a commit, PR, issue, chat message or note."""

    id: str  # "commit:<sha>", "pr:12", "chat:<channel>:<ts>", "note:<file>"
    source: str  # commit | pr | issue | chat | note | worktree
    author: str = ""
    date: datetime | None = None
    title: str = ""
    body: str = ""
    url: str | None = None
    files: list[tuple[str, int, int]] = field(default_factory=list)  # (path, added, deleted)
    tags: list[str] = field(default_factory=list)
    # Filled in by the NLP pass:
    intent: str = "other"
    subject: str = ""  # title with any "type(scope):" prefix and "(#12)" suffix removed
    scope: str | None = None
    breaking: bool = False
    confidence: float = 0.0

    @property
    def sha(self) -> str | None:
        """Full commit hash, or None for anything that is not a commit."""
        return self.id.split(":", 1)[1] if self.source == "commit" else None

    @property
    def text(self) -> str:
        """Title and body together, as fed to the NLP passes."""
        if self.source == "chat":  # a chat message's "title" is only its channel name
            return self.body.strip()
        return f"{self.title}\n\n{self.body}".strip()

    @property
    def timestamp(self) -> float:
        """Seconds since the epoch (0 when undated), for ordering."""
        if self.date is None:
            return 0.0
        d = self.date if self.date.tzinfo else self.date.replace(tzinfo=timezone.utc)
        return d.timestamp()

    @property
    def day(self) -> str:
        """Date as YYYY-MM-DD."""
        return self.date.strftime("%Y-%m-%d") if self.date else "undated"

    @property
    def label(self) -> str:
        """Short human-readable reference: abbreviated hash, ``pr:12`` or ``#channel``."""
        if self.source == "commit":
            return (self.sha or "")[:7]
        if self.source == "chat" and self.title:
            return self.title
        return "uncommitted" if self.source == "worktree" else self.id


@dataclass
class Link:
    """Evidence that a message is about a symbol."""

    message_id: str
    confidence: float
    reasons: list[str] = field(default_factory=list)
    lines: int = 0  # surviving lines of the symbol last written by this commit


@dataclass
class Issue:
    """A detected documentation problem."""

    kind: str
    severity: str  # high | medium | low
    file: str
    line: int
    message: str
    symbol: str | None = None
    detail: list[str] = field(default_factory=list)

    def sort_key(self) -> tuple:
        """Order issues by severity, then location."""
        return ({"high": 0, "medium": 1, "low": 2}[self.severity], self.file, self.line, self.kind)
