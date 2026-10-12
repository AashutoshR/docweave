"""Read developer communication and line-level authorship out of git."""

from __future__ import annotations

import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from .model import Message

UNCOMMITTED = "0" * 40
_LOG_FORMAT = "%x1e%H%x1f%an%x1f%cI%x1f%D%x1f%s%x1f%b%x1d"
_BLAME_HEADER = re.compile(r"^([0-9a-f]{40}) \d+ \d+")
_DEF_LINE = re.compile(
    r"^([-+])\s*(?:export\s+(?:default\s+)?)?(?:async\s+)?(?:def|class|function\*?)\s+([A-Za-z_$][\w$]*)"
)
_SOURCE_GLOBS = ["*.py", "*.js", "*.jsx", "*.mjs", "*.cjs", "*.ts", "*.tsx"]


@dataclass
class Removal:
    """A definition that used to exist: which commit deleted it and what appeared in its place."""

    name: str
    sha: str
    file: str
    replacements: list[str] = field(default_factory=list)


def _numstat_path(path: str) -> str:
    """Normalise git's rename notation (``a/{old => new}/c`` or ``old => new``) to the new path."""
    path = re.sub(r"\{[^{}]*? => ([^{}]*?)\}", r"\1", path)
    if " => " in path:
        path = path.split(" => ", 1)[1]
    return path.replace("//", "/")


class GitRepo:
    """Thin, read-only wrapper around the ``git`` command line for one work tree."""

    def __init__(self, root: Path) -> None:
        self.root = root

    @classmethod
    def open(cls, root: Path) -> "GitRepo | None":
        """Return a repo handle if ``root`` is inside a git work tree that has at least one commit."""
        repo = cls(root)
        try:
            if repo._git("rev-parse", "--is-inside-work-tree").strip() != "true":
                return None
            repo._git("rev-parse", "--verify", "HEAD")
        except (OSError, subprocess.CalledProcessError):
            return None
        return repo

    def _git(self, *args: str, check: bool = True, stdin: str | None = None) -> str:
        proc = subprocess.run(
            ["git", "-c", "core.quotepath=off", *args], cwd=self.root, input=stdin,
            capture_output=True, text=True, encoding="utf-8", errors="replace", check=check,
        )
        return proc.stdout

    def _parse_log(self, out: str) -> list[Message]:
        web = self.web_url()
        messages: list[Message] = []
        for chunk in out.split("\x1e")[1:]:
            head, _, tail = chunk.partition("\x1d")
            fields = head.split("\x1f")
            if len(fields) < 6:
                continue
            sha, author, date, refs, subject, body = fields[:6]
            files = []
            for line in tail.splitlines():
                parts = line.split("\t")
                if len(parts) == 3:
                    added, deleted, path = parts
                    files.append((_numstat_path(path), int(added) if added.isdigit() else 0, int(deleted) if deleted.isdigit() else 0))
            messages.append(
                Message(
                    id=f"commit:{sha}", source="commit", author=author, date=datetime.fromisoformat(date),
                    title=subject.strip(), body=body.strip(), files=files,
                    url=f"{web}/commit/{sha}" if web else None,
                    tags=[r.strip()[5:] for r in refs.split(",") if r.strip().startswith("tag: ")],
                )
            )
        return messages

    def log(self, limit: int) -> list[Message]:
        """Commits reachable from HEAD, newest first, with per-file line counts."""
        out = self._git("log", "--no-merges", f"-n{limit}", "--relative", "--numstat", f"--format={_LOG_FORMAT}")
        return self._parse_log(out)

    def show(self, shas: list[str]) -> list[Message]:
        """Look up specific commits (those that blame found beyond the history limit)."""
        found: list[Message] = []
        for i in range(0, len(shas), 100):
            out = self._git("log", "--no-walk", "--relative", "--numstat", f"--format={_LOG_FORMAT}", *shas[i : i + 100], check=False)
            found += self._parse_log(out)
        return found

    def blame(self, rel: str) -> list[str] | None:
        """Commit sha that last touched each line of ``rel`` (index 0 is line 1); None if untracked."""
        try:
            out = self._git("blame", "--line-porcelain", "-w", "-M", "--", rel)
        except subprocess.CalledProcessError:
            return None
        shas: list[str] = []
        current = UNCOMMITTED
        for line in out.split("\n"):
            if line.startswith("\t"):
                shas.append(current)
            elif m := _BLAME_HEADER.match(line):
                current = m[1]
        return shas

    def blame_many(self, files: list[str]) -> dict[str, list[str]]:
        """Blame several files concurrently; untracked files are left out."""
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = pool.map(self.blame, files)
        return {f: b for f, b in zip(files, results) if b}

    def removed_definitions(self, limit: int) -> dict[str, Removal]:
        """Names of functions/classes that history shows were deleted or renamed, newest removal first.

        A definition counts as removed when a commit deletes its ``def``/``class``/``function`` line
        without adding one for the same name. Definitions added by that same commit to the same
        file are recorded as likely replacements (that is what a rename looks like in a diff).
        """
        out = self._git(
            "log", "--no-merges", f"-n{limit}", "--relative", "-p", "-U0", "--no-color",
            "--format=%x1e%H", "--", *_SOURCE_GLOBS, check=False,
        )
        graveyard: dict[str, Removal] = {}
        for chunk in out.split("\x1e")[1:]:
            lines = chunk.split("\n")
            sha = lines[0].strip()
            per_file: dict[str, tuple[set[str], set[str]]] = {}
            current = ""
            for line in lines[1:]:
                if line.startswith("diff --git "):
                    current = line.rsplit(" b/", 1)[-1]
                elif (m := _DEF_LINE.match(line)) and not line.startswith(("---", "+++")):
                    removed, added = per_file.setdefault(current, (set(), set()))
                    (removed if m[1] == "-" else added).add(m[2])
            for path, (removed, added) in per_file.items():
                for name in removed - added:
                    graveyard.setdefault(name, Removal(name, sha, path, sorted(added - removed)))
        return graveyard

    def staged_files(self) -> list[str]:
        """Paths with changes staged for the next commit."""
        return [ln.strip() for ln in self._git("diff", "--cached", "--name-only", "--relative", check=False).splitlines() if ln.strip()]

    def deleted_files(self, limit: int) -> dict[str, str]:
        """Paths that history shows were deleted, mapped to the commit that deleted them."""
        out = self._git("log", "--no-merges", f"-n{limit}", "--relative", "--diff-filter=D", "--name-only", "--format=%x1e%H", check=False)
        deleted: dict[str, str] = {}
        for chunk in out.split("\x1e")[1:]:
            lines = [ln.strip() for ln in chunk.splitlines() if ln.strip()]
            for path in lines[1:]:
                deleted.setdefault(path, lines[0])
        return deleted

    def web_url(self) -> str | None:
        """Browser URL of the ``origin`` remote, for linking commits and pull requests."""
        if not hasattr(self, "_web"):
            url = self._git("remote", "get-url", "origin", check=False).strip()
            m = re.match(r"(?:git@|ssh://git@|https?://)(?:[^@/]+@)?([^:/]+)[:/](.+?)(?:\.git)?/?$", url)
            self._web = f"https://{m[1]}/{m[2]}" if m else None
        return self._web


def worktree_message() -> Message:
    """Stand-in 'commit' for lines that are modified but not committed yet."""
    return Message(
        id=f"commit:{UNCOMMITTED}", source="worktree", author="(uncommitted)",
        date=datetime.now(timezone.utc), title="Uncommitted changes in the working tree", intent="wip",
    )
