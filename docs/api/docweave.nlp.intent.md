<!-- docweave:begin module -->
# `docweave.nlp.intent`

Classify what a piece of developer communication is *doing*: fixing, adding, refactoring...

Conventional-commit prefixes are trusted when present. Otherwise a weighted lexicon votes, with
the leading word of the subject counting most (commit subjects are usually imperative).

Source: [`docweave/nlp/intent.py`](../../docweave/nlp/intent.py) · 90 lines

**Imports:** [`docweave.nlp.text`](docweave.nlp.text.md)

**Imported by:** [`docweave.cli`](docweave.cli.md), [`docweave.drift`](docweave.drift.md), [`docweave.engine`](docweave.engine.md), [`docweave.render`](docweave.render.md)
<!-- docweave:end module -->

<!-- docweave:begin contents -->
## Contents

| Symbol | Kind | Summary |
| --- | --- | --- |
| [`INTENTS`](#intents) | constant | Intents setting. |
| [`INTENT_TITLES`](#intent-titles) | constant | Intent titles setting. |
| [`DOC_IMPACT`](#doc-impact) | constant | How strongly a change of this kind is expected to invalidate existing documentation. |
| [`LEXICON`](#lexicon) | constant | Lexicon setting. |
| [`classify`](#classify) | function | Return ``(intent, scope, breaking, confidence, clean_subject)`` for a message. |

## Reference
<!-- docweave:end contents -->

<!-- docweave:begin sym:INTENTS -->
<a id="intents"></a>
### `INTENTS` <sup>constant</sup>

```python
INTENTS = ('security', 'fix', 'feature', 'perf', 'deprecation', 'refactor', 'revert', '...
```

Intents setting.

*No docstring in the source - this description is inferred from the name.*

<sub>[`docweave/nlp/intent.py:13`](../../docweave/nlp/intent.py#L13)</sub>
<!-- docweave:end sym:INTENTS -->

<!-- docweave:begin sym:INTENT_TITLES -->
<a id="intent-titles"></a>
### `INTENT_TITLES` <sup>constant</sup>

```python
INTENT_TITLES = {'feature': 'Features', 'fix': 'Fixes', 'perf': 'Performance', 'security': 'S...
```

Intent titles setting.

*No docstring in the source - this description is inferred from the name.*

<sub>[`docweave/nlp/intent.py:15`](../../docweave/nlp/intent.py#L15)</sub>
<!-- docweave:end sym:INTENT_TITLES -->

<!-- docweave:begin sym:DOC_IMPACT -->
<a id="doc-impact"></a>
### `DOC_IMPACT` <sup>constant</sup>

```python
DOC_IMPACT = {'feature': 1.0, 'fix': 1.0, 'security': 1.0, 'deprecation': 1.0, 'revert': 1...
```

How strongly a change of this kind is expected to invalidate existing documentation.

<sub>[`docweave/nlp/intent.py:31`](../../docweave/nlp/intent.py#L31)</sub>
<!-- docweave:end sym:DOC_IMPACT -->

<!-- docweave:begin sym:LEXICON -->
<a id="lexicon"></a>
### `LEXICON` <sup>constant</sup>

```python
LEXICON = {intent: {stem(w) for w in words.split()} for intent, words in _LEXICON_WORDS...
```

Lexicon setting.

*No docstring in the source - this description is inferred from the name.*

<sub>[`docweave/nlp/intent.py:59`](../../docweave/nlp/intent.py#L59)</sub>
<!-- docweave:end sym:LEXICON -->

<!-- docweave:begin sym:classify -->
<a id="classify"></a>
### `classify` <sup>function</sup>

```python
def classify(title: str, body: str='') -> tuple[str, str | None, bool, float, str]
```

Return ``(intent, scope, breaking, confidence, clean_subject)`` for a message.

| Parameter | Type | Default |
| --- | --- | --- |
| `title` | `str` |  |
| `body` | `str` | `''` |

**Returns:** `tuple[str, str | None, bool, float, str]`

<sub>[`docweave/nlp/intent.py:64`](../../docweave/nlp/intent.py#L64) · complexity 12</sub>
<!-- docweave:end sym:classify -->
