<!-- docweave:begin module -->
# `docweave.hooks`

Keep docs in sync automatically: a git pre-commit hook and a CI workflow template.

Source: [`docweave/hooks.py`](../../docweave/hooks.py) · 98 lines · main authors: AashutoshR (100%)

**Imports:** [`docweave.config`](docweave.config.md)

**Imported by:** [`docweave.cli`](docweave.cli.md)
<!-- docweave:end module -->

<!-- docweave:begin contents -->
## Contents

| Symbol | Kind | Summary |
| --- | --- | --- |
| [`MARKER`](#marker) | constant | Marker setting. |
| [`CI_WORKFLOW`](#ci-workflow) | constant | Ci workflow setting. |
| [`install_hook`](#install-hook) | function | Install a pre-commit hook. |
| [`uninstall_hook`](#uninstall-hook) | function | Remove the pre-commit hook if DocWeave installed it; returns whether anything was removed. |
| [`write_ci`](#write-ci) | function | Write the GitHub Actions workflow and return its path. |

## Reference
<!-- docweave:end contents -->

<!-- docweave:begin sym:MARKER -->
<a id="marker"></a>
### `MARKER` <sup>constant</sup>

```python
MARKER = '# docweave-hook'
```

Marker setting.

*No docstring in the source - this description is inferred from the name.*

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/hooks.py:11`](../../docweave/hooks.py#L11) · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:MARKER -->

<!-- docweave:begin sym:CI_WORKFLOW -->
<a id="ci-workflow"></a>
### `CI_WORKFLOW` <sup>constant</sup>

```python
CI_WORKFLOW = 'name: docs\n\non:\n  pull_request:\n  push:\n    branches: [main]\n\njobs:\n...
```

Ci workflow setting.

*No docstring in the source - this description is inferred from the name.*

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/hooks.py:13`](../../docweave/hooks.py#L13) · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:CI_WORKFLOW -->

<!-- docweave:begin sym:install_hook -->
<a id="install-hook"></a>
### `install_hook` <sup>function</sup>

```python
def install_hook(cfg: Config, sync: bool=False, force: bool=False) -> Path
```

Install a pre-commit hook.

By default the hook blocks a commit when the files it stages have high-severity drift
(drift elsewhere in the project is not held against it). With ``sync`` it instead
regenerates the docs and stages them, so docs travel in the same commit as the code.

| Parameter | Type | Default |
| --- | --- | --- |
| `cfg` | `Config` |  |
| `sync` | `bool` | `False` |
| `force` | `bool` | `False` |

**Returns:** `Path`

**Raises:** `RuntimeError`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/hooks.py:59`](../../docweave/hooks.py#L59) · complexity 5 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:install_hook -->

<!-- docweave:begin sym:uninstall_hook -->
<a id="uninstall-hook"></a>
### `uninstall_hook` <sup>function</sup>

```python
def uninstall_hook(cfg: Config) -> bool
```

Remove the pre-commit hook if DocWeave installed it; returns whether anything was removed.

| Parameter | Type |
| --- | --- |
| `cfg` | `Config` |

**Returns:** `bool`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/hooks.py:83`](../../docweave/hooks.py#L83) · complexity 3 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:uninstall_hook -->

<!-- docweave:begin sym:write_ci -->
<a id="write-ci"></a>
### `write_ci` <sup>function</sup>

```python
def write_ci(cfg: Config) -> Path
```

Write the GitHub Actions workflow and return its path.

| Parameter | Type |
| --- | --- |
| `cfg` | `Config` |

**Returns:** `Path`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/hooks.py:92`](../../docweave/hooks.py#L92) · complexity 1 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:write_ci -->
