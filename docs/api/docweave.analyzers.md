<!-- docweave:begin module -->
# `docweave.analyzers`

Language analyzers and source discovery.

Source: [`docweave/analyzers/__init__.py`](../../docweave/analyzers/__init__.py) · 61 lines · main authors: AashutoshR (100%)

**Imports:** [`docweave.analyzers.javascript`](docweave.analyzers.javascript.md), [`docweave.analyzers.python`](docweave.analyzers.python.md), [`docweave.config`](docweave.config.md), [`docweave.model`](docweave.model.md)

**Imported by:** [`docweave.cli`](docweave.cli.md), [`docweave.drift`](docweave.drift.md), [`docweave.engine`](docweave.engine.md)
<!-- docweave:end module -->

<!-- docweave:begin contents -->
## Contents

| Symbol | Kind | Summary |
| --- | --- | --- |
| [`ANALYZERS`](#analyzers) | constant | Analyzers setting. |
| [`is_excluded`](#is-excluded) | function | True if any path component, or the whole relative path, matches an exclude pattern. |
| [`discover`](#discover) | function | List project files (posix paths relative to the root) having one of ``extensions``. |
| [`scan`](#scan) | function | Run static analysis over every supported source file in the project. |

## Reference
<!-- docweave:end contents -->

<!-- docweave:begin sym:ANALYZERS -->
<a id="analyzers"></a>
### `ANALYZERS` <sup>constant</sup>

```python
ANALYZERS = {ext: mod.analyze for mod in (python, javascript) for ext in mod.EXTENSIONS}
```

Analyzers setting.

*No docstring in the source - this description is inferred from the name.*

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/analyzers/__init__.py:13`](../../docweave/analyzers/__init__.py#L13) · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:ANALYZERS -->

<!-- docweave:begin sym:is_excluded -->
<a id="is-excluded"></a>
### `is_excluded` <sup>function</sup>

```python
def is_excluded(rel: str, patterns: list[str]) -> bool
```

True if any path component, or the whole relative path, matches an exclude pattern.

| Parameter | Type |
| --- | --- |
| `rel` | `str` |
| `patterns` | `list[str]` |

**Returns:** `bool`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/analyzers/__init__.py:16`](../../docweave/analyzers/__init__.py#L16) · complexity 5 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:is_excluded -->

<!-- docweave:begin sym:discover -->
<a id="discover"></a>
### `discover` <sup>function</sup>

```python
def discover(cfg: Config, extensions: tuple[str, ...], sources: list[str] | None=None) -> list[str]
```

List project files (posix paths relative to the root) having one of ``extensions``.

| Parameter | Type | Default |
| --- | --- | --- |
| `cfg` | `Config` |  |
| `extensions` | `tuple[str, ...]` |  |
| `sources` | `list[str] \| None` | `None` |

**Returns:** `list[str]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/analyzers/__init__.py:24`](../../docweave/analyzers/__init__.py#L24) · complexity 10 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:discover -->

<!-- docweave:begin sym:scan -->
<a id="scan"></a>
### `scan` <sup>function</sup>

```python
def scan(cfg: Config) -> Project
```

Run static analysis over every supported source file in the project.

| Parameter | Type |
| --- | --- |
| `cfg` | `Config` |

**Returns:** `Project`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/analyzers/__init__.py:42`](../../docweave/analyzers/__init__.py#L42) · complexity 6 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:scan -->
