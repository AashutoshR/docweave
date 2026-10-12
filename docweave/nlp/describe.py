"""Synthesise a one-line description for symbols nobody documented.

Well-named code already half-documents itself; this turns ``get_user_by_id`` into
"Return user by id." Output is always labelled as inferred so it is never mistaken for
something a human wrote.
"""

from __future__ import annotations

from .text import split_identifier

_VERBS = {
    "get": "Return", "fetch": "Fetch", "load": "Load", "read": "Read", "find": "Find", "list": "List",
    "is": "Check whether", "has": "Check whether it has", "can": "Check whether it can",
    "should": "Decide whether it should", "set": "Set", "update": "Update", "add": "Add",
    "remove": "Remove", "delete": "Delete", "create": "Create", "make": "Create", "build": "Build",
    "parse": "Parse", "render": "Render", "write": "Write", "save": "Save", "send": "Send",
    "validate": "Validate", "check": "Check", "compute": "Compute", "calc": "Calculate",
    "calculate": "Calculate", "convert": "Convert", "to": "Convert to", "from": "Create from",
    "handle": "Handle", "on": "Handle", "run": "Run", "start": "Start", "stop": "Stop",
    "init": "Initialise", "apply": "Apply", "format": "Format", "extract": "Extract",
    "merge": "Merge", "open": "Open", "close": "Close", "ensure": "Ensure", "resolve": "Resolve",
    "detect": "Detect", "scan": "Scan", "collect": "Collect", "classify": "Classify",
    "generate": "Generate", "analyze": "Analyse", "analyse": "Analyse", "install": "Install",
}


def describe(name: str, kind: str) -> str:
    """Return an inferred one-line description for a symbol called ``name``."""
    words = split_identifier(name.strip("_"))
    if not words:
        return ""
    if kind == "class":
        return " ".join(words).capitalize() + "."
    if kind == "constant":
        return " ".join(words).capitalize() + " setting."
    head, rest = words[0], words[1:]
    if name == "__init__":
        return "Initialise the instance."
    if head in _VERBS:
        return " ".join([_VERBS[head], *rest]).strip() + "."
    return " ".join(words).capitalize() + "."
