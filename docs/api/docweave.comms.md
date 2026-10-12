<!-- docweave:begin module -->
# `docweave.comms`

Load developer communication that lives outside git: PRs, issues, chat exports, notes.

Drop files into the configured ``comms_dir`` and they are picked up automatically:

* ``*.json`` - a GitHub export (``gh pr list --json ...`` / ``gh issue list --json ...``),
  a Slack channel export (a list of ``{"user", "text", "ts"}``), or generic message objects.
* ``*.jsonl`` - one generic message object per line.
* ``*.md`` / ``*.txt`` - meeting notes or ADRs; the first heading is the title.

Source: [`docweave/comms.py`](../../docweave/comms.py) · 122 lines

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

<sub>[`docweave/comms.py:22`](../../docweave/comms.py#L22)</sub>
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

<sub>[`docweave/comms.py:65`](../../docweave/comms.py#L65) · complexity 19</sub>
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

<sub>[`docweave/comms.py:108`](../../docweave/comms.py#L108) · complexity 4</sub>
<!-- docweave:end sym:pull_github -->
