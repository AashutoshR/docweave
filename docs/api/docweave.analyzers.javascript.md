<!-- docweave:begin module -->
# `docweave.analyzers.javascript`

Structural analysis of JavaScript / TypeScript.

There is no JS parser in the Python standard library, so this is a scanner rather than a full
parser. It blanks out comments and strings, finds the *head* of each declaration with a regular
expression, and then walks balanced brackets to find its parameter list, return type and body -
which is what lets it cope with callback types, object-literal types and multi-line signatures.

It understands top-level functions, arrow functions and function expressions assigned to
constants or to ``exports.x``, classes with their methods and arrow-function properties,
TypeScript interfaces, type aliases and enums, JSDoc blocks, and ES / CommonJS imports and exports.
Declarations nested inside other functions are deliberately ignored.

Source: [`docweave/analyzers/javascript.py`](../../docweave/analyzers/javascript.py) · 432 lines · main authors: AashutoshR (100%)

**Imports:** [`docweave.model`](docweave.model.md)

**Imported by:** [`docweave.analyzers`](docweave.analyzers.md)
<!-- docweave:end module -->

<!-- docweave:begin contents -->
## Contents

| Symbol | Kind | Summary |
| --- | --- | --- |
| [`EXTENSIONS`](#extensions) | constant | Extensions setting. |
| [`module_name`](#module-name) | function | Dotted module name for a JS/TS file path (``src/cart/index.ts`` -> ``cart``). |
| [`mask`](#mask) | function | Replace comments (and optionally string contents) with spaces, preserving offsets and newlines. |
| [`analyze`](#analyze) | function | Scan one JS/TS file into a :class:`Module`. |

## Reference
<!-- docweave:end contents -->

<!-- docweave:begin sym:EXTENSIONS -->
<a id="extensions"></a>
### `EXTENSIONS` <sup>constant</sup>

```python
EXTENSIONS = ('.js', '.jsx', '.mjs', '.cjs', '.ts', '.tsx')
```

Extensions setting.

*No docstring in the source - this description is inferred from the name.*

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/analyzers/javascript.py:23`](../../docweave/analyzers/javascript.py#L23) · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:EXTENSIONS -->

<!-- docweave:begin sym:module_name -->
<a id="module-name"></a>
### `module_name` <sup>function</sup>

```python
def module_name(rel: str) -> str
```

Dotted module name for a JS/TS file path (``src/cart/index.ts`` -> ``cart``).

| Parameter | Type |
| --- | --- |
| `rel` | `str` |

**Returns:** `str`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/analyzers/javascript.py:51`](../../docweave/analyzers/javascript.py#L51) · complexity 5 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:module_name -->

<!-- docweave:begin sym:mask -->
<a id="mask"></a>
### `mask` <sup>function</sup>

```python
def mask(text: str, strings: bool=True) -> str
```

Replace comments (and optionally string contents) with spaces, preserving offsets and newlines.

| Parameter | Type | Default |
| --- | --- | --- |
| `text` | `str` |  |
| `strings` | `bool` | `True` |

**Returns:** `str`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/analyzers/javascript.py:66`](../../docweave/analyzers/javascript.py#L66) · complexity 17 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:mask -->

<!-- docweave:begin sym:analyze -->
<a id="analyze"></a>
### `analyze` <sup>function</sup>

```python
def analyze(rel: str, text: str) -> Module
```

Scan one JS/TS file into a :class:`Module`.

| Parameter | Type |
| --- | --- |
| `rel` | `str` |
| `text` | `str` |

**Returns:** `Module`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/analyzers/javascript.py:410`](../../docweave/analyzers/javascript.py#L410) · complexity 10 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:analyze -->
