"""Classify what a piece of developer communication is *doing*: fixing, adding, refactoring...

Conventional-commit prefixes are trusted when present. Otherwise a weighted lexicon votes, with
the leading word of the subject counting most (commit subjects are usually imperative).
"""

from __future__ import annotations

import re

from .text import stem, tokenize

INTENTS = ("security", "fix", "feature", "perf", "deprecation", "refactor", "revert", "docs", "test", "style", "chore")

INTENT_TITLES = {
    "feature": "Features",
    "fix": "Fixes",
    "perf": "Performance",
    "security": "Security",
    "deprecation": "Deprecations",
    "refactor": "Refactoring",
    "revert": "Reverts",
    "docs": "Documentation",
    "test": "Tests",
    "style": "Style",
    "chore": "Maintenance",
    "other": "Other changes",
}

# How strongly a change of this kind is expected to invalidate existing documentation.
DOC_IMPACT = {
    "feature": 1.0, "fix": 1.0, "security": 1.0, "deprecation": 1.0, "revert": 1.0, "wip": 1.0,
    "other": 0.7, "perf": 0.6, "refactor": 0.5, "chore": 0.2, "docs": 0.1, "test": 0.1, "style": 0.05,
}

_CONVENTIONAL = re.compile(r"^(?P<type>[A-Za-z]+)(?:\((?P<scope>[^)]+)\))?(?P<bang>!)?:\s+(?P<subject>.+)$")
_CONVENTIONAL_TYPES = {
    "feat": "feature", "feature": "feature", "fix": "fix", "bugfix": "fix", "hotfix": "fix",
    "perf": "perf", "refactor": "refactor", "docs": "docs", "doc": "docs", "test": "test",
    "tests": "test", "style": "style", "chore": "chore", "build": "chore", "ci": "chore",
    "deps": "chore", "revert": "revert", "security": "security", "sec": "security",
    "deprecate": "deprecation",
}
_LEXICON_WORDS = {
    "security": "security vulnerability vulnerable cve xss csrf injection sanitize sanitise exploit leak secret harden",
    "fix": "fix bug crash error issue patch resolve correct regression broken fail failure wrong incorrect "
           "handle prevent avoid hotfix repair race deadlock overflow null none exception",
    "feature": "add implement support introduce new allow enable feature create provide expose",
    "perf": "perf performance speed fast faster optimize optimise cache latency memory slow quicker throughput",
    "deprecation": "deprecate deprecated deprecation obsolete sunset",
    "refactor": "refactor restructure cleanup clean simplify extract rename move reorganize reorganise "
                "dedupe deduplicate split consolidate inline tidy rework",
    "revert": "revert rollback undo",
    "docs": "doc docs documentation readme comment docstring typo changelog wording",
    "test": "test tests testing coverage fixture mock unittest pytest",
    "style": "format formatting lint linter whitespace style black prettier isort indent",
    "chore": "bump upgrade dependency dependencies deps ci build release version merge pin config tooling",
}
LEXICON = {intent: {stem(w) for w in words.split()} for intent, words in _LEXICON_WORDS.items()}
_BREAKING = re.compile(r"BREAKING[ -]CHANGE|\bbreaking\b|\bbackwards?[- ]incompatible\b", re.I)
_PR_SUFFIX = re.compile(r"\s*\(#\d+\)\s*$")


def classify(title: str, body: str = "") -> tuple[str, str | None, bool, float, str]:
    """Return ``(intent, scope, breaking, confidence, clean_subject)`` for a message."""
    title = title.strip()
    breaking = bool(_BREAKING.search(f"{title}\n{body}"))
    subject = _PR_SUFFIX.sub("", title)
    m = _CONVENTIONAL.match(subject)
    if m and m["type"].lower() in _CONVENTIONAL_TYPES:
        subject = m["subject"].strip()
        subject = subject[:1].upper() + subject[1:]
        return _CONVENTIONAL_TYPES[m["type"].lower()], m["scope"], breaking or bool(m["bang"]), 1.0, subject

    scores = dict.fromkeys(INTENTS, 0.0)
    for i, tok in enumerate(tokenize(title)):
        weight = 3.0 if i == 0 else 2.0
        for intent in INTENTS:
            if tok in LEXICON[intent]:
                scores[intent] += weight
    for tok in tokenize(body)[:80]:
        for intent in INTENTS:
            if tok in LEXICON[intent]:
                scores[intent] += 0.5
    best = max(INTENTS, key=lambda k: scores[k])  # ties resolve by INTENTS priority order
    subject = subject[:1].upper() + subject[1:]
    if scores[best] == 0:
        return "other", None, breaking, 0.0, subject
    return best, None, breaking, round(scores[best] / (sum(scores.values()) + 1.0), 2), subject
