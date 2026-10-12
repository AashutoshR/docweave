"""Parse docstrings (Google, NumPy, Sphinx and JSDoc styles) into structured claims.

The point is not pretty rendering: it is to recover what the documentation *claims* about a
function (its parameters, return value and exceptions) so those claims can be checked against
what static analysis says the code actually does.
"""

from __future__ import annotations

import inspect
import re
from dataclasses import dataclass, field

from .text import first_sentence

PARAM_HEADS = {"args", "arguments", "parameters", "params", "keyword args", "keyword arguments", "other parameters"}
RETURN_HEADS = {"returns", "return", "yields", "yield"}
RAISE_HEADS = {"raises", "raise", "throws"}
OTHER_HEADS = {
    "example", "examples", "note", "notes", "attributes", "see also", "warning", "warnings",
    "references", "todo", "usage", "methods",
}
ALL_HEADS = PARAM_HEADS | RETURN_HEADS | RAISE_HEADS | OTHER_HEADS

_ENTRY = re.compile(
    r"^(?P<names>\*{0,2}[A-Za-z_][\w.]*(?:\s*,\s*\*{0,2}[A-Za-z_][\w.]*)*)\s*"
    r"(?:\((?P<gtype>[^)]*)\))?\s*(?P<colon>:\s*(?P<rest>.*))?$"
)
_UNDERLINE = re.compile(r"\s*[-=]{3,}\s*$")
_SPHINX_PARAM = re.compile(r"^:(?:param|parameter|arg|argument|keyword|kwarg)\s+(?:[^:]*?\s)?\*{0,2}(?P<name>\w+):\s*(?P<desc>.*)$")
_SPHINX_RETURN = re.compile(r"^:(?:returns?|rtype):\s*(?P<desc>.*)$")
_SPHINX_RAISE = re.compile(r"^:(?:raises?|except|exception)\s+(?P<name>[\w.]+):\s*(?P<desc>.*)$")
_SPHINX_OTHER = re.compile(r"^:(?:type|vartype|ivar|cvar|var|meta)\b[^:]*:")
_JSDOC_PARAM = re.compile(r"^@(?:param|arg|argument)\s+(?:\{(?P<type>[^}]*)\}\s*)?(?P<name>\[?[\w$.]+(?:\s*=[^\]]*)?\]?)\s*-?\s*(?P<desc>.*)$")
_JSDOC_RETURN = re.compile(r"^@returns?\b\s*(?:\{(?P<type>[^}]*)\}\s*)?-?\s*(?P<desc>.*)$")
_JSDOC_RAISE = re.compile(r"^@(?:throws|exception)\b\s*(?:\{(?P<name>[^}]*)\}\s*)?-?\s*(?P<desc>.*)$")
_JSDOC_OTHER = re.compile(r"^@\w+")


@dataclass
class DocInfo:
    """The claims a docstring makes, in structured form."""

    summary: str = ""
    description: str = ""
    params: dict[str, str] = field(default_factory=dict)
    param_types: dict[str, str] = field(default_factory=dict)
    returns: str | None = None
    raises: dict[str, str] = field(default_factory=dict)


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip())


def _entries(content: list[str], numpy: bool) -> list[tuple[list[str], str, str]]:
    """Parse the body of an Args/Raises section into ``(names, type, description)`` entries."""
    body = [ln for ln in content if ln.strip()]
    if not body:
        return []
    base = min(_indent(ln) for ln in body)
    entries: list[list] = []
    for line in body:
        m = _ENTRY.match(line.strip()) if _indent(line) == base else None
        if m and (numpy or m["colon"]):
            names = [n.strip().lstrip("*") for n in m["names"].split(",")]
            rest = (m["rest"] or "").strip()
            entries.append([names, rest if numpy else (m["gtype"] or ""), "" if numpy else rest])
        elif entries:
            entries[-1][2] = f"{entries[-1][2]} {line.strip()}".strip()
    return [(e[0], e[1], e[2]) for e in entries]


def _flatten_jsdoc_type(line: str) -> str:
    """Hide braces nested inside a JSDoc ``{type}`` so a simple pattern can match the tag.

    ``@param {Array<{id: number}>} xs`` has braces within the type; they are swapped for
    placeholder characters here and restored by :func:`_restore_type`.
    """
    if not line.startswith("@") or "{" not in line:
        return line
    start = line.index("{")
    depth = 0
    for i in range(start, len(line)):
        depth += {"{": 1, "}": -1}.get(line[i], 0)
        if depth == 0:
            inner = line[start + 1 : i].replace("{", "\x01").replace("}", "\x02")
            return f"{line[:start]}{{{inner}}}{line[i + 1:]}"
    return line


def _restore_type(text: str) -> str:
    return text.replace("\x01", "{").replace("\x02", "}")


def parse_docstring(text: str | None) -> DocInfo:
    """Parse a docstring of any supported style into a :class:`DocInfo`."""
    info = DocInfo()
    if not text or not text.strip():
        return info
    lines = inspect.cleandoc(text).split("\n")
    description: list[str] = []
    sections: list[tuple[str, bool, list[str]]] = []
    current: tuple[str, bool, list[str]] | None = None
    head_indent = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        key = stripped.rstrip(":").lower()
        numpy = key in ALL_HEADS and i + 1 < len(lines) and bool(_UNDERLINE.match(lines[i + 1]))
        google = stripped.endswith(":") and key in ALL_HEADS
        if numpy or google:
            current = (key, numpy, [])
            sections.append(current)
            head_indent = _indent(line)
            i += 2 if numpy else 1
            continue
        if current is not None and not current[1] and stripped and _indent(line) <= head_indent:
            current = None  # a dedented line ends a Google-style section
        (current[2] if current is not None else description).append(line)
        i += 1

    for key, numpy, content in sections:
        if key in PARAM_HEADS:
            for names, typ, desc in _entries(content, numpy):
                for name in names:
                    info.params[name] = desc
                    if typ:
                        info.param_types[name] = typ
        elif key in RAISE_HEADS:
            for names, _typ, desc in _entries(content, numpy):
                for name in names:
                    info.raises[name.split(".")[-1]] = desc
        elif key in RETURN_HEADS:
            info.returns = " ".join(ln.strip() for ln in content if ln.strip()) or "(documented)"

    # Field-list styles (Sphinx ":param x:" and JSDoc "@param x") live in the description lines.
    prose: list[str] = []
    target: tuple[dict, str] | None = None
    in_field = False
    for line in description:
        s = _flatten_jsdoc_type(line.strip())
        if m := _SPHINX_PARAM.match(s) or _JSDOC_PARAM.match(s):
            name = re.sub(r"\s*=.*$", "", m["name"].strip("[]"))
            in_field, target = True, None
            if "." not in name:  # "opts.field" documents a property of an already-documented param
                info.params[name] = m["desc"].strip()
                target = (info.params, name)
                if m.groupdict().get("type"):
                    info.param_types[name] = _restore_type(m["type"])
        elif m := _SPHINX_RAISE.match(s) or _JSDOC_RAISE.match(s):
            name = (m["name"] or "Error").split(".")[-1]
            info.raises[name] = m["desc"].strip()
            in_field, target = True, (info.raises, name)
        elif m := _SPHINX_RETURN.match(s) or _JSDOC_RETURN.match(s):
            typ = _restore_type(m.groupdict().get("type") or "")
            info.returns = f"{info.returns or ''} {m['desc'].strip() or typ}".strip() or "(documented)"
            in_field, target = True, None
        elif _SPHINX_OTHER.match(s) or _JSDOC_OTHER.match(s):
            in_field, target = True, None
        elif in_field and s and line[:1] in " \t":
            if target:
                target[0][target[1]] = f"{target[0][target[1]]} {s}".strip()
        else:
            in_field = False
            prose.append(line)
    info.description = "\n".join(prose).strip()
    info.summary = first_sentence(info.description.split("\n\n")[0]) if info.description else ""
    return info
