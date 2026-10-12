<!-- docweave:begin module -->
# `docweave.llm`

Optional AI layer (``--llm``): Claude writes summaries for code nobody documented.

Everything else in DocWeave is deterministic and offline. This module is only imported when asked
for, needs ``pip install anthropic`` plus credentials (``ANTHROPIC_API_KEY`` or ``ant auth login``),
and caches results by code fingerprint so only symbols that actually changed are ever re-sent.

Source: [`docweave/llm.py`](../../docweave/llm.py) · 150 lines

**Imports:** [`docweave.engine`](docweave.engine.md), [`docweave.model`](docweave.model.md), [`docweave.nlp.rationale`](docweave.nlp.rationale.md)

**Imported by:** [`docweave.cli`](docweave.cli.md)
<!-- docweave:end module -->

<!-- docweave:begin contents -->
## Contents

| Symbol | Kind | Summary |
| --- | --- | --- |
| [`BATCH`](#batch) | constant | Batch setting. |
| [`LLMError`](#llmerror) | class | The AI layer could not be used; the message says what to do about it. |
| [`summarize_undocumented`](#summarize-undocumented) | function | Return AI-written summaries for visible symbols that have no docstring, using the cache. |
| [`answer`](#answer) | function | Answer a question about the codebase from retrieved symbols and discussions. |

## Reference
<!-- docweave:end contents -->

<!-- docweave:begin sym:BATCH -->
<a id="batch"></a>
### `BATCH` <sup>constant</sup>

```python
BATCH = 20
```

Batch setting.

*No docstring in the source - this description is inferred from the name.*

<sub>[`docweave/llm.py:17`](../../docweave/llm.py#L17)</sub>
<!-- docweave:end sym:BATCH -->

<!-- docweave:begin sym:LLMError -->
<a id="llmerror"></a>
### `LLMError` <sup>class</sup>

```python
class LLMError(RuntimeError)
```

The AI layer could not be used; the message says what to do about it.

<sub>[`docweave/llm.py:45`](../../docweave/llm.py#L45)</sub>
<!-- docweave:end sym:LLMError -->

<!-- docweave:begin sym:summarize_undocumented -->
<a id="summarize-undocumented"></a>
### `summarize_undocumented` <sup>function</sup>

```python
def summarize_undocumented(analysis: Analysis, progress: Callable[[str], None]=lambda _msg: None) -> dict[str, str]
```

Return AI-written summaries for visible symbols that have no docstring, using the cache.

| Parameter | Type | Default |
| --- | --- | --- |
| `analysis` | `Analysis` |  |
| `progress` | `Callable[[str], None]` | `lambda _msg: None` |

**Returns:** `dict[str, str]`

<sub>[`docweave/llm.py:101`](../../docweave/llm.py#L101) · complexity 21</sub>
<!-- docweave:end sym:summarize_undocumented -->

<!-- docweave:begin sym:answer -->
<a id="answer"></a>
### `answer` <sup>function</sup>

```python
def answer(analysis: Analysis, question: str, context: str) -> str
```

Answer a question about the codebase from retrieved symbols and discussions.

| Parameter | Type |
| --- | --- |
| `analysis` | `Analysis` |
| `question` | `str` |
| `context` | `str` |

**Returns:** `str`

<sub>[`docweave/llm.py:139`](../../docweave/llm.py#L139) · complexity 2</sub>
<!-- docweave:end sym:answer -->
