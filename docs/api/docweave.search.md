<!-- docweave:begin module -->
# `docweave.search`

Ask questions of the codebase: BM25 retrieval over symbols and the communication linked to them.

Source: [`docweave/search.py`](../../docweave/search.py) · 55 lines

**Imports:** [`docweave.engine`](docweave.engine.md), [`docweave.nlp.docstring`](docweave.nlp.docstring.md), [`docweave.nlp.index`](docweave.nlp.index.md), [`docweave.nlp.rationale`](docweave.nlp.rationale.md), [`docweave.nlp.text`](docweave.nlp.text.md)

**Imported by:** [`docweave.cli`](docweave.cli.md)
<!-- docweave:end module -->

<!-- docweave:begin contents -->
## Contents

| Symbol | Kind | Summary |
| --- | --- | --- |
| [`Hit`](#hit) | class | One search result. |
| [`search`](#search) | function | Rank symbols and messages against a natural-language question. |

## Reference
<!-- docweave:end contents -->

<!-- docweave:begin sym:Hit -->
<a id="hit"></a>
### `Hit` <sup>class</sup>

```python
@dataclass
class Hit
```

One search result.

<sub>[`docweave/search.py:15`](../../docweave/search.py#L15)</sub>
<!-- docweave:end sym:Hit -->

<!-- docweave:begin sym:search -->
<a id="search"></a>
### `search` <sup>function</sup>

```python
def search(analysis: Analysis, question: str, k: int=5) -> list[Hit]
```

Rank symbols and messages against a natural-language question.

A symbol is indexed together with the commits and discussions linked to it, so a question
phrased in the team's words ("rate limit workaround") finds code that never uses those words.

| Parameter | Type | Default |
| --- | --- | --- |
| `analysis` | `Analysis` |  |
| `question` | `str` |  |
| `k` | `int` | `5` |

**Returns:** `list[Hit]`

<sub>[`docweave/search.py:26`](../../docweave/search.py#L26) · complexity 13</sub>
<!-- docweave:end sym:search -->
