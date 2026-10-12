"""Ask questions of the codebase: BM25 retrieval over symbols and the communication linked to them."""

from __future__ import annotations

from dataclasses import dataclass

from .engine import Analysis
from .nlp.docstring import parse_docstring
from .nlp.index import TextIndex
from .nlp.rationale import rationale
from .nlp.text import tokenize


@dataclass
class Hit:
    """One search result."""

    id: str
    kind: str
    title: str
    location: str
    snippet: str
    score: float


def search(analysis: Analysis, question: str, k: int = 5) -> list[Hit]:
    """Rank symbols and messages against a natural-language question.

    A symbol is indexed together with the commits and discussions linked to it, so a question
    phrased in the team's words ("rate limit workaround") finds code that never uses those words.
    """
    index = TextIndex()
    docs: dict[str, Hit] = {}
    for sym in analysis.project.symbols.values():
        linked = [analysis.messages[l.message_id] for l in analysis.links.get(sym.id, [])[:6]]
        tokens = tokenize(sym.qualname) * 4 + tokenize(sym.signature) + tokenize(sym.docstring or "")
        for msg in linked:
            tokens += tokenize(msg.text)
        why = next((r[0] for m in linked if (r := rationale(m.title, m.body, 1))), "")
        summary = parse_docstring(sym.docstring).summary or sym.signature
        index.add(sym.id, tokens)
        docs[sym.id] = Hit(sym.id, sym.kind, sym.qualname, f"{sym.file}:{sym.lineno}", summary + (f"\n  why: {why}" if why else ""), 0.0)
    for msg in analysis.messages.values():
        if msg.source == "worktree":
            continue
        index.add(msg.id, tokenize(msg.text))
        docs[msg.id] = Hit(msg.id, msg.source, msg.subject or msg.title, f"{msg.day} {msg.label} {msg.author}".strip(), " ".join(msg.body.split())[:200], 0.0)
    index.finalize()
    hits = []
    for doc_id, score in index.bm25(tokenize(question), k=k):
        hit = docs[doc_id]
        hit.score = score
        hits.append(hit)
    return hits
