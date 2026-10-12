<!-- docweave:begin module -->
# `docweave.nlp.index`

A small inverted index offering BM25 ranking and TF-IDF cosine similarity.

Source: [`docweave/nlp/index.py`](../../docweave/nlp/index.py) · 63 lines · main authors: AashutoshR (100%)

**Imported by:** [`docweave.linker`](docweave.linker.md), [`docweave.search`](docweave.search.md)
<!-- docweave:end module -->

<!-- docweave:begin contents -->
## Contents

| Symbol | Kind | Summary |
| --- | --- | --- |
| [`TextIndex`](#textindex) | class | An in-memory inverted index over tokenised documents. |
| [`TextIndex.add`](#textindex-add) | method | Add a document; call :meth:`finalize` once all documents are in. |
| [`TextIndex.finalize`](#textindex-finalize) | method | Compute IDF weights and document norms. |
| [`TextIndex.bm25`](#textindex-bm25) | method | Rank documents against ``query`` with Okapi BM25; returns the top ``k`` as ``(id, score)``. |
| [`TextIndex.cosine`](#textindex-cosine) | method | TF-IDF cosine similarity of ``query`` to each document, optionally only those in ``restrict``. |

## Reference
<!-- docweave:end contents -->

<!-- docweave:begin sym:TextIndex -->
<a id="textindex"></a>
### `TextIndex` <sup>class</sup>

```python
class TextIndex
```

An in-memory inverted index over tokenised documents.

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/nlp/index.py:9`](../../docweave/nlp/index.py#L9) · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:TextIndex -->

<!-- docweave:begin sym:TextIndex.add -->
<a id="textindex-add"></a>
#### `TextIndex.add` <sup>method</sup>

```python
def add(self, doc_id: str, tokens: list[str]) -> None
```

Add a document; call :meth:`finalize` once all documents are in.

| Parameter | Type |
| --- | --- |
| `doc_id` | `str` |
| `tokens` | `list[str]` |

**Returns:** `None`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/nlp/index.py:20`](../../docweave/nlp/index.py#L20) · complexity 2 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:TextIndex.add -->

<!-- docweave:begin sym:TextIndex.finalize -->
<a id="textindex-finalize"></a>
#### `TextIndex.finalize` <sup>method</sup>

```python
def finalize(self) -> 'TextIndex'
```

Compute IDF weights and document norms. Must be called before querying.

**Returns:** `'TextIndex'`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/nlp/index.py:29`](../../docweave/nlp/index.py#L29) · complexity 7 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:TextIndex.finalize -->

<!-- docweave:begin sym:TextIndex.bm25 -->
<a id="textindex-bm25"></a>
#### `TextIndex.bm25` <sup>method</sup>

```python
def bm25(self, query: list[str], k: int=10, k1: float=1.4, b: float=0.75) -> list[tuple[str, float]]
```

Rank documents against ``query`` with Okapi BM25; returns the top ``k`` as ``(id, score)``.

| Parameter | Type | Default |
| --- | --- | --- |
| `query` | `list[str]` |  |
| `k` | `int` | `10` |
| `k1` | `float` | `1.4` |
| `b` | `float` | `0.75` |

**Returns:** `list[tuple[str, float]]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/nlp/index.py:39`](../../docweave/nlp/index.py#L39) · complexity 4 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:TextIndex.bm25 -->

<!-- docweave:begin sym:TextIndex.cosine -->
<a id="textindex-cosine"></a>
#### `TextIndex.cosine` <sup>method</sup>

```python
def cosine(self, query: list[str], restrict: set[str] | None=None, k: int=5) -> list[tuple[str, float]]
```

TF-IDF cosine similarity of ``query`` to each document, optionally only those in ``restrict``.

| Parameter | Type | Default |
| --- | --- | --- |
| `query` | `list[str]` |  |
| `restrict` | `set[str] \| None` | `None` |
| `k` | `int` | `5` |

**Returns:** `list[tuple[str, float]]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/nlp/index.py:50`](../../docweave/nlp/index.py#L50) · complexity 11 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:TextIndex.cosine -->
