"""Managed regions: let generated and hand-written text share a file without clobbering.

Generated content is wrapped in ``<!-- docweave:begin ID -->`` / ``<!-- docweave:end ID -->``
markers. Regenerating rewrites only what is between markers; everything a person wrote outside
them survives. Blocks for code that no longer exists are removed; new blocks are slotted in after
their natural predecessor.
"""

from __future__ import annotations

import re

# Markers only count when they stand on their own line, so prose that merely mentions them is safe.
_REGION = re.compile(
    r"^<!-- docweave:begin (?P<id>[^\s>]+) -->[ \t]*\n(?P<body>.*?)^<!-- docweave:end (?P=id) -->[ \t]*$",
    re.S | re.M,
)


def wrap(block_id: str, body: str) -> str:
    """Wrap ``body`` in the begin/end markers for ``block_id``."""
    return f"<!-- docweave:begin {block_id} -->\n{body.strip()}\n<!-- docweave:end {block_id} -->"


def region_ids(text: str) -> list[str]:
    """Ids of the managed regions present in ``text``, in order."""
    return [m["id"] for m in _REGION.finditer(text)]


def strip_regions(text: str) -> str:
    """What remains of a file once every managed region is removed (the hand-written part)."""
    return _REGION.sub("", text)


def merge(existing: str | None, blocks: list[tuple[str, str]], inject_only: bool = False) -> str:
    """Merge freshly generated ``blocks`` into ``existing`` text.

    With ``inject_only`` (used for files people own, like the README) nothing is added or removed:
    only regions already present in the file are refreshed.
    """
    fresh = dict(blocks)
    if existing is None:
        return "\n\n".join(wrap(i, b) for i, b in blocks) + "\n"

    segments: list[tuple[str, str]] = []  # ("text", raw) | (block_id, rendered region)
    pos = 0
    for m in _REGION.finditer(existing):
        segments.append(("text", existing[pos : m.start()]))
        if m["id"] in fresh:
            segments.append((m["id"], wrap(m["id"], fresh[m["id"]])))
        elif inject_only:
            segments.append((m["id"], m.group(0)))
        pos = m.end()
    segments.append(("text", existing[pos:]))

    if not inject_only:
        present = {kind for kind, _ in segments if kind != "text"}
        previous: str | None = None
        for block_id, body in blocks:
            if block_id not in present:
                region = (block_id, wrap(block_id, body))
                if previous is None:
                    segments[0:0] = [region, ("text", "\n\n")]
                else:  # the predecessor is always present: it either existed or was just inserted
                    at = next(i for i, (kind, _) in enumerate(segments) if kind == previous)
                    segments[at + 1 : at + 1] = [("text", "\n\n"), region]
                present.add(block_id)
            previous = block_id

    text = "".join(raw for _, raw in segments)
    return re.sub(r"\n{3,}", "\n\n", text).strip("\n") + "\n"
