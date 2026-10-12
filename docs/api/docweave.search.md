<!-- docweave:begin module -->
# `docweave.search`

Ask questions of the codebase: BM25 retrieval over symbols and the communication linked to them.

Source: [`docweave/search.py`](../../docweave/search.py) · 55 lines · main authors: AashutoshR (100%)

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

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/search.py:15`](../../docweave/search.py#L15) · written by AashutoshR (100%)</sub>
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

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/search.py:26`](../../docweave/search.py#L26) · complexity 13 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:search -->
