<!-- docweave:begin module -->
# `docweave.nlp.rationale`

Mine the *why* out of developer communication.

Code says what happens; commit bodies, PR threads and chat say why. These heuristics find the
sentences that carry intent ("because", "to avoid", "instead of", "we decided") so they can be
attached to the code they explain.

Source: [`docweave/nlp/rationale.py`](../../docweave/nlp/rationale.py) · 67 lines

**Imports:** [`docweave.nlp.text`](docweave.nlp.text.md)

**Imported by:** [`docweave.cli`](docweave.cli.md), [`docweave.llm`](docweave.llm.md), [`docweave.render`](docweave.render.md), [`docweave.search`](docweave.search.md)
<!-- docweave:end module -->

<!-- docweave:begin contents -->
## Contents

| Symbol | Kind | Summary |
| --- | --- | --- |
| [`score_sentence`](#score-sentence) | function | How strongly a sentence reads as an explanation rather than a description. |
| [`rationale`](#rationale) | function | Return up to ``limit`` sentences from a message that best explain why a change was made. |
| [`decision_score`](#decision-score) | function | Score a message as a design decision worth recording in the decision log. |

## Reference
<!-- docweave:end contents -->

<!-- docweave:begin sym:score_sentence -->
<a id="score-sentence"></a>
### `score_sentence` <sup>function</sup>

```python
def score_sentence(sentence: str) -> float
```

How strongly a sentence reads as an explanation rather than a description.

| Parameter | Type |
| --- | --- |
| `sentence` | `str` |

**Returns:** `float`

<sub>[`docweave/nlp/rationale.py:45`](../../docweave/nlp/rationale.py#L45) · complexity 4</sub>
<!-- docweave:end sym:score_sentence -->

<!-- docweave:begin sym:rationale -->
<a id="rationale"></a>
### `rationale` <sup>function</sup>

```python
def rationale(title: str, body: str, limit: int=2) -> list[str]
```

Return up to ``limit`` sentences from a message that best explain why a change was made.

The body is where people explain themselves; the title is only mined when there is no body.

| Parameter | Type | Default |
| --- | --- | --- |
| `title` | `str` |  |
| `body` | `str` |  |
| `limit` | `int` | `2` |

**Returns:** `list[str]`

<sub>[`docweave/nlp/rationale.py:52`](../../docweave/nlp/rationale.py#L52) · complexity 6</sub>
<!-- docweave:end sym:rationale -->

<!-- docweave:begin sym:decision_score -->
<a id="decision-score"></a>
### `decision_score` <sup>function</sup>

```python
def decision_score(title: str, body: str) -> float
```

Score a message as a design decision worth recording in the decision log.

| Parameter | Type |
| --- | --- |
| `title` | `str` |
| `body` | `str` |

**Returns:** `float`

<sub>[`docweave/nlp/rationale.py:62`](../../docweave/nlp/rationale.py#L62) · complexity 3</sub>
<!-- docweave:end sym:decision_score -->
