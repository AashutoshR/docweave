<!-- docweave:begin module -->
# `docweave.nlp.text`

Tokenising, identifier splitting, light stemming and sentence segmentation.

Source: [`docweave/nlp/text.py`](../../docweave/nlp/text.py) · 88 lines

**Imported by:** [`docweave.linker`](docweave.linker.md), [`docweave.nlp.describe`](docweave.nlp.describe.md), [`docweave.nlp.docstring`](docweave.nlp.docstring.md), [`docweave.nlp.intent`](docweave.nlp.intent.md), [`docweave.nlp.rationale`](docweave.nlp.rationale.md), [`docweave.render`](docweave.render.md), [`docweave.search`](docweave.search.md)
<!-- docweave:end module -->

<!-- docweave:begin contents -->
## Contents

| Symbol | Kind | Summary |
| --- | --- | --- |
| [`STOPWORDS`](#stopwords) | constant | Stopwords setting. |
| [`split_identifier`](#split-identifier) | function | Split ``snake_case`` / ``camelCase`` / ``HTTPServer`` into lowercase words. |
| [`stem`](#stem) | function | A deliberately small suffix stripper; it only has to be consistent, not linguistically right. |
| [`tokenize`](#tokenize) | function | Lowercased, identifier-split, stemmed tokens suitable for retrieval and classification. |
| [`sentences`](#sentences) | function | Split prose (commit bodies, chat, PR descriptions) into sentences; bullets count as sentences. |
| [`first_sentence`](#first-sentence) | function | The first sentence of ``text``, or an empty string. |

## Reference
<!-- docweave:end contents -->

<!-- docweave:begin sym:STOPWORDS -->
<a id="stopwords"></a>
### `STOPWORDS` <sup>constant</sup>

```python
STOPWORDS = frozenset('a an the and or but if then else of to in on at by for from with w...
```

Stopwords setting.

*No docstring in the source - this description is inferred from the name.*

<sub>[`docweave/nlp/text.py:7`](../../docweave/nlp/text.py#L7)</sub>
<!-- docweave:end sym:STOPWORDS -->

<!-- docweave:begin sym:split_identifier -->
<a id="split-identifier"></a>
### `split_identifier` <sup>function</sup>

```python
def split_identifier(name: str) -> list[str]
```

Split ``snake_case`` / ``camelCase`` / ``HTTPServer`` into lowercase words.

| Parameter | Type |
| --- | --- |
| `name` | `str` |

**Returns:** `list[str]`

<sub>[`docweave/nlp/text.py:20`](../../docweave/nlp/text.py#L20) · complexity 4</sub>
<!-- docweave:end sym:split_identifier -->

<!-- docweave:begin sym:stem -->
<a id="stem"></a>
### `stem` <sup>function</sup>

```python
def stem(word: str) -> str
```

A deliberately small suffix stripper; it only has to be consistent, not linguistically right.

| Parameter | Type |
| --- | --- |
| `word` | `str` |

**Returns:** `str`

<sub>[`docweave/nlp/text.py:28`](../../docweave/nlp/text.py#L28) · complexity 12</sub>
<!-- docweave:end sym:stem -->

<!-- docweave:begin sym:tokenize -->
<a id="tokenize"></a>
### `tokenize` <sup>function</sup>

```python
def tokenize(text: str, *, keep_stopwords: bool=False) -> list[str]
```

Lowercased, identifier-split, stemmed tokens suitable for retrieval and classification.

| Parameter | Type | Default |
| --- | --- | --- |
| `text` | `str` |  |
| `keep_stopwords` | `bool` | `False` |

**Returns:** `list[str]`

<sub>[`docweave/nlp/text.py:44`](../../docweave/nlp/text.py#L44) · complexity 6</sub>
<!-- docweave:end sym:tokenize -->

<!-- docweave:begin sym:sentences -->
<a id="sentences"></a>
### `sentences` <sup>function</sup>

```python
def sentences(text: str) -> list[str]
```

Split prose (commit bodies, chat, PR descriptions) into sentences; bullets count as sentences.

| Parameter | Type |
| --- | --- |
| `text` | `str` |

**Returns:** `list[str]`

<sub>[`docweave/nlp/text.py:59`](../../docweave/nlp/text.py#L59) · complexity 8</sub>
<!-- docweave:end sym:sentences -->

<!-- docweave:begin sym:first_sentence -->
<a id="first-sentence"></a>
### `first_sentence` <sup>function</sup>

```python
def first_sentence(text: str) -> str
```

The first sentence of ``text``, or an empty string.

| Parameter | Type |
| --- | --- |
| `text` | `str` |

**Returns:** `str`

<sub>[`docweave/nlp/text.py:84`](../../docweave/nlp/text.py#L84) · complexity 2</sub>
<!-- docweave:end sym:first_sentence -->
