<!-- docweave:begin module -->
# `docweave.comms`

Load developer communication that lives outside git: PRs, issues, chat exports, notes.

Drop files into the configured ``comms_dir`` and they are picked up automatically:

* ``*.json`` - a GitHub export (``gh pr list --json ...`` / ``gh issue list --json ...``),
  a Slack channel export (a list of ``{"user", "text", "ts"}``), or generic message objects.
* ``*.jsonl`` - one generic message object per line.
* ``*.md`` / ``*.txt`` - meeting notes or ADRs; the first heading is the title.

Source: [`docweave/comms.py`](../../docweave/comms.py) · 122 lines · main authors: AashutoshR (100%)

**Imports:** [`docweave.model`](docweave.model.md)

**Imported by:** [`docweave.cli`](docweave.cli.md), [`docweave.engine`](docweave.engine.md)
<!-- docweave:end module -->

<!-- docweave:begin contents -->
## Contents

| Symbol | Kind | Summary |
| --- | --- | --- |
| [`GH_FIELDS`](#gh-fields) | constant | Gh fields setting. |
| [`load_comms`](#load-comms) | function | Read every supported file under ``directory`` into normalised messages. |
| [`pull_github`](#pull-github) | function | Export merged PRs and issues with the ``gh`` CLI into ``directory`` (needs ``gh auth login``). |

## Reference
<!-- docweave:end contents -->

<!-- docweave:begin sym:GH_FIELDS -->
<a id="gh-fields"></a>
### `GH_FIELDS` <sup>constant</sup>

```python
GH_FIELDS = 'number,title,body,author,createdAt,url'
```

Gh fields setting.

*No docstring in the source - this description is inferred from the name.*

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/comms.py:22`](../../docweave/comms.py#L22) · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:GH_FIELDS -->

<!-- docweave:begin sym:load_comms -->
<a id="load-comms"></a>
### `load_comms` <sup>function</sup>

```python
def load_comms(directory: Path) -> list[Message]
```

Read every supported file under ``directory`` into normalised messages.

| Parameter | Type |
| --- | --- |
| `directory` | `Path` |

**Returns:** `list[Message]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/comms.py:65`](../../docweave/comms.py#L65) · complexity 19 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:load_comms -->

<!-- docweave:begin sym:pull_github -->
<a id="pull-github"></a>
### `pull_github` <sup>function</sup>

```python
def pull_github(root: Path, directory: Path, limit: int=200) -> list[Path]
```

Export merged PRs and issues with the ``gh`` CLI into ``directory`` (needs ``gh auth login``).

| Parameter | Type | Default |
| --- | --- | --- |
| `root` | `Path` |  |
| `directory` | `Path` |  |
| `limit` | `int` | `200` |

**Returns:** `list[Path]`

**Raises:** `RuntimeError`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/comms.py:108`](../../docweave/comms.py#L108) · complexity 4 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:pull_github -->
