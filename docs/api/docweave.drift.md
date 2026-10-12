<!-- docweave:begin module -->
# `docweave.drift`

Detect documentation that no longer matches the code.

Five independent detectors, from most to least certain:

1. **Claim checking** - parameters, return values and exceptions a docstring documents are
   compared with what static analysis finds in the signature and body.
2. **Reference rot** - identifiers and paths mentioned in hand-written Markdown are resolved
   against the code; ones that used to exist are traced to the commit that removed them.
3. **Blame staleness** - a docstring is suspect when the code it describes was rewritten by later
   commits. Commit intent weights the evidence: a ``fix`` or ``feat`` counts, a reformat does not.
4. **Prose staleness** - the same test applied to Markdown lines that mention a symbol.
5. **Anchored signatures** - without git, a state file remembers the signature each docstring
   was written against.

Source: [`docweave/drift.py`](../../docweave/drift.py) · 395 lines · main authors: AashutoshR (100%)

**Imports:** [`docweave.analyzers`](docweave.analyzers.md), [`docweave.config`](docweave.config.md), [`docweave.gitrepo`](docweave.gitrepo.md), [`docweave.linker`](docweave.linker.md), [`docweave.model`](docweave.model.md), [`docweave.nlp.docstring`](docweave.nlp.docstring.md), [`docweave.nlp.intent`](docweave.nlp.intent.md)

**Imported by:** [`docweave.cli`](docweave.cli.md), [`docweave.engine`](docweave.engine.md), [`docweave.render`](docweave.render.md)
<!-- docweave:end module -->

<!-- docweave:begin contents -->
## Contents

| Symbol | Kind | Summary |
| --- | --- | --- |
| [`SEVERITIES`](#severities) | constant | Severities setting. |
| [`ISSUE_HELP`](#issue-help) | constant | Issue help setting. |
| [`Reference`](#reference) | class | A mention of code found in hand-written Markdown. |
| [`Health`](#health) | class | Documentation quality in numbers. |
| [`Health.coverage`](#health-coverage) | method | Share of public symbols that have documentation. |
| [`check_claims`](#check-claims) | function | Compare what a docstring claims about a function with what the code does. |
| [`check_staleness`](#check-staleness) | function | Flag a docstring whose code was rewritten by meaningful commits after it was last edited. |
| [`name_index`](#name-index) | function | Every way prose might spell a symbol: bare name, qualified name, fully dotted path. |
| [`resolve_name`](#resolve-name) | function | Resolve a dotted name from prose to symbol ids, tolerating a partial module prefix. |
| [`scan_markdown`](#scan-markdown) | function | Find code references in hand-written Markdown. |
| [`check_references`](#check-references) | function | Turn Markdown references into issues: dangling names, missing paths and stale prose. |
| [`load_state`](#load-state) | function | Read the signature anchors saved by the last ``generate`` (empty if there are none). |
| [`next_state`](#next-state) | function | Remember, per symbol, the signature its current docstring was written against. |
| [`save_state`](#save-state) | function | Persist signature anchors so the next run can compare against them. |
| [`check_anchors`](#check-anchors) | function | Flag documented symbols whose signature differs from the one their docstring was written for. |
| [`is_documented`](#is-documented) | function | True if the symbol has a non-empty docstring. |
| [`detect`](#detect) | function | Run every detector and return de-duplicated issues, most severe first. |
| [`health`](#health) | function | Summarise documentation quality as a 0-100 score: 40% coverage, 60% freshness. |

## Reference
<!-- docweave:end contents -->

<!-- docweave:begin sym:SEVERITIES -->
<a id="severities"></a>
### `SEVERITIES` <sup>constant</sup>

```python
SEVERITIES = ('high', 'medium', 'low')
```

Severities setting.

*No docstring in the source - this description is inferred from the name.*

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/drift.py:33`](../../docweave/drift.py#L33) · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:SEVERITIES -->

<!-- docweave:begin sym:ISSUE_HELP -->
<a id="issue-help"></a>
### `ISSUE_HELP` <sup>constant</sup>

```python
ISSUE_HELP = {'param-not-in-signature': 'The docstring documents a parameter the function ...
```

Issue help setting.

*No docstring in the source - this description is inferred from the name.*

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/drift.py:44`](../../docweave/drift.py#L44) · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:ISSUE_HELP -->

<!-- docweave:begin sym:Reference -->
<a id="reference"></a>
### `Reference` <sup>class</sup>

```python
@dataclass
class Reference
```

A mention of code found in hand-written Markdown.

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/drift.py:60`](../../docweave/drift.py#L60) · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Reference -->

<!-- docweave:begin sym:Health -->
<a id="health"></a>
### `Health` <sup>class</sup>

```python
@dataclass
class Health
```

Documentation quality in numbers.

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/drift.py:70`](../../docweave/drift.py#L70) · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Health -->

<!-- docweave:begin sym:Health.coverage -->
<a id="health-coverage"></a>
#### `Health.coverage` <sup>method</sup>

```python
@property
def coverage(self) -> float
```

Share of public symbols that have documentation.

**Returns:** `float`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/drift.py:79`](../../docweave/drift.py#L79) · complexity 2 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Health.coverage -->

<!-- docweave:begin sym:check_claims -->
<a id="check-claims"></a>
### `check_claims` <sup>function</sup>

```python
def check_claims(sym: Symbol) -> list[Issue]
```

Compare what a docstring claims about a function with what the code does.

| Parameter | Type |
| --- | --- |
| `sym` | `Symbol` |

**Returns:** `list[Issue]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/drift.py:88`](../../docweave/drift.py#L88) · complexity 31 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:check_claims -->

<!-- docweave:begin sym:check_staleness -->
<a id="check-staleness"></a>
### `check_staleness` <sup>function</sup>

```python
def check_staleness(sym: Symbol, info: BlameInfo | None, messages: dict[str, Message]) -> Issue | None
```

Flag a docstring whose code was rewritten by meaningful commits after it was last edited.

| Parameter | Type |
| --- | --- |
| `sym` | `Symbol` |
| `info` | `BlameInfo \| None` |
| `messages` | `dict[str, Message]` |

**Returns:** `Issue | None`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/drift.py:150`](../../docweave/drift.py#L150) · complexity 15 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:check_staleness -->

<!-- docweave:begin sym:name_index -->
<a id="name-index"></a>
### `name_index` <sup>function</sup>

```python
def name_index(project: Project) -> dict[str, list[str]]
```

Every way prose might spell a symbol: bare name, qualified name, fully dotted path.

| Parameter | Type |
| --- | --- |
| `project` | `Project` |

**Returns:** `dict[str, list[str]]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/drift.py:174`](../../docweave/drift.py#L174) · complexity 4 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:name_index -->

<!-- docweave:begin sym:resolve_name -->
<a id="resolve-name"></a>
### `resolve_name` <sup>function</sup>

```python
def resolve_name(name: str, index: dict[str, list[str]], module_names: set[str]) -> list[str]
```

Resolve a dotted name from prose to symbol ids, tolerating a partial module prefix.

| Parameter | Type |
| --- | --- |
| `name` | `str` |
| `index` | `dict[str, list[str]]` |
| `module_names` | `set[str]` |

**Returns:** `list[str]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/drift.py:184`](../../docweave/drift.py#L184) · complexity 7 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:resolve_name -->

<!-- docweave:begin sym:scan_markdown -->
<a id="scan-markdown"></a>
### `scan_markdown` <sup>function</sup>

```python
def scan_markdown(cfg: Config, project: Project) -> tuple[list[Reference], list[tuple[str, int, str]]]
```

Find code references in hand-written Markdown.

Returns resolved/unresolved identifier references, plus ``(file, line, path)`` for path-like
spans. Generated output, changelogs and DocWeave-managed regions are skipped.

| Parameter | Type |
| --- | --- |
| `cfg` | `Config` |
| `project` | `Project` |

**Returns:** `tuple[list[Reference], list[tuple[str, int, str]]]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/drift.py:196`](../../docweave/drift.py#L196) · complexity 18 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:scan_markdown -->

<!-- docweave:begin sym:check_references -->
<a id="check-references"></a>
### `check_references` <sup>function</sup>

```python
def check_references(cfg: Config, project: Project, references: list[Reference], paths: list[tuple[str, int, str]], graveyard: dict[str, Removal], deleted: dict[str, str], messages: dict[str, Message], blame: dict[str, list[str]], blame_info: dict[str, BlameInfo]) -> list[Issue]
```

Turn Markdown references into issues: dangling names, missing paths and stale prose.

| Parameter | Type |
| --- | --- |
| `cfg` | `Config` |
| `project` | `Project` |
| `references` | `list[Reference]` |
| `paths` | `list[tuple[str, int, str]]` |
| `graveyard` | `dict[str, Removal]` |
| `deleted` | `dict[str, str]` |
| `messages` | `dict[str, Message]` |
| `blame` | `dict[str, list[str]]` |
| `blame_info` | `dict[str, BlameInfo]` |

**Returns:** `list[Issue]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/drift.py:232`](../../docweave/drift.py#L232) · complexity 45 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:check_references -->

<!-- docweave:begin sym:load_state -->
<a id="load-state"></a>
### `load_state` <sup>function</sup>

```python
def load_state(cfg: Config) -> dict
```

Read the signature anchors saved by the last ``generate`` (empty if there are none).

| Parameter | Type |
| --- | --- |
| `cfg` | `Config` |

**Returns:** `dict`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/drift.py:310`](../../docweave/drift.py#L310) · complexity 2 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:load_state -->

<!-- docweave:begin sym:next_state -->
<a id="next-state"></a>
### `next_state` <sup>function</sup>

```python
def next_state(project: Project, previous: dict) -> dict
```

Remember, per symbol, the signature its current docstring was written against.

| Parameter | Type |
| --- | --- |
| `project` | `Project` |
| `previous` | `dict` |

**Returns:** `dict`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/drift.py:319`](../../docweave/drift.py#L319) · complexity 4 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:next_state -->

<!-- docweave:begin sym:save_state -->
<a id="save-state"></a>
### `save_state` <sup>function</sup>

```python
def save_state(cfg: Config, state: dict) -> None
```

Persist signature anchors so the next run can compare against them.

| Parameter | Type |
| --- | --- |
| `cfg` | `Config` |
| `state` | `dict` |

**Returns:** `None`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/drift.py:330`](../../docweave/drift.py#L330) · complexity 1 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:save_state -->

<!-- docweave:begin sym:check_anchors -->
<a id="check-anchors"></a>
### `check_anchors` <sup>function</sup>

```python
def check_anchors(project: Project, state: dict) -> list[Issue]
```

Flag documented symbols whose signature differs from the one their docstring was written for.

| Parameter | Type |
| --- | --- |
| `project` | `Project` |
| `state` | `dict` |

**Returns:** `list[Issue]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/drift.py:337`](../../docweave/drift.py#L337) · complexity 6 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:check_anchors -->

<!-- docweave:begin sym:is_documented -->
<a id="is-documented"></a>
### `is_documented` <sup>function</sup>

```python
def is_documented(sym: Symbol) -> bool
```

True if the symbol has a non-empty docstring.

| Parameter | Type |
| --- | --- |
| `sym` | `Symbol` |

**Returns:** `bool`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/drift.py:350`](../../docweave/drift.py#L350) · complexity 2 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:is_documented -->

<!-- docweave:begin sym:detect -->
<a id="detect"></a>
### `detect` <sup>function</sup>

```python
def detect(cfg: Config, project: Project, messages: dict[str, Message], blame: dict[str, list[str]], blame_info: dict[str, BlameInfo], graveyard: dict[str, Removal], deleted: dict[str, str], state: dict) -> tuple[list[Issue], list[Reference]]
```

Run every detector and return de-duplicated issues, most severe first.

| Parameter | Type |
| --- | --- |
| `cfg` | `Config` |
| `project` | `Project` |
| `messages` | `dict[str, Message]` |
| `blame` | `dict[str, list[str]]` |
| `blame_info` | `dict[str, BlameInfo]` |
| `graveyard` | `dict[str, Removal]` |
| `deleted` | `dict[str, str]` |
| `state` | `dict` |

**Returns:** `tuple[list[Issue], list[Reference]]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/drift.py:355`](../../docweave/drift.py#L355) · complexity 14 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:detect -->

<!-- docweave:begin sym:health -->
<a id="health"></a>
### `health` <sup>function</sup>

```python
def health(cfg: Config, project: Project, issues: list[Issue]) -> Health
```

Summarise documentation quality as a 0-100 score: 40% coverage, 60% freshness.

Coverage counts classes, functions and methods; constants are documented when they have a
comment but are not held against the score when they do not.

| Parameter | Type |
| --- | --- |
| `cfg` | `Config` |
| `project` | `Project` |
| `issues` | `list[Issue]` |

**Returns:** `Health`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/drift.py:382`](../../docweave/drift.py#L382) · complexity 13 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:health -->
