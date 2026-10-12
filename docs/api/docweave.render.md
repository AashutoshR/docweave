<!-- docweave:begin module -->
# `docweave.render`

Render an :class:`~docweave.engine.Analysis` as a Markdown documentation site.

Every page is a list of ``(block_id, markdown)`` pairs. Blocks are written inside managed-region
markers (see :mod:`docweave.regions`), which is what lets regeneration update the page in place
while keeping anything a person added around them. Output is deterministic - no timestamps - so
an unchanged project regenerates byte-identical docs and ``git diff`` stays quiet.

Source: [`docweave/render.py`](../../docweave/render.py) · 468 lines · main authors: AashutoshR (100%)

**Imports:** [`docweave`](docweave.md), [`docweave.changelog`](docweave.changelog.md), [`docweave.drift`](docweave.drift.md), [`docweave.engine`](docweave.engine.md), [`docweave.graph`](docweave.graph.md), [`docweave.linker`](docweave.linker.md), [`docweave.model`](docweave.model.md), [`docweave.nlp.describe`](docweave.nlp.describe.md), [`docweave.nlp.docstring`](docweave.nlp.docstring.md), [`docweave.nlp.intent`](docweave.nlp.intent.md), [`docweave.nlp.rationale`](docweave.nlp.rationale.md), [`docweave.nlp.text`](docweave.nlp.text.md), [`docweave.regions`](docweave.regions.md)

**Imported by:** [`docweave.cli`](docweave.cli.md)
<!-- docweave:end module -->

<!-- docweave:begin contents -->
## Contents

| Symbol | Kind | Summary |
| --- | --- | --- |
| [`Renderer`](#renderer) | class | Turns one analysis into the blocks of every documentation page. |
| [`Renderer.module_page`](#renderer-module-page) | method | Path of the API page for a module. |
| [`Renderer.rel`](#renderer-rel) | method | Relative link from ``page`` to ``target`` (both relative to the project root). |
| [`Renderer.symbol_link`](#renderer-symbol-link) | method | Markdown link to a symbol's reference entry, or plain code if it has none. |
| [`Renderer.message_ref`](#renderer-message-ref) | method | A message's label, linked to its URL when it has one. |
| [`Renderer.summary_of`](#renderer-summary-of) | method | One-line description of a symbol and where it came from: doc \| ai \| inferred. |
| [`Renderer.module_summary`](#renderer-module-summary) | method | First sentence of the module docstring, or a list of what it defines. |
| [`Renderer.module_owners`](#renderer-module-owners) | method | The top three authors of a module by surviving lines. |
| [`Renderer.coverable`](#renderer-coverable) | method | The module's visible classes, functions and methods - what documentation coverage counts. |
| [`Renderer.visible_modules`](#renderer-visible-modules) | method | Modules that get a page: those with visible symbols or a docstring. |
| [`Renderer.pages`](#renderer-pages) | method | Every page of the site, keyed by its path relative to the project root. |
| [`Renderer.health_line`](#renderer-health-line) | method | One-line health badge linking to the full report. |
| [`Renderer.module_table`](#renderer-module-table) | method | Table of modules with summary, API size, coverage and main authors. |
| [`Renderer.recent_changes`](#renderer-recent-changes) | method | The latest meaningful commits (formatting and chores are skipped) with the API they touch. |
| [`Renderer.index_page`](#renderer-index-page) | method | Landing page: health, project size, module table and recent changes. |
| [`Renderer.symbol_block`](#renderer-symbol-block) | method | Reference entry for one symbol: signature, drift warnings, description, parameters, history. |
| [`Renderer.history`](#renderer-history) | method | The communication linked to a symbol, phrased as an annotated timeline. |
| [`Renderer.api_page`](#renderer-api-page) | method | Reference page for one module: header, table of contents, then one block per symbol. |
| [`Renderer.architecture_page`](#renderer-architecture-page) | method | Dependency graph, import cycles, coupling table and churn-times-complexity hotspots. |
| [`Renderer.changelog_page`](#renderer-changelog-page) | method | Changelog with one block per release, each entry annotated with the API it touched. |
| [`Renderer.decisions_page`](#renderer-decisions-page) | method | Decision log: messages that explain a choice, newest first, linked to the code they shaped. |
| [`Renderer.health_page`](#renderer-health-page) | method | Health report: score, every drift issue by severity, and per-module coverage. |
| [`Renderer.inject_blocks`](#renderer-inject-blocks) | method | Blocks that can be embedded in hand-written files (README etc.) via region markers. |
| [`render`](#render) | function | Produce the final text of every documentation file, merged with what is already on disk. |
| [`stale_pages`](#stale-pages) | function | Compare rendered ``files`` with disk: returns (changed or new files, orphaned API pages). |
| [`write`](#write) | function | Write changed files, delete API pages for modules that no longer exist; return both lists. |

## Reference
<!-- docweave:end contents -->

<!-- docweave:begin sym:Renderer -->
<a id="renderer"></a>
### `Renderer` <sup>class</sup>

```python
class Renderer
```

Turns one analysis into the blocks of every documentation page.

| Parameter | Type |
| --- | --- |
| `analysis` | `Analysis` |

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/render.py:47`](../../docweave/render.py#L47) · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Renderer -->

<!-- docweave:begin sym:Renderer.module_page -->
<a id="renderer-module-page"></a>
#### `Renderer.module_page` <sup>method</sup>

```python
def module_page(self, module: str) -> str
```

Path of the API page for a module.

| Parameter | Type |
| --- | --- |
| `module` | `str` |

**Returns:** `str`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/render.py:59`](../../docweave/render.py#L59) · complexity 1 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Renderer.module_page -->

<!-- docweave:begin sym:Renderer.rel -->
<a id="renderer-rel"></a>
#### `Renderer.rel` <sup>method</sup>

```python
def rel(self, page: str, target: str) -> str
```

Relative link from ``page`` to ``target`` (both relative to the project root).

| Parameter | Type |
| --- | --- |
| `page` | `str` |
| `target` | `str` |

**Returns:** `str`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/render.py:63`](../../docweave/render.py#L63) · complexity 1 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Renderer.rel -->

<!-- docweave:begin sym:Renderer.symbol_link -->
<a id="renderer-symbol-link"></a>
#### `Renderer.symbol_link` <sup>method</sup>

```python
def symbol_link(self, page: str, sid: str) -> str
```

Markdown link to a symbol's reference entry, or plain code if it has none.

| Parameter | Type |
| --- | --- |
| `page` | `str` |
| `sid` | `str` |

**Returns:** `str`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/render.py:67`](../../docweave/render.py#L67) · complexity 2 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Renderer.symbol_link -->

<!-- docweave:begin sym:Renderer.message_ref -->
<a id="renderer-message-ref"></a>
#### `Renderer.message_ref` <sup>method</sup>

```python
def message_ref(self, msg: Message) -> str
```

A message's label, linked to its URL when it has one.

| Parameter | Type |
| --- | --- |
| `msg` | `Message` |

**Returns:** `str`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/render.py:74`](../../docweave/render.py#L74) · complexity 2 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Renderer.message_ref -->

<!-- docweave:begin sym:Renderer.summary_of -->
<a id="renderer-summary-of"></a>
#### `Renderer.summary_of` <sup>method</sup>

```python
def summary_of(self, sym: Symbol) -> tuple[str, str]
```

One-line description of a symbol and where it came from: doc | ai | inferred.

| Parameter | Type |
| --- | --- |
| `sym` | `Symbol` |

**Returns:** `tuple[str, str]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/render.py:79`](../../docweave/render.py#L79) · complexity 5 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Renderer.summary_of -->

<!-- docweave:begin sym:Renderer.module_summary -->
<a id="renderer-module-summary"></a>
#### `Renderer.module_summary` <sup>method</sup>

```python
def module_summary(self, module: Module) -> str
```

First sentence of the module docstring, or a list of what it defines.

| Parameter | Type |
| --- | --- |
| `module` | `Module` |

**Returns:** `str`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/render.py:87`](../../docweave/render.py#L87) · complexity 7 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Renderer.module_summary -->

<!-- docweave:begin sym:Renderer.module_owners -->
<a id="renderer-module-owners"></a>
#### `Renderer.module_owners` <sup>method</sup>

```python
def module_owners(self, module: Module) -> list[tuple[str, float]]
```

The top three authors of a module by surviving lines.

| Parameter | Type |
| --- | --- |
| `module` | `Module` |

**Returns:** `list[tuple[str, float]]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/render.py:94`](../../docweave/render.py#L94) · complexity 6 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Renderer.module_owners -->

<!-- docweave:begin sym:Renderer.coverable -->
<a id="renderer-coverable"></a>
#### `Renderer.coverable` <sup>method</sup>

```python
def coverable(self, module: Module) -> list[Symbol]
```

The module's visible classes, functions and methods - what documentation coverage counts.

| Parameter | Type |
| --- | --- |
| `module` | `Module` |

**Returns:** `list[Symbol]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/render.py:109`](../../docweave/render.py#L109) · complexity 4 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Renderer.coverable -->

<!-- docweave:begin sym:Renderer.visible_modules -->
<a id="renderer-visible-modules"></a>
#### `Renderer.visible_modules` <sup>method</sup>

```python
def visible_modules(self) -> list[Module]
```

Modules that get a page: those with visible symbols or a docstring.

**Returns:** `list[Module]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/render.py:113`](../../docweave/render.py#L113) · complexity 5 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Renderer.visible_modules -->

<!-- docweave:begin sym:Renderer.pages -->
<a id="renderer-pages"></a>
#### `Renderer.pages` <sup>method</sup>

```python
def pages(self) -> dict[str, Blocks]
```

Every page of the site, keyed by its path relative to the project root.

**Returns:** `dict[str, Blocks]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/render.py:119`](../../docweave/render.py#L119) · complexity 4 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Renderer.pages -->

<!-- docweave:begin sym:Renderer.health_line -->
<a id="renderer-health-line"></a>
#### `Renderer.health_line` <sup>method</sup>

```python
def health_line(self, page: str) -> str
```

One-line health badge linking to the full report.

| Parameter | Type |
| --- | --- |
| `page` | `str` |

**Returns:** `str`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/render.py:134`](../../docweave/render.py#L134) · complexity 2 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Renderer.health_line -->

<!-- docweave:begin sym:Renderer.module_table -->
<a id="renderer-module-table"></a>
#### `Renderer.module_table` <sup>method</sup>

```python
def module_table(self, page: str) -> str
```

Table of modules with summary, API size, coverage and main authors.

| Parameter | Type |
| --- | --- |
| `page` | `str` |

**Returns:** `str`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/render.py:142`](../../docweave/render.py#L142) · complexity 9 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Renderer.module_table -->

<!-- docweave:begin sym:Renderer.recent_changes -->
<a id="renderer-recent-changes"></a>
#### `Renderer.recent_changes` <sup>method</sup>

```python
def recent_changes(self, page: str, limit: int=8) -> str
```

The latest meaningful commits (formatting and chores are skipped) with the API they touch.

| Parameter | Type | Default |
| --- | --- | --- |
| `page` | `str` |  |
| `limit` | `int` | `8` |

**Returns:** `str`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/render.py:156`](../../docweave/render.py#L156) · complexity 9 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Renderer.recent_changes -->

<!-- docweave:begin sym:Renderer.index_page -->
<a id="renderer-index-page"></a>
#### `Renderer.index_page` <sup>method</sup>

```python
def index_page(self) -> Blocks
```

Landing page: health, project size, module table and recent changes.

**Returns:** `Blocks`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/render.py:169`](../../docweave/render.py#L169) · complexity 8 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Renderer.index_page -->

<!-- docweave:begin sym:Renderer.symbol_block -->
<a id="renderer-symbol-block"></a>
#### `Renderer.symbol_block` <sup>method</sup>

```python
def symbol_block(self, page: str, sym: Symbol) -> str
```

Reference entry for one symbol: signature, drift warnings, description, parameters, history.

| Parameter | Type |
| --- | --- |
| `page` | `str` |
| `sym` | `Symbol` |

**Returns:** `str`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/render.py:188`](../../docweave/render.py#L188) · complexity 41 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Renderer.symbol_block -->

<!-- docweave:begin sym:Renderer.history -->
<a id="renderer-history"></a>
#### `Renderer.history` <sup>method</sup>

```python
def history(self, page: str, sym: Symbol, limit: int=6) -> list[str]
```

The communication linked to a symbol, phrased as an annotated timeline.

| Parameter | Type | Default |
| --- | --- | --- |
| `page` | `str` |  |
| `sym` | `Symbol` |  |
| `limit` | `int` | `6` |

**Returns:** `list[str]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/render.py:243`](../../docweave/render.py#L243) · complexity 12 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Renderer.history -->

<!-- docweave:begin sym:Renderer.api_page -->
<a id="renderer-api-page"></a>
#### `Renderer.api_page` <sup>method</sup>

```python
def api_page(self, module: Module) -> Blocks
```

Reference page for one module: header, table of contents, then one block per symbol.

| Parameter | Type |
| --- | --- |
| `module` | `Module` |

**Returns:** `Blocks`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/render.py:262`](../../docweave/render.py#L262) · complexity 18 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Renderer.api_page -->

<!-- docweave:begin sym:Renderer.architecture_page -->
<a id="renderer-architecture-page"></a>
#### `Renderer.architecture_page` <sup>method</sup>

```python
def architecture_page(self) -> Blocks
```

Dependency graph, import cycles, coupling table and churn-times-complexity hotspots.

**Returns:** `Blocks`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/render.py:292`](../../docweave/render.py#L292) · complexity 22 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Renderer.architecture_page -->

<!-- docweave:begin sym:Renderer.changelog_page -->
<a id="renderer-changelog-page"></a>
#### `Renderer.changelog_page` <sup>method</sup>

```python
def changelog_page(self) -> Blocks
```

Changelog with one block per release, each entry annotated with the API it touched.

**Returns:** `Blocks`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/render.py:329`](../../docweave/render.py#L329) · complexity 11 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Renderer.changelog_page -->

<!-- docweave:begin sym:Renderer.decisions_page -->
<a id="renderer-decisions-page"></a>
#### `Renderer.decisions_page` <sup>method</sup>

```python
def decisions_page(self) -> Blocks
```

Decision log: messages that explain a choice, newest first, linked to the code they shaped.

**Returns:** `Blocks`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/render.py:351`](../../docweave/render.py#L351) · complexity 17 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Renderer.decisions_page -->

<!-- docweave:begin sym:Renderer.health_page -->
<a id="renderer-health-page"></a>
#### `Renderer.health_page` <sup>method</sup>

```python
def health_page(self) -> Blocks
```

Health report: score, every drift issue by severity, and per-module coverage.

**Returns:** `Blocks`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/render.py:377`](../../docweave/render.py#L377) · complexity 16 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Renderer.health_page -->

<!-- docweave:begin sym:Renderer.inject_blocks -->
<a id="renderer-inject-blocks"></a>
#### `Renderer.inject_blocks` <sup>method</sup>

```python
def inject_blocks(self, page: str) -> Blocks
```

Blocks that can be embedded in hand-written files (README etc.) via region markers.

| Parameter | Type |
| --- | --- |
| `page` | `str` |

**Returns:** `Blocks`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/render.py:411`](../../docweave/render.py#L411) · complexity 3 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Renderer.inject_blocks -->

<!-- docweave:begin sym:render -->
<a id="render"></a>
### `render` <sup>function</sup>

```python
def render(analysis: Analysis) -> dict[str, str]
```

Produce the final text of every documentation file, merged with what is already on disk.

| Parameter | Type |
| --- | --- |
| `analysis` | `Analysis` |

**Returns:** `dict[str, str]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/render.py:421`](../../docweave/render.py#L421) · complexity 6 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:render -->

<!-- docweave:begin sym:stale_pages -->
<a id="stale-pages"></a>
### `stale_pages` <sup>function</sup>

```python
def stale_pages(cfg, files: dict[str, str]) -> tuple[list[str], list[str]]
```

Compare rendered ``files`` with disk: returns (changed or new files, orphaned API pages).

| Parameter | Type |
| --- | --- |
| `cfg` |  |
| `files` | `dict[str, str]` |

**Returns:** `tuple[list[str], list[str]]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/render.py:440`](../../docweave/render.py#L440) · complexity 9 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:stale_pages -->

<!-- docweave:begin sym:write -->
<a id="write"></a>
### `write` <sup>function</sup>

```python
def write(cfg, files: dict[str, str]) -> tuple[list[str], list[str]]
```

Write changed files, delete API pages for modules that no longer exist; return both lists.

| Parameter | Type |
| --- | --- |
| `cfg` |  |
| `files` | `dict[str, str]` |

**Returns:** `tuple[list[str], list[str]]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/render.py:458`](../../docweave/render.py#L458) · complexity 3 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:write -->
