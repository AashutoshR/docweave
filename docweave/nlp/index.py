"""A small inverted index offering BM25 ranking and TF-IDF cosine similarity."""

from __future__ import annotations

import math
from collections import Counter


class TextIndex:
    """An in-memory inverted index over tokenised documents."""

    def __init__(self) -> None:
        self.ids: list[str] = []
        self._tf: list[Counter] = []
        self._postings: dict[str, dict[int, int]] = {}
        self._idf: dict[str, float] = {}
        self._norm: list[float] = []
        self._avg_len = 1.0

    def add(self, doc_id: str, tokens: list[str]) -> None:
        """Add a document; call :meth:`finalize` once all documents are in."""
        idx = len(self.ids)
        self.ids.append(doc_id)
        tf = Counter(tokens)
        self._tf.append(tf)
        for term, count in tf.items():
            self._postings.setdefault(term, {})[idx] = count

    def finalize(self) -> "TextIndex":
        """Compute IDF weights and document norms. Must be called before querying."""
        n = len(self.ids)
        self._idf = {t: math.log(1 + (n - len(p) + 0.5) / (len(p) + 0.5)) for t, p in self._postings.items()}
        self._norm = [
            math.sqrt(sum((c * self._idf[t]) ** 2 for t, c in tf.items())) or 1.0 for tf in self._tf
        ]
        self._avg_len = (sum(sum(tf.values()) for tf in self._tf) / n) if n else 1.0
        return self

    def bm25(self, query: list[str], k: int = 10, k1: float = 1.4, b: float = 0.75) -> list[tuple[str, float]]:
        """Rank documents against ``query`` with Okapi BM25; returns the top ``k`` as ``(id, score)``."""
        scores: dict[int, float] = {}
        for term in set(query):
            for idx, tf in self._postings.get(term, {}).items():
                length = sum(self._tf[idx].values())
                gain = tf * (k1 + 1) / (tf + k1 * (1 - b + b * length / self._avg_len))
                scores[idx] = scores.get(idx, 0.0) + self._idf[term] * gain
        top = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))[:k]
        return [(self.ids[i], round(s, 4)) for i, s in top]

    def cosine(self, query: list[str], restrict: set[str] | None = None, k: int = 5) -> list[tuple[str, float]]:
        """TF-IDF cosine similarity of ``query`` to each document, optionally only those in ``restrict``."""
        q = Counter(t for t in query if t in self._idf)
        q_norm = math.sqrt(sum((c * self._idf[t]) ** 2 for t, c in q.items()))
        if not q_norm:
            return []
        dots: dict[int, float] = {}
        for term, qc in q.items():
            for idx, tf in self._postings[term].items():
                if restrict is None or self.ids[idx] in restrict:
                    dots[idx] = dots.get(idx, 0.0) + qc * tf * self._idf[term] ** 2
        top = sorted(((d / (q_norm * self._norm[i]), i) for i, d in dots.items()), reverse=True)[:k]
        return [(self.ids[i], round(s, 4)) for s, i in top]
