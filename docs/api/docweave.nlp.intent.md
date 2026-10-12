<!-- docweave:begin module -->
# `docweave.nlp.intent`

Classify what a piece of developer communication is *doing*: fixing, adding, refactoring...

Conventional-commit prefixes are trusted when present. Otherwise a weighted lexicon votes, with
the leading word of the subject counting most (commit subjects are usually imperative).

Source: [`docweave/nlp/intent.py`](../../docweave/nlp/intent.py) · 90 lines · main authors: AashutoshR (100%)

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

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/nlp/intent.py:13`](../../docweave/nlp/intent.py#L13) · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:INTENTS -->

<!-- docweave:begin sym:INTENT_TITLES -->
<a id="intent-titles"></a>
### `INTENT_TITLES` <sup>constant</sup>

```python
INTENT_TITLES = {'feature': 'Features', 'fix': 'Fixes', 'perf': 'Performance', 'security': 'S...
```

Intent titles setting.

*No docstring in the source - this description is inferred from the name.*

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/nlp/intent.py:15`](../../docweave/nlp/intent.py#L15) · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:INTENT_TITLES -->

<!-- docweave:begin sym:DOC_IMPACT -->
<a id="doc-impact"></a>
### `DOC_IMPACT` <sup>constant</sup>

```python
DOC_IMPACT = {'feature': 1.0, 'fix': 1.0, 'security': 1.0, 'deprecation': 1.0, 'revert': 1...
```

How strongly a change of this kind is expected to invalidate existing documentation.

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/nlp/intent.py:31`](../../docweave/nlp/intent.py#L31) · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:DOC_IMPACT -->

<!-- docweave:begin sym:LEXICON -->
<a id="lexicon"></a>
### `LEXICON` <sup>constant</sup>

```python
LEXICON = {intent: {stem(w) for w in words.split()} for intent, words in _LEXICON_WORDS...
```

Lexicon setting.

*No docstring in the source - this description is inferred from the name.*

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/nlp/intent.py:59`](../../docweave/nlp/intent.py#L59) · written by AashutoshR (100%)</sub>
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

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/nlp/intent.py:64`](../../docweave/nlp/intent.py#L64) · complexity 12 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:classify -->
