"""Mine the *why* out of developer communication.

Code says what happens; commit bodies, PR threads and chat say why. These heuristics find the
sentences that carry intent ("because", "to avoid", "instead of", "we decided") so they can be
attached to the code they explain.
"""

from __future__ import annotations

import re

from .text import sentences

_MARKERS: list[tuple[re.Pattern, float]] = [
    (re.compile(p, re.I), w)
    for p, w in [
        (r"\bbecause\b", 2.0),
        (r"\bso that\b", 2.0),
        (r"\bin order to\b", 2.0),
        (r"\bdue to\b", 1.5),
        (r"\binstead of\b", 2.0),
        (r"\brather than\b", 2.0),
        (r"\bwork(?:s|ed|ing)?[- ]?around\b", 2.0),
        (r"\bto (?:avoid|prevent|ensure|allow|support|keep|reduce|stop|make sure|guard)\b", 1.5),
        (r"\botherwise\b", 1.5),
        (r"\bsince\b", 0.75),
        (r"\bwhich (?:caused|causes|means|meant|led|leads|broke|breaks)\b", 1.5),
        (r"\bthe reason\b|\breason (?:is|was|for|being)\b", 1.5),
        (r",\s+so\b", 1.0),
        (r"\btrade-?offs?\b", 2.0),
        (r"\bwe (?:decided|chose|agreed|settled|opted)\b|\bdecision\b", 2.5),
        (r"\b(?:caused|causing|led to|resulted in)\b", 1.0),
        (r"\b(?:no longer|used to|previously|until now)\b", 1.0),
        (r"\b(?:must|should|need(?:s|ed)? to)\b", 0.5),
    ]
]
_DECISION = re.compile(
    r"\bwe (?:decided|chose|agreed|settled|opted)\b|\bdecision\b|\btrade-?offs?\b|\binstead of\b|\brather than\b"
    r"|\bdeprecat|\bBREAKING\b|\bgoing forward\b|\bfrom now on\b",
    re.I,
)
_NOISE = re.compile(r"^(?:signed-off-by|co-authored-by|change-id|reviewed-by|cc|refs?)\b", re.I)


def score_sentence(sentence: str) -> float:
    """How strongly a sentence reads as an explanation rather than a description."""
    if _NOISE.match(sentence):
        return 0.0
    return sum(weight for pattern, weight in _MARKERS if pattern.search(sentence))


def rationale(title: str, body: str, limit: int = 2) -> list[str]:
    """Return up to ``limit`` sentences from a message that best explain why a change was made.

    The body is where people explain themselves; the title is only mined when there is no body.
    """
    scored = [(score_sentence(s), -i, s) for i, s in enumerate(sentences(body) or sentences(title))]
    best = sorted((t for t in scored if t[0] >= 1.0), reverse=True)[:limit]
    return [s for _score, _i, s in sorted(best, key=lambda t: -t[1])]


def decision_score(title: str, body: str) -> float:
    """Score a message as a design decision worth recording in the decision log."""
    text = f"{title}\n{body}"
    explained = sum(sorted((score_sentence(s) for s in sentences(text)), reverse=True)[:2])
    return explained + (2.0 if _DECISION.search(text) else 0.0)
