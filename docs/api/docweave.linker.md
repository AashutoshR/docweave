<!-- docweave:begin module -->
# `docweave.linker`

Link developer communication to the code it is about.

Three independent kinds of evidence are combined (noisy-OR) into one confidence per
``(message, symbol)`` pair:

* **blame** - the commit is the last writer of lines that still exist in the symbol;
* **mention** - the message names the symbol (``in backticks``, as a call, or as a distinctive
  identifier in running text);
* **similarity** - TF-IDF cosine between the message and the symbol's name and docstring.

Pull requests and issues additionally inherit the links of commits that reference them (``#12``).

Source: [`docweave/linker.py`](../../docweave/linker.py) · 188 lines · main authors: AashutoshR (100%)

**Imports:** [`docweave.gitrepo`](docweave.gitrepo.md), [`docweave.model`](docweave.model.md), [`docweave.nlp.index`](docweave.nlp.index.md), [`docweave.nlp.text`](docweave.nlp.text.md)

**Imported by:** [`docweave.cli`](docweave.cli.md), [`docweave.drift`](docweave.drift.md), [`docweave.engine`](docweave.engine.md), [`docweave.render`](docweave.render.md)
<!-- docweave:end module -->

<!-- docweave:begin contents -->
## Contents

| Symbol | Kind | Summary |
| --- | --- | --- |
| [`MIN_CONFIDENCE`](#min-confidence) | constant | Min confidence setting. |
| [`BlameInfo`](#blameinfo) | class | Which commits last wrote each part of a symbol. |
| [`symbol_blame`](#symbol-blame) | function | Attribute every line of every symbol to the commit that last wrote it. |
| [`is_distinctive`](#is-distinctive) | function | Would this name, seen in running prose, plausibly be a reference to code? |
| [`Linker`](#linker) | class | Scores every (message, symbol) pair from blame, mentions and wording similarity. |
| [`Linker.mentions`](#linker-mentions) | method | Symbols a message names explicitly, with the strength of each mention. |
| [`Linker.run`](#linker-run) | method | Compute links for every symbol, newest message first. |
| [`owners`](#owners) | function | Authors of the surviving lines of a symbol, as ``(name, share)`` pairs. |

## Reference
<!-- docweave:end contents -->

<!-- docweave:begin sym:MIN_CONFIDENCE -->
<a id="min-confidence"></a>
### `MIN_CONFIDENCE` <sup>constant</sup>

```python
MIN_CONFIDENCE = 0.3
```

Min confidence setting.

*No docstring in the source - this description is inferred from the name.*

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/linker.py:28`](../../docweave/linker.py#L28) · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:MIN_CONFIDENCE -->

<!-- docweave:begin sym:BlameInfo -->
<a id="blameinfo"></a>
### `BlameInfo` <sup>class</sup>

```python
@dataclass
class BlameInfo
```

Which commits last wrote each part of a symbol.

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/linker.py:32`](../../docweave/linker.py#L32) · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:BlameInfo -->

<!-- docweave:begin sym:symbol_blame -->
<a id="symbol-blame"></a>
### `symbol_blame` <sup>function</sup>

```python
def symbol_blame(project: Project, blame: dict[str, list[str]]) -> dict[str, BlameInfo]
```

Attribute every line of every symbol to the commit that last wrote it.

| Parameter | Type |
| --- | --- |
| `project` | `Project` |
| `blame` | `dict[str, list[str]]` |

**Returns:** `dict[str, BlameInfo]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/linker.py:40`](../../docweave/linker.py#L40) · complexity 14 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:symbol_blame -->

<!-- docweave:begin sym:is_distinctive -->
<a id="is-distinctive"></a>
### `is_distinctive` <sup>function</sup>

```python
def is_distinctive(name: str) -> bool
```

Would this name, seen in running prose, plausibly be a reference to code?

| Parameter | Type |
| --- | --- |
| `name` | `str` |

**Returns:** `bool`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/linker.py:67`](../../docweave/linker.py#L67) · complexity 4 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:is_distinctive -->

<!-- docweave:begin sym:Linker -->
<a id="linker"></a>
### `Linker` <sup>class</sup>

```python
class Linker
```

Scores every (message, symbol) pair from blame, mentions and wording similarity.

| Parameter | Type |
| --- | --- |
| `project` | `Project` |
| `messages` | `dict[str, Message]` |
| `blame_info` | `dict[str, BlameInfo]` |

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/linker.py:80`](../../docweave/linker.py#L80) · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Linker -->

<!-- docweave:begin sym:Linker.mentions -->
<a id="linker-mentions"></a>
#### `Linker.mentions` <sup>method</sup>

```python
def mentions(self, message: Message) -> dict[str, float]
```

Symbols a message names explicitly, with the strength of each mention.

| Parameter | Type |
| --- | --- |
| `message` | `Message` |

**Returns:** `dict[str, float]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/linker.py:100`](../../docweave/linker.py#L100) · complexity 18 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Linker.mentions -->

<!-- docweave:begin sym:Linker.run -->
<a id="linker-run"></a>
#### `Linker.run` <sup>method</sup>

```python
def run(self) -> dict[str, list[Link]]
```

Compute links for every symbol, newest message first.

**Returns:** `dict[str, list[Link]]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/linker.py:123`](../../docweave/linker.py#L123) · complexity 29 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Linker.run -->

<!-- docweave:begin sym:owners -->
<a id="owners"></a>
### `owners` <sup>function</sup>

```python
def owners(info: BlameInfo | None, messages: dict[str, Message], top: int=3) -> list[tuple[str, float]]
```

Authors of the surviving lines of a symbol, as ``(name, share)`` pairs.

| Parameter | Type | Default |
| --- | --- | --- |
| `info` | `BlameInfo \| None` |  |
| `messages` | `dict[str, Message]` |  |
| `top` | `int` | `3` |

**Returns:** `list[tuple[str, float]]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/linker.py:178`](../../docweave/linker.py#L178) · complexity 7 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:owners -->
