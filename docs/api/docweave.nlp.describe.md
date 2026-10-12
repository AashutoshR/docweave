<!-- docweave:begin module -->
# `docweave.nlp.describe`

Synthesise a one-line description for symbols nobody documented.

Well-named code already half-documents itself; this turns ``get_user_by_id`` into
"Return user by id." Output is always labelled as inferred so it is never mistaken for
something a human wrote.

Source: [`docweave/nlp/describe.py`](../../docweave/nlp/describe.py) · 43 lines · main authors: AashutoshR (100%)

**Imports:** [`docweave.nlp.text`](docweave.nlp.text.md)

**Imported by:** [`docweave.render`](docweave.render.md)
<!-- docweave:end module -->

<!-- docweave:begin contents -->
## Contents

| Symbol | Kind | Summary |
| --- | --- | --- |
| [`describe`](#describe) | function | Return an inferred one-line description for a symbol called ``name``. |

## Reference
<!-- docweave:end contents -->

<!-- docweave:begin sym:describe -->
<a id="describe"></a>
### `describe` <sup>function</sup>

```python
def describe(name: str, kind: str) -> str
```

Return an inferred one-line description for a symbol called ``name``.

| Parameter | Type |
| --- | --- |
| `name` | `str` |
| `kind` | `str` |

**Returns:** `str`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/nlp/describe.py:28`](../../docweave/nlp/describe.py#L28) · complexity 6 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:describe -->
