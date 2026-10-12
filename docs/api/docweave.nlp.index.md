<!-- docweave:begin module -->
# `docweave.nlp.index`

A small inverted index offering BM25 ranking and TF-IDF cosine similarity.

Source: [`docweave/nlp/index.py`](../../docweave/nlp/index.py) · 63 lines

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

<sub>[`docweave/nlp/index.py:9`](../../docweave/nlp/index.py#L9)</sub>
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

<sub>[`docweave/nlp/index.py:20`](../../docweave/nlp/index.py#L20) · complexity 2</sub>
<!-- docweave:end sym:TextIndex.add -->

<!-- docweave:begin sym:TextIndex.finalize -->
<a id="textindex-finalize"></a>
#### `TextIndex.finalize` <sup>method</sup>

```python
def finalize(self) -> 'TextIndex'
```

Compute IDF weights and document norms. Must be called before querying.

**Returns:** `'TextIndex'`

<sub>[`docweave/nlp/index.py:29`](../../docweave/nlp/index.py#L29) · complexity 7</sub>
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

<sub>[`docweave/nlp/index.py:39`](../../docweave/nlp/index.py#L39) · complexity 4</sub>
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

<sub>[`docweave/nlp/index.py:50`](../../docweave/nlp/index.py#L50) · complexity 11</sub>
<!-- docweave:end sym:TextIndex.cosine -->
