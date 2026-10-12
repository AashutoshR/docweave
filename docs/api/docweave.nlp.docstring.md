<!-- docweave:begin module -->
# `docweave.nlp.docstring`

Parse docstrings (Google, NumPy, Sphinx and JSDoc styles) into structured claims.

The point is not pretty rendering: it is to recover what the documentation *claims* about a
function (its parameters, return value and exceptions) so those claims can be checked against
what static analysis says the code actually does.

Source: [`docweave/nlp/docstring.py`](../../docweave/nlp/docstring.py) · 171 lines

**Imports:** [`docweave.nlp.text`](docweave.nlp.text.md)

**Imported by:** [`docweave.drift`](docweave.drift.md), [`docweave.render`](docweave.render.md), [`docweave.search`](docweave.search.md)
<!-- docweave:end module -->

<!-- docweave:begin contents -->
## Contents

| Symbol | Kind | Summary |
| --- | --- | --- |
| [`PARAM_HEADS`](#param-heads) | constant | Param heads setting. |
| [`RETURN_HEADS`](#return-heads) | constant | Return heads setting. |
| [`RAISE_HEADS`](#raise-heads) | constant | Raise heads setting. |
| [`OTHER_HEADS`](#other-heads) | constant | Other heads setting. |
| [`ALL_HEADS`](#all-heads) | constant | All heads setting. |
| [`DocInfo`](#docinfo) | class | The claims a docstring makes, in structured form. |
| [`parse_docstring`](#parse-docstring) | function | Parse a docstring of any supported style into a :class:`DocInfo`. |

## Reference
<!-- docweave:end contents -->

<!-- docweave:begin sym:PARAM_HEADS -->
<a id="param-heads"></a>
### `PARAM_HEADS` <sup>constant</sup>

```python
PARAM_HEADS = {'args', 'arguments', 'parameters', 'params', 'keyword args', 'keyword argume...
```

Param heads setting.

*No docstring in the source - this description is inferred from the name.*

<sub>[`docweave/nlp/docstring.py:16`](../../docweave/nlp/docstring.py#L16)</sub>
<!-- docweave:end sym:PARAM_HEADS -->

<!-- docweave:begin sym:RETURN_HEADS -->
<a id="return-heads"></a>
### `RETURN_HEADS` <sup>constant</sup>

```python
RETURN_HEADS = {'returns', 'return', 'yields', 'yield'}
```

Return heads setting.

*No docstring in the source - this description is inferred from the name.*

<sub>[`docweave/nlp/docstring.py:17`](../../docweave/nlp/docstring.py#L17)</sub>
<!-- docweave:end sym:RETURN_HEADS -->

<!-- docweave:begin sym:RAISE_HEADS -->
<a id="raise-heads"></a>
### `RAISE_HEADS` <sup>constant</sup>

```python
RAISE_HEADS = {'raises', 'raise', 'throws'}
```

Raise heads setting.

*No docstring in the source - this description is inferred from the name.*

<sub>[`docweave/nlp/docstring.py:18`](../../docweave/nlp/docstring.py#L18)</sub>
<!-- docweave:end sym:RAISE_HEADS -->

<!-- docweave:begin sym:OTHER_HEADS -->
<a id="other-heads"></a>
### `OTHER_HEADS` <sup>constant</sup>

```python
OTHER_HEADS = {'example', 'examples', 'note', 'notes', 'attributes', 'see also', 'warning',...
```

Other heads setting.

*No docstring in the source - this description is inferred from the name.*

<sub>[`docweave/nlp/docstring.py:19`](../../docweave/nlp/docstring.py#L19)</sub>
<!-- docweave:end sym:OTHER_HEADS -->

<!-- docweave:begin sym:ALL_HEADS -->
<a id="all-heads"></a>
### `ALL_HEADS` <sup>constant</sup>

```python
ALL_HEADS = PARAM_HEADS | RETURN_HEADS | RAISE_HEADS | OTHER_HEADS
```

All heads setting.

*No docstring in the source - this description is inferred from the name.*

<sub>[`docweave/nlp/docstring.py:23`](../../docweave/nlp/docstring.py#L23)</sub>
<!-- docweave:end sym:ALL_HEADS -->

<!-- docweave:begin sym:DocInfo -->
<a id="docinfo"></a>
### `DocInfo` <sup>class</sup>

```python
@dataclass
class DocInfo
```

The claims a docstring makes, in structured form.

<sub>[`docweave/nlp/docstring.py:41`](../../docweave/nlp/docstring.py#L41)</sub>
<!-- docweave:end sym:DocInfo -->

<!-- docweave:begin sym:parse_docstring -->
<a id="parse-docstring"></a>
### `parse_docstring` <sup>function</sup>

```python
def parse_docstring(text: str | None) -> DocInfo
```

Parse a docstring of any supported style into a :class:`DocInfo`.

| Parameter | Type |
| --- | --- |
| `text` | `str \| None` |

**Returns:** `DocInfo`

<sub>[`docweave/nlp/docstring.py:96`](../../docweave/nlp/docstring.py#L96) · complexity 48</sub>
<!-- docweave:end sym:parse_docstring -->
