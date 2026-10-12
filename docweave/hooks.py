"""Keep docs in sync automatically: a git pre-commit hook and a CI workflow template."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from .config import Config

MARKER = "# docweave-hook"

CI_WORKFLOW = """\
name: docs

on:
  pull_request:
  push:
    branches: [main]

jobs:
  docweave:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0 # DocWeave reads commit history and blame
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      # Install DocWeave however you distribute it (a git URL, an internal index, or a vendored copy).
      - run: pip install docweave

      # On pull requests: annotate the diff with documentation drift and fail on serious issues.
      - if: github.event_name == 'pull_request'
        run: docweave check --format github

      # On main: regenerate the docs and commit them if anything changed.
      - if: github.event_name == 'push'
        run: |
          docweave generate
          git config user.name "docweave"
          git config user.email "docweave@users.noreply.github.com"
          git add -A {out_dir} .docweave/state.json
          git diff --cached --quiet || git commit -m "docs: regenerate with docweave [skip ci]"
          git push
"""


def _hook_path(cfg: Config) -> Path:
    out = subprocess.run(["git", "rev-parse", "--git-path", "hooks"], cwd=cfg.root, capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError("not a git repository")
    return (cfg.root / out.stdout.strip() / "pre-commit").resolve()


def install_hook(cfg: Config, sync: bool = False, force: bool = False) -> Path:
    """Install a pre-commit hook.

    By default the hook blocks a commit when the files it stages have high-severity drift
    (drift elsewhere in the project is not held against it). With ``sync`` it instead
    regenerates the docs and stages them, so docs travel in the same commit as the code.
    """
    path = _hook_path(cfg)
    if path.exists() and MARKER not in path.read_text(encoding="utf-8", errors="replace") and not force:
        raise RuntimeError(f"{path} already exists and was not created by docweave (use --force to replace it)")
    python = Path(sys.executable).as_posix()
    if sync:
        body = f'"{python}" -m docweave generate --quiet || exit 1\ngit add -A "{cfg.out_dir}" .docweave/state.json\n'
    else:
        body = (f'"{python}" -m docweave check --staged --quiet || {{\n'
                '  echo "docweave: this commit touches code whose documentation is out of date."\n'
                '  echo "Run \'docweave check\' for details, fix the docs, or commit with --no-verify to skip."\n'
                "  exit 1\n}\n")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"#!/bin/sh\n{MARKER} (managed by `docweave hook install`)\n{body}", encoding="utf-8", newline="\n")
    path.chmod(0o755)
    return path


def uninstall_hook(cfg: Config) -> bool:
    """Remove the pre-commit hook if DocWeave installed it; returns whether anything was removed."""
    path = _hook_path(cfg)
    if path.exists() and MARKER in path.read_text(encoding="utf-8", errors="replace"):
        path.unlink()
        return True
    return False


def write_ci(cfg: Config) -> Path:
    """Write the GitHub Actions workflow and return its path."""
    path = cfg.root / ".github" / "workflows" / "docweave.yml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(CI_WORKFLOW.replace("{out_dir}", cfg.out_dir), encoding="utf-8", newline="\n")
    return path
