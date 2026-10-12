"""Language analyzers and source discovery."""

from __future__ import annotations

import fnmatch
import os
from pathlib import Path

from ..config import Config
from ..model import Module, Project
from . import javascript, python

ANALYZERS = {ext: mod.analyze for mod in (python, javascript) for ext in mod.EXTENSIONS}


def is_excluded(rel: str, patterns: list[str]) -> bool:
    """True if any path component, or the whole relative path, matches an exclude pattern."""
    parts = rel.split("/")
    return any(fnmatch.fnmatch(part, pat) for part in parts for pat in patterns) or any(
        fnmatch.fnmatch(rel, pat) for pat in patterns
    )


def discover(cfg: Config, extensions: tuple[str, ...], sources: list[str] | None = None) -> list[str]:
    """List project files (posix paths relative to the root) having one of ``extensions``."""
    found: set[str] = set()
    for src in sources or cfg.source:
        base = (cfg.root / src).resolve()
        for dirpath, dirnames, filenames in os.walk(base):
            rel_dir = Path(dirpath).resolve().relative_to(cfg.root).as_posix()
            rel_dir = "" if rel_dir == "." else rel_dir
            dirnames[:] = sorted(
                d for d in dirnames if not is_excluded(f"{rel_dir}/{d}".lstrip("/"), cfg.excludes)
            )
            for fn in filenames:
                rel = f"{rel_dir}/{fn}".lstrip("/")
                if fn.lower().endswith(extensions) and not is_excluded(rel, cfg.excludes):
                    found.add(rel)
    return sorted(found)


def scan(cfg: Config) -> Project:
    """Run static analysis over every supported source file in the project."""
    project = Project(name=cfg.name)
    for rel in discover(cfg, tuple(ANALYZERS)):
        try:
            text = (cfg.root / rel).read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            project.modules[rel] = Module(name=rel, file=rel, language="unknown", error=str(exc))
            continue
        module = ANALYZERS[os.path.splitext(rel)[1].lower()](rel, text)
        if module.name in project.modules:  # e.g. util.py next to util.js
            module.name = f"{module.name}[{module.language}]"
            for sym in module.symbols:
                sym.module = module.name
                sym.id = f"{module.name}:{sym.qualname}"
                if sym.parent:
                    sym.parent = f"{module.name}:{sym.parent.split(':', 1)[1]}"
        project.modules[module.name] = module
    return project
