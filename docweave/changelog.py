"""Group commits into a release-by-release changelog, using classified intent rather than prefixes."""

from __future__ import annotations

from dataclasses import dataclass, field

from .config import Config
from .model import Message


@dataclass
class Release:
    """One changelog section: a tagged version, or the unreleased work since the last tag."""

    name: str
    date: str | None = None
    breaking: list[Message] = field(default_factory=list)
    sections: dict[str, list[Message]] = field(default_factory=dict)

    @property
    def empty(self) -> bool:
        """True when no commit in this release is worth listing."""
        return not self.breaking and not any(self.sections.values())


def is_docs_only(cfg: Config, commit: Message) -> bool:
    """True for commits that only touched generated output, so regenerating docs is a fixpoint."""
    prefixes = (cfg.out_dir + "/", ".docweave/")
    return bool(commit.files) and all(path.startswith(prefixes) for path, _a, _d in commit.files)


def build_changelog(cfg: Config, commits: list[Message]) -> list[Release]:
    """Split ``commits`` (newest first) into releases at tagged commits, grouped by intent."""
    releases = [Release("Unreleased")]
    for commit in commits:
        if commit.tags:
            releases.append(Release(commit.tags[0], commit.day))
        if commit.source != "commit" or is_docs_only(cfg, commit):
            continue
        release = releases[-1]
        if commit.breaking:
            release.breaking.append(commit)
        elif commit.intent in cfg.changelog_sections:
            release.sections.setdefault(commit.intent, []).append(commit)
    return [r for r in releases if not r.empty]
