<!-- docweave:begin module -->
# `docweave.analyzers.python`

Static analysis of Python source using the standard ``ast`` module.

Source: [`docweave/analyzers/python.py`](../../docweave/analyzers/python.py) · 242 lines

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

<sub>[`docweave/analyzers/python.py:11`](../../docweave/analyzers/python.py#L11)</sub>
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

<sub>[`docweave/analyzers/python.py:14`](../../docweave/analyzers/python.py#L14) · complexity 5</sub>
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

<sub>[`docweave/analyzers/python.py:210`](../../docweave/analyzers/python.py#L210) · complexity 21</sub>
<!-- docweave:end sym:analyze -->
