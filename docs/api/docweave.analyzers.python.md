<!-- docweave:begin module -->
# `docweave.analyzers.python`

Static analysis of Python source using the standard ``ast`` module.

Source: [`docweave/analyzers/python.py`](../../docweave/analyzers/python.py) · 242 lines · main authors: AashutoshR (100%)

**Imports:** [`docweave.model`](docweave.model.md)

**Imported by:** [`docweave.analyzers`](docweave.analyzers.md)
<!-- docweave:end module -->

<!-- docweave:begin contents -->
## Contents

| Symbol | Kind | Summary |
| --- | --- | --- |
| [`EXTENSIONS`](#extensions) | constant | Extensions setting. |
| [`module_name`](#module-name) | function | Dotted module name for a Python file path (``src/pkg/mod.py`` -> ``pkg.mod``). |
| [`analyze`](#analyze) | function | Parse one Python file into a :class:`Module` with all of its documentable symbols. |

## Reference
<!-- docweave:end contents -->

<!-- docweave:begin sym:EXTENSIONS -->
<a id="extensions"></a>
### `EXTENSIONS` <sup>constant</sup>

```python
EXTENSIONS = ('.py',)
```

Extensions setting.

*No docstring in the source - this description is inferred from the name.*

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/analyzers/python.py:11`](../../docweave/analyzers/python.py#L11) · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:EXTENSIONS -->

<!-- docweave:begin sym:module_name -->
<a id="module-name"></a>
### `module_name` <sup>function</sup>

```python
def module_name(rel: str) -> str
```

Dotted module name for a Python file path (``src/pkg/mod.py`` -> ``pkg.mod``).

| Parameter | Type |
| --- | --- |
| `rel` | `str` |

**Returns:** `str`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/analyzers/python.py:14`](../../docweave/analyzers/python.py#L14) · complexity 5 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:module_name -->

<!-- docweave:begin sym:analyze -->
<a id="analyze"></a>
### `analyze` <sup>function</sup>

```python
def analyze(rel: str, text: str) -> Module
```

Parse one Python file into a :class:`Module` with all of its documentable symbols.

| Parameter | Type |
| --- | --- |
| `rel` | `str` |
| `text` | `str` |

**Returns:** `Module`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/analyzers/python.py:210`](../../docweave/analyzers/python.py#L210) · complexity 21 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:analyze -->
