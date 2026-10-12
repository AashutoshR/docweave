"""Tokenising, identifier splitting, light stemming and sentence segmentation."""

from __future__ import annotations

import re

STOPWORDS = frozenset(
    """a an the and or but if then else of to in on at by for from with without into onto over under as is
    are was were be been being it its this that these those there here we you they he she i our your their
    not no do does did done can could should would will shall may might must have has had having so than
    too very just also only when while where which who whom what how why all any each some such via per
    about after before again more most other out up down off own same s t don now get got""".split()
)

_WORD = re.compile(r"[A-Za-z][A-Za-z0-9_]*")
_HUMPS = re.compile(r"[A-Z]+(?=[A-Z][a-z])|[A-Z]?[a-z]+|[A-Z]+|\d+")
_SUFFIXES = (("ies", "y"), ("sses", "ss"), ("ing", ""), ("edly", ""), ("ed", ""), ("es", ""), ("s", ""), ("ly", ""))


def split_identifier(name: str) -> list[str]:
    """Split ``snake_case`` / ``camelCase`` / ``HTTPServer`` into lowercase words."""
    words: list[str] = []
    for part in re.split(r"[^A-Za-z0-9]+", name):
        words += _HUMPS.findall(part)
    return [w.lower() for w in words if w]


def stem(word: str) -> str:
    """A deliberately small suffix stripper; it only has to be consistent, not linguistically right."""
    w = word
    if len(w) <= 3:
        return w
    for suffix, repl in _SUFFIXES:
        if w.endswith(suffix) and len(w) - len(suffix) >= 3 and not (suffix == "s" and w.endswith("ss")):
            w = w[: -len(suffix)] + repl
            break
    if len(w) > 4 and w.endswith("e"):
        w = w[:-1]
    if len(w) > 3 and w[-1] == w[-2] and w[-1] not in "lsz":
        w = w[:-1]
    return w


def tokenize(text: str, *, keep_stopwords: bool = False) -> list[str]:
    """Lowercased, identifier-split, stemmed tokens suitable for retrieval and classification."""
    out: list[str] = []
    for raw in _WORD.findall(text):
        for word in split_identifier(raw):
            if len(word) < 2 or (not keep_stopwords and word in STOPWORDS):
                continue
            out.append(stem(word))
    return out


_BULLET = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
_SENT_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z`\"'(\[])")


def sentences(text: str) -> list[str]:
    """Split prose (commit bodies, chat, PR descriptions) into sentences; bullets count as sentences."""
    chunks: list[str] = []
    buf: list[str] = []

    def flush() -> None:
        if buf:
            chunks.append(" ".join(buf))
            buf.clear()

    for line in text.replace("\r", "").split("\n"):
        if not line.strip():
            flush()
        elif _BULLET.match(line):
            flush()
            buf.append(_BULLET.sub("", line).strip())
        else:
            buf.append(line.strip())
    flush()
    out: list[str] = []
    for chunk in chunks:
        out += [s.strip() for s in _SENT_END.split(chunk) if s.strip()]
    return out


def first_sentence(text: str) -> str:
    """The first sentence of ``text``, or an empty string."""
    parts = sentences(text)
    return parts[0] if parts else ""
