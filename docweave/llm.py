"""Optional AI layer (``--llm``): Claude writes summaries for code nobody documented.

Everything else in DocWeave is deterministic and offline. This module is only imported when asked
for, needs ``pip install anthropic`` plus credentials (``ANTHROPIC_API_KEY`` or ``ant auth login``),
and caches results by code fingerprint so only symbols that actually changed are ever re-sent.
"""

from __future__ import annotations

import json
from typing import Callable

from .engine import Analysis
from .model import Symbol
from .nlp.rationale import rationale

BATCH = 20
# Models that accept the server-side refusal fallback (see the Anthropic "refusals and fallback" docs).
_FALLBACK_MODELS = {"claude-opus-5-5", "claude-opus-5", "claude-fable-5-1", "claude-sonnet-5-5"}
_SCHEMA = {
    "type": "object",
    "properties": {
        "summaries": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"id": {"type": "string"}, "summary": {"type": "string"}},
                "required": ["id", "summary"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["summaries"],
    "additionalProperties": False,
}
_SYSTEM = """You write reference documentation for a codebase. For each symbol you are given its \
source code and, when available, the commit messages and discussions linked to it.

Write one or two plain sentences per symbol: what it does, and - only when the history states it - \
why it exists or why it works the way it does. Describe behaviour a caller can rely on, not the \
implementation line by line. State only what the code or history supports; never guess at intent. \
Do not start with the symbol's name or "This function"."""


class LLMError(RuntimeError):
    """The AI layer could not be used; the message says what to do about it."""


def _client():
    try:
        import anthropic
    except ImportError as exc:
        raise LLMError("The --llm option needs the Anthropic SDK: pip install anthropic") from exc
    return anthropic, anthropic.Anthropic()


def _create(client, model: str, **kwargs):
    """Send one request, opting into the server-side refusal fallback where the model supports it."""
    if model in _FALLBACK_MODELS:
        return client.beta.messages.create(model=model, betas=["server-side-fallback-2026-07-01"], fallbacks="default", **kwargs)
    return client.messages.create(model=model, **kwargs)


def _call(anthropic, client, model: str, **kwargs):
    try:
        return _create(client, model, **kwargs)
    except anthropic.AuthenticationError as exc:
        raise LLMError("No valid Anthropic credentials: set ANTHROPIC_API_KEY or run `ant auth login`.") from exc
    except anthropic.NotFoundError as exc:
        raise LLMError(f"Model `{model}` was not found; check llm_model in docweave.toml.") from exc
    except anthropic.RateLimitError as exc:
        raise LLMError("Rate limited by the Anthropic API; summaries so far are cached, so just re-run later.") from exc
    except anthropic.APIStatusError as exc:
        raise LLMError(f"Anthropic API error {exc.status_code}: {exc.message}") from exc
    except anthropic.APIConnectionError as exc:
        raise LLMError("Could not reach the Anthropic API; check your network connection.") from exc


def _text(response) -> str | None:
    if response.stop_reason == "refusal":
        return None
    return next((block.text for block in response.content if block.type == "text"), None)


def _prompt(analysis: Analysis, symbols: list[Symbol], sources: dict[str, list[str]]) -> str:
    parts = []
    for sym in symbols:
        lines = sources[sym.file]
        code = "\n".join(lines[sym.lineno - 1 : sym.end_lineno])
        history = []
        for link in analysis.links.get(sym.id, [])[:4]:
            msg = analysis.messages[link.message_id]
            if msg.source != "worktree":
                why = " ".join(rationale(msg.title, msg.body))
                history.append(f"- [{msg.source}, {msg.day}] {msg.title}" + (f" - {why}" if why else ""))
        parts.append(f'<symbol id="{sym.id}" kind="{sym.kind}" file="{sym.file}">\n<code>\n{code}\n</code>\n'
                     + (f"<history>\n{chr(10).join(history)}\n</history>\n" if history else "") + "</symbol>")
    return "Summarise each of these symbols. Return one entry per symbol id.\n\n" + "\n\n".join(parts)


def summarize_undocumented(analysis: Analysis, progress: Callable[[str], None] = lambda _msg: None) -> dict[str, str]:
    """Return AI-written summaries for visible symbols that have no docstring, using the cache."""
    cfg = analysis.cfg
    cache_path = cfg.state_dir / "llm_cache.json"
    try:
        cache: dict[str, str] = json.loads(cache_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        cache = {}
    key = lambda s: f"{s.id}@{s.interface_hash}.{s.body_hash}"  # noqa: E731
    wanted = [s for s in analysis.project.symbols.values()
              if analysis.visible(s) and not (s.docstring or "").strip() and s.kind != "constant"]
    todo = [s for s in wanted if key(s) not in cache]
    if todo:
        anthropic, client = _client()
        sources = {f: (cfg.root / f).read_text(encoding="utf-8", errors="replace").split("\n") for f in {s.file for s in todo}}
        for start in range(0, len(todo), BATCH):
            batch = todo[start : start + BATCH]
            progress(f"summarising {start + 1}-{start + len(batch)} of {len(todo)} undocumented symbols")
            response = _call(
                anthropic, client, cfg.llm_model, max_tokens=16000, system=_SYSTEM,
                output_config={"effort": "low", "format": {"type": "json_schema", "schema": _SCHEMA}},
                messages=[{"role": "user", "content": _prompt(analysis, batch, sources)}],
            )
            text = _text(response)
            try:
                items = json.loads(text)["summaries"] if text else []
            except (ValueError, KeyError, TypeError):
                progress("a batch came back incomplete and was skipped; re-run to retry it")
                continue
            by_id = {s.id: s for s in batch}
            for item in items:
                if (sym := by_id.get(item.get("id"))) and item.get("summary", "").strip():
                    cache[key(sym)] = item["summary"].strip()
            cfg.state_dir.mkdir(exist_ok=True)
            cache_path.write_text(json.dumps(cache, indent=1, sort_keys=True), encoding="utf-8")
    return {s.id: cache[key(s)] for s in wanted if key(s) in cache}


def answer(analysis: Analysis, question: str, context: str) -> str:
    """Answer a question about the codebase from retrieved symbols and discussions."""
    anthropic, client = _client()
    response = _call(
        anthropic, client, analysis.cfg.llm_model, max_tokens=16000,
        output_config={"effort": "medium"},
        system="Answer questions about a codebase using only the retrieved context you are given. "
               "Cite the file:line or commit you rely on. If the context does not answer the question, say so.",
        messages=[{"role": "user", "content": f"<context>\n{context}\n</context>\n\nQuestion: {question}"}],
    )
    return _text(response) or "The model declined to answer this question."
