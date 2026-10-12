<!-- docweave:begin module -->
# `docweave.config`

Configuration: defaults, overridden by ``docweave.toml`` or ``[tool.docweave]`` in pyproject.

Source: [`docweave/config.py`](../../docweave/config.py) · 85 lines · main authors: AashutoshR (100%)

**Imported by:** [`docweave.analyzers`](docweave.analyzers.md), [`docweave.changelog`](docweave.changelog.md), [`docweave.cli`](docweave.cli.md), [`docweave.drift`](docweave.drift.md), [`docweave.engine`](docweave.engine.md), [`docweave.hooks`](docweave.hooks.md)
<!-- docweave:end module -->

<!-- docweave:begin contents -->
## Contents

| Symbol | Kind | Summary |
| --- | --- | --- |
| [`DEFAULT_EXCLUDE`](#default-exclude) | constant | Default exclude setting. |
| [`CONFIG_TEMPLATE`](#config-template) | constant | Config template setting. |
| [`Config`](#config) | class | Resolved settings for one project. |
| [`Config.excludes`](#config-excludes) | method | Built-in exclude patterns plus the project's own. |
| [`Config.state_dir`](#config-state-dir) | method | Folder for DocWeave's own state (signature anchors, AI cache). |
| [`load_config`](#load-config) | function | Load configuration for the project at ``root``, applying non-None ``overrides`` last. |

## Reference
<!-- docweave:end contents -->

<!-- docweave:begin sym:DEFAULT_EXCLUDE -->
<a id="default-exclude"></a>
### `DEFAULT_EXCLUDE` <sup>constant</sup>

```python
DEFAULT_EXCLUDE = ['.git', '.hg', '.svn', '.venv', 'venv', 'env', 'node_modules', '__pycache__'...
```

Default exclude setting.

*No docstring in the source - this description is inferred from the name.*

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/config.py:9`](../../docweave/config.py#L9) · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:DEFAULT_EXCLUDE -->

<!-- docweave:begin sym:CONFIG_TEMPLATE -->
<a id="config-template"></a>
### `CONFIG_TEMPLATE` <sup>constant</sup>

```python
CONFIG_TEMPLATE = '# DocWeave configuration. Every key is optional; the values below are the de...
```

Config template setting.

*No docstring in the source - this description is inferred from the name.*

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/config.py:16`](../../docweave/config.py#L16) · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:CONFIG_TEMPLATE -->

<!-- docweave:begin sym:Config -->
<a id="config"></a>
### `Config` <sup>class</sup>

```python
@dataclass
class Config
```

Resolved settings for one project.

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/config.py:33`](../../docweave/config.py#L33) · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Config -->

<!-- docweave:begin sym:Config.excludes -->
<a id="config-excludes"></a>
#### `Config.excludes` <sup>method</sup>

```python
@property
def excludes(self) -> list[str]
```

Built-in exclude patterns plus the project's own.

**Returns:** `list[str]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/config.py:51`](../../docweave/config.py#L51) · complexity 1 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Config.excludes -->

<!-- docweave:begin sym:Config.state_dir -->
<a id="config-state-dir"></a>
#### `Config.state_dir` <sup>method</sup>

```python
@property
def state_dir(self) -> Path
```

Folder for DocWeave's own state (signature anchors, AI cache).

**Returns:** `Path`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/config.py:56`](../../docweave/config.py#L56) · complexity 1 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Config.state_dir -->

<!-- docweave:begin sym:load_config -->
<a id="load-config"></a>
### `load_config` <sup>function</sup>

```python
def load_config(root: Path | str, **overrides) -> Config
```

Load configuration for the project at ``root``, applying non-None ``overrides`` last.

| Parameter | Type |
| --- | --- |
| `root` | `Path \| str` |
| `**overrides` |  |

**Returns:** `Config`

**Raises:** `ValueError`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/config.py:61`](../../docweave/config.py#L61) · complexity 10 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:load_config -->
