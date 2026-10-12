"""Configuration: defaults, overridden by ``docweave.toml`` or ``[tool.docweave]`` in pyproject."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field, fields
from pathlib import Path

DEFAULT_EXCLUDE = [
    ".git", ".hg", ".svn", ".venv", "venv", "env", "node_modules", "__pycache__", ".tox",
    ".mypy_cache", ".pytest_cache", "build", "dist", "site-packages", ".docweave", "*.egg-info",
    "tests", "test", "test_*.py", "*_test.py", "conftest.py", "*.test.js", "*.test.ts",
    "*.spec.js", "*.spec.ts", "*.min.js", "*.d.ts", "setup.py",
]

CONFIG_TEMPLATE = """\
# DocWeave configuration. Every key is optional; the values below are the defaults.

# name = "my-project"          # defaults to the folder name
out_dir = "docs"                # where generated documentation is written
source = ["."]                  # folders to analyse, relative to this file
# exclude = ["migrations"]      # extra folder / file patterns to skip
include_private = false         # document _private symbols too
comms_dir = "comms"             # optional exports of PRs, issues, chat, meeting notes
history_limit = 2000            # how many commits of history to read
fail_on = "high"                # `docweave check` fails at this severity: high | medium | low
changelog_sections = ["feature", "fix", "perf", "security", "deprecation", "refactor"]
llm_model = "claude-opus-5-5"   # used only with --llm
"""


@dataclass
class Config:
    """Resolved settings for one project."""

    root: Path
    name: str = ""
    out_dir: str = "docs"
    source: list[str] = field(default_factory=lambda: ["."])
    exclude: list[str] = field(default_factory=list)
    include_private: bool = False
    comms_dir: str = "comms"
    history_limit: int = 2000
    fail_on: str = "high"
    changelog_sections: list[str] = field(
        default_factory=lambda: ["feature", "fix", "perf", "security", "deprecation", "refactor"]
    )
    llm_model: str = "claude-opus-5-5"

    @property
    def excludes(self) -> list[str]:
        """Built-in exclude patterns plus the project's own."""
        return DEFAULT_EXCLUDE + self.exclude

    @property
    def state_dir(self) -> Path:
        """Folder for DocWeave's own state (signature anchors, AI cache)."""
        return self.root / ".docweave"


def load_config(root: Path | str, **overrides) -> Config:
    """Load configuration for the project at ``root``, applying non-None ``overrides`` last."""
    root = Path(root).resolve()
    data: dict = {}
    toml = root / "docweave.toml"
    pyproject = root / "pyproject.toml"
    if toml.is_file():
        data = tomllib.loads(toml.read_text(encoding="utf-8"))
    elif pyproject.is_file():
        try:
            data = tomllib.loads(pyproject.read_text(encoding="utf-8")).get("tool", {}).get("docweave", {})
        except tomllib.TOMLDecodeError:
            data = {}
    known = {f.name for f in fields(Config)} - {"root"}
    unknown = set(data) - known
    if unknown:
        raise ValueError(f"Unknown docweave config key(s): {', '.join(sorted(unknown))}")
    data.update({k: v for k, v in overrides.items() if v is not None})
    cfg = Config(root=root, **data)
    if cfg.fail_on not in ("high", "medium", "low"):
        raise ValueError("fail_on must be one of: high, medium, low")
    cfg.name = cfg.name or root.name
    cfg.out_dir = cfg.out_dir.strip("/\\").replace("\\", "/")
    return cfg
