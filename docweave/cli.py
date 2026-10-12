"""Command-line interface: ``docweave <command>``."""

from __future__ import annotations

import argparse
import difflib
import json
import sys
import time
from pathlib import Path

from . import __version__, drift, hooks, render
from .analyzers import ANALYZERS, discover
from .changelog import build_changelog
from .comms import pull_github
from .config import CONFIG_TEMPLATE, Config, load_config
from .engine import Analysis, analyze
from .gitrepo import GitRepo
from .linker import owners
from .nlp.intent import INTENT_TITLES
from .nlp.rationale import rationale
from .search import search

_RANK = {"high": 0, "medium": 1, "low": 2}


def _config(args) -> Config:
    return load_config(args.root, out_dir=getattr(args, "out", None))


def _analyze(args) -> Analysis:
    return analyze(_config(args), use_git=not args.no_git)


def _summary(a: Analysis) -> str:
    h = a.health
    return (f"health {h.score}/100 | {h.documented}/{h.public} public symbols documented | "
            f"drift: {h.counts['high']} high, {h.counts['medium']} medium, {h.counts['low']} low")


def _generate(args, quiet: bool = False) -> Analysis:
    a = _analyze(args)
    if getattr(args, "llm", False):
        from .llm import LLMError, summarize_undocumented

        try:
            a.summaries = summarize_undocumented(a, progress=lambda m: print(f"  llm: {m}", file=sys.stderr))
        except LLMError as exc:
            print(f"docweave: {exc}", file=sys.stderr)
            raise SystemExit(2) from exc
    changed, removed = render.write(a.cfg, render.render(a))
    if any(not rel.startswith(a.cfg.out_dir + "/") for rel in changed):
        # A hand-written file had a managed region refreshed, which can shift the line numbers
        # that drift reports cite. Analyse once more so the output is a fixpoint.
        summaries, a = a.summaries, _analyze(args)
        a.summaries = summaries
        again, _ = render.write(a.cfg, render.render(a))
        changed = sorted(set(changed) | set(again))
    drift.save_state(a.cfg, a.state)
    if not quiet:
        for rel in changed:
            print(f"  wrote   {rel}")
        for rel in removed:
            print(f"  removed {rel}")
        if not changed and not removed:
            print("  docs already up to date")
        print(_summary(a))
        if not a.has_git:
            print("note: no git history found - rationale, ownership and blame-based staleness are unavailable")
    return a


def cmd_init(args) -> int:
    """Write a starter docweave.toml and, on request, the CI workflow and git hook."""
    cfg = _config(args)
    path = cfg.root / "docweave.toml"
    if path.exists():
        print(f"{path.name} already exists")
    else:
        path.write_text(CONFIG_TEMPLATE, encoding="utf-8", newline="\n")
        print(f"created {path.name}")
    if args.ci:
        print(f"created {hooks.write_ci(cfg).relative_to(cfg.root).as_posix()}")
    if args.hook:
        print(f"installed {hooks.install_hook(cfg)}")
    print("next: docweave generate")
    return 0


def cmd_generate(args) -> int:
    """Analyse the project and write the documentation site."""
    _generate(args, quiet=args.quiet)
    return 0


def cmd_check(args) -> int:
    """Report drift in the chosen format and return 1 if anything reaches the failure threshold."""
    a = _analyze(args)
    threshold = _RANK[args.fail_on or a.cfg.fail_on]
    failing = [i for i in a.issues if _RANK[i.severity] <= threshold]
    if args.staged:
        # Hold a commit responsible only for the files it touches, so a project with existing
        # drift can adopt the hook without first fixing everything.
        repo = GitRepo.open(a.cfg.root)
        staged = set(repo.staged_files()) if repo else set()
        failing = [i for i in failing if i.file in staged or (i.symbol and a.project.symbols[i.symbol].file in staged)]
    outdated: list[str] = []
    if args.require_fresh:
        changed, removed = render.stale_pages(a.cfg, render.render(a))
        outdated = changed + removed
    if args.format == "json":
        print(json.dumps({
            "health": {"score": a.health.score, "public": a.health.public, "documented": a.health.documented, **a.health.counts},
            "issues": [vars(i) for i in a.issues], "outdated": outdated,
        }, indent=2))
    elif args.format == "github":
        level = {"high": "error", "medium": "warning", "low": "notice"}
        for i in a.issues:
            detail = "; ".join(i.detail)
            text = (i.message + (f" ({detail})" if detail else "")).replace("%", "%25").replace("\n", "%0A")
            print(f"::{level[i.severity]} file={i.file},line={i.line},title=docweave {i.kind}::{text}")
        for rel in outdated:
            print(f"::error file={rel},title=docweave::generated docs are out of date; run `docweave generate`")
    elif not args.quiet or failing or outdated:
        for i in failing if args.quiet else a.issues:
            print(f"{i.severity.upper():6} {i.file}:{i.line}  [{i.kind}] {i.message}")
            for d in i.detail:
                print(f"         - {d}")
        for rel in outdated:
            print(f"STALE  {rel}  generated docs are out of date; run `docweave generate`")
        print(_summary(a))
    return 1 if failing or outdated else 0


def _find_symbol(a: Analysis, name: str):
    index = drift.name_index(a.project)
    modules = set(a.project.modules) | {m.rpartition(".")[2] for m in a.project.modules}
    ids = drift.resolve_name(name.removesuffix("()"), index, modules)
    if not ids:
        close = difflib.get_close_matches(name, list(index), n=5, cutoff=0.5)
        print(f"no symbol named `{name}`" + (f"; did you mean: {', '.join(close)}?" if close else ""), file=sys.stderr)
    return [a.project.symbols[i] for i in ids]


def cmd_why(args) -> int:
    """Print who wrote a symbol, what is wrong with its docs, and the discussion linked to it."""
    a = _analyze(args)
    symbols = _find_symbol(a, args.symbol)
    for sym in symbols:
        print(f"{sym.qualname}  ({sym.kind}, {sym.file}:{sym.lineno})")
        print(f"  {sym.signature}")
        if who := owners(a.blame_info.get(sym.id), a.messages):
            print("  written by: " + ", ".join(f"{n} ({s:.0%})" for n, s in who))
        for issue in a.issues_for(sym.id):
            print(f"  ! {issue.severity} ({issue.file}:{issue.line}): {issue.message}")
        links = [l for l in a.links.get(sym.id, []) if a.messages[l.message_id].source != "worktree"]
        if not links:
            print("  no linked history" + ("" if a.has_git else " (not a git repository)"))
        for link in links[: args.limit]:
            msg = a.messages[link.message_id]
            print(f"\n  {msg.day}  {msg.source} {msg.label}  [{msg.intent}]  {msg.author}  (confidence {link.confidence:.2f}: {'; '.join(link.reasons)})")
            print(f"    {msg.subject or msg.title or ' '.join(msg.body.split())[:100]}")
            for sentence in rationale(msg.title, msg.body):
                print(f"    why: {sentence}")
        print()
    return 0 if symbols else 1


def cmd_ask(args) -> int:
    """Answer a question with the best-matching symbols and discussions."""
    a = _analyze(args)
    hits = search(a, args.question, k=args.limit)
    if not hits:
        print("nothing relevant found")
        return 1
    if args.llm:
        from .llm import LLMError, answer

        context = "\n\n".join(f"[{h.kind}] {h.title} ({h.location})\n{h.snippet}" for h in hits)
        try:
            print(answer(a, args.question, context) + "\n\nSources:")
        except LLMError as exc:
            print(f"docweave: {exc}", file=sys.stderr)
            return 2
    for h in hits:
        print(f"{h.score:6.2f}  [{h.kind}] {h.title}  -  {h.location}")
        for line in h.snippet.split("\n"):
            if line.strip():
                print(f"          {line.strip()}")
    return 0


def cmd_changelog(args) -> int:
    """Print the changelog to standard output without writing any files."""
    a = _analyze(args)
    if not a.has_git:
        print("docweave: changelog needs a git repository with at least one commit", file=sys.stderr)
        return 1
    for release in build_changelog(a.cfg, a.commits):
        print(f"## {release.name}" + (f" - {release.date}" if release.date else ""))
        groups = [("Breaking changes", release.breaking)] + [(INTENT_TITLES.get(k, k), release.sections.get(k, [])) for k in a.cfg.changelog_sections]
        for title, commits in groups:
            if commits:
                print(f"\n### {title}\n")
                for c in commits:
                    print(f"- {f'{c.scope}: ' if c.scope else ''}{c.subject} ({c.label}, {c.author})")
        print()
    return 0


def cmd_hook(args) -> int:
    """Install or remove the pre-commit hook."""
    cfg = _config(args)
    try:
        if args.action == "install":
            print(f"installed {hooks.install_hook(cfg, sync=args.sync, force=args.force)}")
        else:
            print("removed pre-commit hook" if hooks.uninstall_hook(cfg) else "no docweave hook installed")
    except RuntimeError as exc:
        print(f"docweave: {exc}", file=sys.stderr)
        return 1
    return 0


def cmd_comms(args) -> int:
    """Export pull requests and issues from GitHub into the comms folder."""
    cfg = _config(args)
    try:
        for path in pull_github(cfg.root, cfg.root / cfg.comms_dir, limit=args.limit):
            print(f"wrote {path.relative_to(cfg.root).as_posix()}")
    except (RuntimeError, OSError) as exc:
        print(f"docweave: could not export from GitHub ({exc}). Is the `gh` CLI installed and logged in?", file=sys.stderr)
        return 1
    return 0


def cmd_watch(args) -> int:
    """Poll source and Markdown files and regenerate the docs whenever one changes."""
    cfg = _config(args)

    def snapshot() -> dict[str, float]:
        files = discover(cfg, tuple(ANALYZERS)) + [f for f in discover(cfg, (".md",), sources=["."]) if not f.startswith(cfg.out_dir + "/")]
        return {f: (cfg.root / f).stat().st_mtime for f in files if (cfg.root / f).exists()}

    print(f"watching {cfg.root} (Ctrl+C to stop)", flush=True)
    seen: dict[str, float] = {}
    cycles = getattr(args, "cycles", None)  # tests bound the loop; the command line never does
    try:
        while cycles is None or cycles > 0:
            now = snapshot()
            if now != seen:
                changed = sorted(set(now) ^ set(seen) | {f for f in now if f in seen and seen[f] != now[f]}) if seen else []
                print(time.strftime("[%H:%M:%S] ") + (f"changed: {', '.join(changed[:5])}" if changed else "initial build"), flush=True)
                _generate(args)
                sys.stdout.flush()
                seen = snapshot()
            cycles = None if cycles is None else cycles - 1
            if cycles != 0:
                time.sleep(args.interval)
    except KeyboardInterrupt:
        pass
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Define the command-line interface."""
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", default=".", help="project root (default: current directory)")
    common.add_argument("--no-git", action="store_true", help="ignore git history even if present")
    parser = argparse.ArgumentParser(prog="docweave", description="Living documentation from code structure and developer communication.")
    parser.add_argument("--version", action="version", version=f"docweave {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", parents=[common], help="create docweave.toml (and optionally CI / git hook)")
    p.add_argument("--ci", action="store_true", help="also write a GitHub Actions workflow")
    p.add_argument("--hook", action="store_true", help="also install the pre-commit hook")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("generate", parents=[common], help="analyse the project and (re)write the docs")
    p.add_argument("--out", help="output directory (default: docs)")
    p.add_argument("--llm", action="store_true", help="use Claude to summarise undocumented code")
    p.add_argument("--quiet", action="store_true")
    p.set_defaults(func=cmd_generate)

    p = sub.add_parser("check", parents=[common], help="report documentation drift; non-zero exit on failure")
    p.add_argument("--out", help="output directory (default: docs)")
    p.add_argument("--fail-on", choices=list(_RANK), help="lowest severity that fails the check")
    p.add_argument("--require-fresh", action="store_true", help="also fail if generated docs are out of date")
    p.add_argument("--staged", action="store_true", help="only fail on issues in files staged for commit")
    p.add_argument("--format", choices=["text", "json", "github"], default="text")
    p.add_argument("--quiet", action="store_true", help="print only failures")
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("why", parents=[common], help="show the history and reasoning behind a symbol")
    p.add_argument("symbol")
    p.add_argument("--limit", type=int, default=8)
    p.set_defaults(func=cmd_why)

    p = sub.add_parser("ask", parents=[common], help="search code and discussions with a question")
    p.add_argument("question")
    p.add_argument("--limit", type=int, default=5)
    p.add_argument("--llm", action="store_true", help="have Claude answer from the retrieved context")
    p.set_defaults(func=cmd_ask)

    p = sub.add_parser("changelog", parents=[common], help="print a changelog built from commit intent")
    p.set_defaults(func=cmd_changelog)

    p = sub.add_parser("hook", parents=[common], help="install or remove the git pre-commit hook")
    p.add_argument("action", choices=["install", "uninstall"])
    p.add_argument("--sync", action="store_true", help="regenerate and stage docs instead of blocking the commit")
    p.add_argument("--force", action="store_true", help="replace an existing pre-commit hook")
    p.set_defaults(func=cmd_hook)

    p = sub.add_parser("comms", parents=[common], help="export PRs and issues from GitHub into the comms folder")
    p.add_argument("action", choices=["pull"])
    p.add_argument("--limit", type=int, default=200)
    p.set_defaults(func=cmd_comms)

    p = sub.add_parser("watch", parents=[common], help="regenerate docs whenever source files change")
    p.add_argument("--out", help="output directory (default: docs)")
    p.add_argument("--interval", type=float, default=1.5)
    p.set_defaults(func=cmd_watch)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Entry point: parse arguments, run the command, return its exit code."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    args = build_parser().parse_args(argv)
    try:
        if not Path(args.root).is_dir():
            raise ValueError(f"{args.root} is not a directory")
        return args.func(args)
    except ValueError as exc:
        print(f"docweave: {exc}", file=sys.stderr)
        return 2
