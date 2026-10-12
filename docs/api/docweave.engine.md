<!-- docweave:begin module -->
# `docweave.engine`

The analysis pipeline: code structure + developer communication -> one linked model.

Source: [`docweave/engine.py`](../../docweave/engine.py) · 99 lines · main authors: AashutoshR (100%)

**Imports:** [`docweave`](docweave.md), [`docweave.analyzers`](docweave.analyzers.md), [`docweave.comms`](docweave.comms.md), [`docweave.config`](docweave.config.md), [`docweave.drift`](docweave.drift.md), [`docweave.gitrepo`](docweave.gitrepo.md), [`docweave.graph`](docweave.graph.md), [`docweave.linker`](docweave.linker.md), [`docweave.model`](docweave.model.md), [`docweave.nlp.intent`](docweave.nlp.intent.md)

**Imported by:** [`docweave.cli`](docweave.cli.md), [`docweave.llm`](docweave.llm.md), [`docweave.render`](docweave.render.md), [`docweave.search`](docweave.search.md)
<!-- docweave:end module -->

<!-- docweave:begin contents -->
## Contents

| Symbol | Kind | Summary |
| --- | --- | --- |
| [`Analysis`](#analysis) | class | Everything known about a project after one run: code, communication, links and drift. |
| [`Analysis.visible`](#analysis-visible) | method | Whether a symbol belongs in the generated docs. |
| [`Analysis.symbols_of`](#analysis-symbols-of) | method | Symbols a message is linked to, strongest link first. |
| [`Analysis.issues_for`](#analysis-issues-for) | method | Drift issues attached to one symbol. |
| [`analyze`](#analyze) | function | Run static analysis, read history and communication, link them, and detect drift. |

## Reference
<!-- docweave:end contents -->

<!-- docweave:begin sym:Analysis -->
<a id="analysis"></a>
### `Analysis` <sup>class</sup>

```python
@dataclass
class Analysis
```

Everything known about a project after one run: code, communication, links and drift.

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/engine.py:20`](../../docweave/engine.py#L20) · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Analysis -->

<!-- docweave:begin sym:Analysis.visible -->
<a id="analysis-visible"></a>
#### `Analysis.visible` <sup>method</sup>

```python
def visible(self, sym: Symbol) -> bool
```

Whether a symbol belongs in the generated docs.

| Parameter | Type |
| --- | --- |
| `sym` | `Symbol` |

**Returns:** `bool`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/engine.py:38`](../../docweave/engine.py#L38) · complexity 2 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Analysis.visible -->

<!-- docweave:begin sym:Analysis.symbols_of -->
<a id="analysis-symbols-of"></a>
#### `Analysis.symbols_of` <sup>method</sup>

```python
def symbols_of(self, message_id: str) -> list[tuple[str, float]]
```

Symbols a message is linked to, strongest link first.

| Parameter | Type |
| --- | --- |
| `message_id` | `str` |

**Returns:** `list[tuple[str, float]]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/engine.py:42`](../../docweave/engine.py#L42) · complexity 5 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Analysis.symbols_of -->

<!-- docweave:begin sym:Analysis.issues_for -->
<a id="analysis-issues-for"></a>
#### `Analysis.issues_for` <sup>method</sup>

```python
def issues_for(self, symbol_id: str) -> list[Issue]
```

Drift issues attached to one symbol.

| Parameter | Type |
| --- | --- |
| `symbol_id` | `str` |

**Returns:** `list[Issue]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/engine.py:52`](../../docweave/engine.py#L52) · complexity 3 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Analysis.issues_for -->

<!-- docweave:begin sym:analyze -->
<a id="analyze"></a>
### `analyze` <sup>function</sup>

```python
def analyze(cfg: Config, use_git: bool=True) -> Analysis
```

Run static analysis, read history and communication, link them, and detect drift.

| Parameter | Type | Default |
| --- | --- | --- |
| `cfg` | `Config` |  |
| `use_git` | `bool` | `True` |

**Returns:** `Analysis`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/engine.py:57`](../../docweave/engine.py#L57) · complexity 18 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:analyze -->
