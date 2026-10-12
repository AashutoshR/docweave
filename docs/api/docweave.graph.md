<!-- docweave:begin module -->
# `docweave.graph`

Module dependency graph: internal edges, external dependencies, cycles and a Mermaid drawing.

Source: [`docweave/graph.py`](../../docweave/graph.py) · 121 lines · main authors: AashutoshR (100%)

**Imports:** [`docweave.model`](docweave.model.md)

**Imported by:** [`docweave.engine`](docweave.engine.md), [`docweave.render`](docweave.render.md)
<!-- docweave:end module -->

<!-- docweave:begin contents -->
## Contents

| Symbol | Kind | Summary |
| --- | --- | --- |
| [`internal_edges`](#internal-edges) | function | Map each module to the project modules it imports. |
| [`external_dependencies`](#external-dependencies) | function | Third-party packages the project imports (standard-library modules are left out). |
| [`cycles`](#cycles) | function | Import cycles, as strongly connected components with more than one module (Tarjan). |
| [`mermaid`](#mermaid) | function | Draw the dependency graph; large projects are collapsed to one node per package. |

## Reference
<!-- docweave:end contents -->

<!-- docweave:begin sym:internal_edges -->
<a id="internal-edges"></a>
### `internal_edges` <sup>function</sup>

```python
def internal_edges(project: Project) -> dict[str, set[str]]
```

Map each module to the project modules it imports.

| Parameter | Type |
| --- | --- |
| `project` | `Project` |

**Returns:** `dict[str, set[str]]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/graph.py:13`](../../docweave/graph.py#L13) · complexity 7 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:internal_edges -->

<!-- docweave:begin sym:external_dependencies -->
<a id="external-dependencies"></a>
### `external_dependencies` <sup>function</sup>

```python
def external_dependencies(project: Project) -> list[str]
```

Third-party packages the project imports (standard-library modules are left out).

| Parameter | Type |
| --- | --- |
| `project` | `Project` |

**Returns:** `list[str]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/graph.py:25`](../../docweave/graph.py#L25) · complexity 11 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:external_dependencies -->

<!-- docweave:begin sym:cycles -->
<a id="cycles"></a>
### `cycles` <sup>function</sup>

```python
def cycles(edges: dict[str, set[str]]) -> list[list[str]]
```

Import cycles, as strongly connected components with more than one module (Tarjan).

| Parameter | Type |
| --- | --- |
| `edges` | `dict[str, set[str]]` |

**Returns:** `list[list[str]]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/graph.py:43`](../../docweave/graph.py#L43) · complexity 13 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:cycles -->

<!-- docweave:begin sym:mermaid -->
<a id="mermaid"></a>
### `mermaid` <sup>function</sup>

```python
def mermaid(edges: dict[str, set[str]], collapse_over: int=40) -> str
```

Draw the dependency graph; large projects are collapsed to one node per package.

| Parameter | Type | Default |
| --- | --- | --- |
| `edges` | `dict[str, set[str]]` |  |
| `collapse_over` | `int` | `40` |

**Returns:** `str`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/graph.py:95`](../../docweave/graph.py#L95) · complexity 17 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:mermaid -->
