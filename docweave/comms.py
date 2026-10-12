"""Load developer communication that lives outside git: PRs, issues, chat exports, notes.

Drop files into the configured ``comms_dir`` and they are picked up automatically:

* ``*.json`` - a GitHub export (``gh pr list --json ...`` / ``gh issue list --json ...``),
  a Slack channel export (a list of ``{"user", "text", "ts"}``), or generic message objects.
* ``*.jsonl`` - one generic message object per line.
* ``*.md`` / ``*.txt`` - meeting notes or ADRs; the first heading is the title.
"""

from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from .model import Message

_DATE_LINE = re.compile(r"^\W*date\W*[:=]\s*(\d{4}-\d{2}-\d{2})", re.I | re.M)
GH_FIELDS = "number,title,body,author,createdAt,url"


def _parse_date(value) -> datetime | None:
    if value in (None, ""):
        return None
    try:
        if isinstance(value, (int, float)) or re.fullmatch(r"\d+(\.\d+)?", str(value)):
            return datetime.fromtimestamp(float(value), tz=timezone.utc)
        d = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except (ValueError, OSError, OverflowError):
        return None


def _author(value) -> str:
    if isinstance(value, dict):
        return str(value.get("login") or value.get("name") or value.get("real_name") or "")
    return str(value or "")


def _from_object(obj: dict, stem: str, index: int) -> Message | None:
    if "number" in obj and "title" in obj:  # GitHub PR or issue
        kind = "pr" if ("mergedAt" in obj or "headRefName" in obj or "/pull/" in str(obj.get("url", "")) or "pr" in stem.lower() or "pull" in stem.lower()) else "issue"
        return Message(
            id=f"{kind}:{obj['number']}", source=kind, author=_author(obj.get("author")),
            date=_parse_date(obj.get("mergedAt") or obj.get("closedAt") or obj.get("createdAt")),
            title=str(obj["title"]), body=str(obj.get("body") or ""), url=obj.get("url"),
        )
    text = obj.get("text") or obj.get("body") or obj.get("message") or obj.get("content")
    if not isinstance(text, str) or not text.strip():
        return None
    stamp = obj.get("ts") or obj.get("date") or obj.get("timestamp") or obj.get("created_at")
    is_chat = "ts" in obj
    title = str(obj.get("title") or "")
    return Message(
        id=str(obj.get("id") or f"{'chat' if is_chat else 'note'}:{stem}:{stamp or index}"),
        source=str(obj.get("source") or ("chat" if is_chat else "note")),
        author=_author(obj.get("user_name") or obj.get("user") or obj.get("author")),
        date=_parse_date(stamp), title=title or f"#{stem}" if is_chat else title, body=text, url=obj.get("url"),
    )


def load_comms(directory: Path) -> list[Message]:
    """Read every supported file under ``directory`` into normalised messages."""
    messages: list[Message] = []
    if not directory.is_dir():
        return messages
    for path in sorted(directory.rglob("*")):
        suffix = path.suffix.lower()
        if not path.is_file() or suffix not in (".json", ".jsonl", ".md", ".txt"):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if suffix in (".md", ".txt"):
            lines = text.strip().splitlines()
            if not lines:
                continue
            date = _DATE_LINE.search(text)
            messages.append(
                Message(
                    id=f"note:{path.relative_to(directory).as_posix()}", source="note",
                    date=_parse_date(date[1]) if date else None,
                    title=lines[0].lstrip("# ").strip(), body="\n".join(lines[1:]).strip(),
                )
            )
            continue
        if suffix == ".jsonl":  # one object per line; a corrupt line costs only itself
            data = []
            for line in text.splitlines():
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        else:
            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                continue
        if isinstance(data, dict):
            data = data.get("messages") or data.get("items") or [data]
        for i, obj in enumerate(data if isinstance(data, list) else []):
            if isinstance(obj, dict) and (msg := _from_object(obj, path.stem, i)):
                messages.append(msg)
    return messages


def pull_github(root: Path, directory: Path, limit: int = 200) -> list[Path]:
    """Export merged PRs and issues with the ``gh`` CLI into ``directory`` (needs ``gh auth login``)."""
    directory.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for name, args in (
        ("github-prs.json", ["pr", "list", "--state", "merged", "--json", GH_FIELDS + ",mergedAt"]),
        ("github-issues.json", ["issue", "list", "--state", "all", "--json", GH_FIELDS + ",closedAt"]),
    ):
        proc = subprocess.run(["gh", *args, "--limit", str(limit)], cwd=root, capture_output=True, text=True, encoding="utf-8")
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr.strip() or "gh failed")
        (directory / name).write_text(proc.stdout, encoding="utf-8")
        written.append(directory / name)
    return written
