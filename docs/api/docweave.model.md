<!-- docweave:begin module -->
# `docweave.model`

Core data model shared by analyzers, the linker, drift detection and renderers.

Source: [`docweave/model.py`](../../docweave/model.py) · 168 lines

**Imported by:** [`docweave.analyzers`](docweave.analyzers.md), [`docweave.analyzers.javascript`](docweave.analyzers.javascript.md), [`docweave.analyzers.python`](docweave.analyzers.python.md), [`docweave.changelog`](docweave.changelog.md), [`docweave.comms`](docweave.comms.md), [`docweave.drift`](docweave.drift.md), [`docweave.engine`](docweave.engine.md), [`docweave.gitrepo`](docweave.gitrepo.md), [`docweave.graph`](docweave.graph.md), [`docweave.linker`](docweave.linker.md), [`docweave.llm`](docweave.llm.md), [`docweave.render`](docweave.render.md)
<!-- docweave:end module -->

<!-- docweave:begin contents -->
## Contents

| Symbol | Kind | Summary |
| --- | --- | --- |
| [`Param`](#param) | class | One parameter of a function signature. |
| [`Symbol`](#symbol) | class | One documentable unit of code: a class, function, method or constant. |
| [`Symbol.anchor`](#symbol-anchor) | method | HTML anchor used for this symbol on its API page. |
| [`Module`](#module) | class | One analysed source file. |
| [`Project`](#project) | class | All analysed modules of one project. |
| [`Project.symbols`](#project-symbols) | method | Every symbol in the project, keyed by id. |
| [`Project.by_file`](#project-by-file) | method | Modules keyed by file path. |
| [`Message`](#message) | class | A unit of developer communication: a commit, PR, issue, chat message or note. |
| [`Message.sha`](#message-sha) | method | Full commit hash, or None for anything that is not a commit. |
| [`Message.text`](#message-text) | method | Title and body together, as fed to the NLP passes. |
| [`Message.timestamp`](#message-timestamp) | method | Seconds since the epoch (0 when undated), for ordering. |
| [`Message.day`](#message-day) | method | Date as YYYY-MM-DD. |
| [`Message.label`](#message-label) | method | Short human-readable reference: abbreviated hash, ``pr:12`` or ``#channel``. |
| [`Link`](#link) | class | Evidence that a message is about a symbol. |
| [`Issue`](#issue) | class | A detected documentation problem. |
| [`Issue.sort_key`](#issue-sort-key) | method | Order issues by severity, then location. |

## Reference
<!-- docweave:end contents -->

<!-- docweave:begin sym:Param -->
<a id="param"></a>
### `Param` <sup>class</sup>

```python
@dataclass
class Param
```

One parameter of a function signature.

<sub>[`docweave/model.py:10`](../../docweave/model.py#L10)</sub>
<!-- docweave:end sym:Param -->

<!-- docweave:begin sym:Symbol -->
<a id="symbol"></a>
### `Symbol` <sup>class</sup>

```python
@dataclass
class Symbol
```

One documentable unit of code: a class, function, method or constant.

<sub>[`docweave/model.py:20`](../../docweave/model.py#L20)</sub>
<!-- docweave:end sym:Symbol -->

<!-- docweave:begin sym:Symbol.anchor -->
<a id="symbol-anchor"></a>
#### `Symbol.anchor` <sup>method</sup>

```python
@property
def anchor(self) -> str
```

HTML anchor used for this symbol on its API page.

**Returns:** `str`

<sub>[`docweave/model.py:52`](../../docweave/model.py#L52) · complexity 1</sub>
<!-- docweave:end sym:Symbol.anchor -->

<!-- docweave:begin sym:Module -->
<a id="module"></a>
### `Module` <sup>class</sup>

```python
@dataclass
class Module
```

One analysed source file.

<sub>[`docweave/model.py:58`](../../docweave/model.py#L58)</sub>
<!-- docweave:end sym:Module -->

<!-- docweave:begin sym:Project -->
<a id="project"></a>
### `Project` <sup>class</sup>

```python
@dataclass
class Project
```

All analysed modules of one project.

<sub>[`docweave/model.py:72`](../../docweave/model.py#L72)</sub>
<!-- docweave:end sym:Project -->

<!-- docweave:begin sym:Project.symbols -->
<a id="project-symbols"></a>
#### `Project.symbols` <sup>method</sup>

```python
@property
def symbols(self) -> dict[str, Symbol]
```

Every symbol in the project, keyed by id.

**Returns:** `dict[str, Symbol]`

<sub>[`docweave/model.py:79`](../../docweave/model.py#L79) · complexity 3</sub>
<!-- docweave:end sym:Project.symbols -->

<!-- docweave:begin sym:Project.by_file -->
<a id="project-by-file"></a>
#### `Project.by_file` <sup>method</sup>

```python
def by_file(self) -> dict[str, Module]
```

Modules keyed by file path.

**Returns:** `dict[str, Module]`

<sub>[`docweave/model.py:83`](../../docweave/model.py#L83) · complexity 2</sub>
<!-- docweave:end sym:Project.by_file -->

<!-- docweave:begin sym:Message -->
<a id="message"></a>
### `Message` <sup>class</sup>

```python
@dataclass
class Message
```

A unit of developer communication: a commit, PR, issue, chat message or note.

<sub>[`docweave/model.py:89`](../../docweave/model.py#L89)</sub>
<!-- docweave:end sym:Message -->

<!-- docweave:begin sym:Message.sha -->
<a id="message-sha"></a>
#### `Message.sha` <sup>method</sup>

```python
@property
def sha(self) -> str | None
```

Full commit hash, or None for anything that is not a commit.

**Returns:** `str | None`

<sub>[`docweave/model.py:109`](../../docweave/model.py#L109) · complexity 2</sub>
<!-- docweave:end sym:Message.sha -->

<!-- docweave:begin sym:Message.text -->
<a id="message-text"></a>
#### `Message.text` <sup>method</sup>

```python
@property
def text(self) -> str
```

Title and body together, as fed to the NLP passes.

**Returns:** `str`

<sub>[`docweave/model.py:114`](../../docweave/model.py#L114) · complexity 2</sub>
<!-- docweave:end sym:Message.text -->

<!-- docweave:begin sym:Message.timestamp -->
<a id="message-timestamp"></a>
#### `Message.timestamp` <sup>method</sup>

```python
@property
def timestamp(self) -> float
```

Seconds since the epoch (0 when undated), for ordering.

**Returns:** `float`

<sub>[`docweave/model.py:121`](../../docweave/model.py#L121) · complexity 3</sub>
<!-- docweave:end sym:Message.timestamp -->

<!-- docweave:begin sym:Message.day -->
<a id="message-day"></a>
#### `Message.day` <sup>method</sup>

```python
@property
def day(self) -> str
```

Date as YYYY-MM-DD.

**Returns:** `str`

<sub>[`docweave/model.py:129`](../../docweave/model.py#L129) · complexity 2</sub>
<!-- docweave:end sym:Message.day -->

<!-- docweave:begin sym:Message.label -->
<a id="message-label"></a>
#### `Message.label` <sup>method</sup>

```python
@property
def label(self) -> str
```

Short human-readable reference: abbreviated hash, ``pr:12`` or ``#channel``.

**Returns:** `str`

<sub>[`docweave/model.py:134`](../../docweave/model.py#L134) · complexity 6</sub>
<!-- docweave:end sym:Message.label -->

<!-- docweave:begin sym:Link -->
<a id="link"></a>
### `Link` <sup>class</sup>

```python
@dataclass
class Link
```

Evidence that a message is about a symbol.

<sub>[`docweave/model.py:144`](../../docweave/model.py#L144)</sub>
<!-- docweave:end sym:Link -->

<!-- docweave:begin sym:Issue -->
<a id="issue"></a>
### `Issue` <sup>class</sup>

```python
@dataclass
class Issue
```

A detected documentation problem.

<sub>[`docweave/model.py:154`](../../docweave/model.py#L154)</sub>
<!-- docweave:end sym:Issue -->

<!-- docweave:begin sym:Issue.sort_key -->
<a id="issue-sort-key"></a>
#### `Issue.sort_key` <sup>method</sup>

```python
def sort_key(self) -> tuple
```

Order issues by severity, then location.

**Returns:** `tuple`

<sub>[`docweave/model.py:165`](../../docweave/model.py#L165) · complexity 1</sub>
<!-- docweave:end sym:Issue.sort_key -->
