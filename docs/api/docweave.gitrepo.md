<!-- docweave:begin module -->
# `docweave.gitrepo`

Read developer communication and line-level authorship out of git.

Source: [`docweave/gitrepo.py`](../../docweave/gitrepo.py) · 182 lines · main authors: AashutoshR (100%)

**Imports:** [`docweave.model`](docweave.model.md)

**Imported by:** [`docweave.cli`](docweave.cli.md), [`docweave.drift`](docweave.drift.md), [`docweave.engine`](docweave.engine.md), [`docweave.linker`](docweave.linker.md)
<!-- docweave:end module -->

<!-- docweave:begin contents -->
## Contents

| Symbol | Kind | Summary |
| --- | --- | --- |
| [`UNCOMMITTED`](#uncommitted) | constant | Uncommitted setting. |
| [`Removal`](#removal) | class | A definition that used to exist: which commit deleted it and what appeared in its place. |
| [`GitRepo`](#gitrepo) | class | Thin, read-only wrapper around the ``git`` command line for one work tree. |
| [`GitRepo.open`](#gitrepo-open) | method | Return a repo handle if ``root`` is inside a git work tree that has at least one commit. |
| [`GitRepo.log`](#gitrepo-log) | method | Commits reachable from HEAD, newest first, with per-file line counts. |
| [`GitRepo.show`](#gitrepo-show) | method | Look up specific commits (those that blame found beyond the history limit). |
| [`GitRepo.blame`](#gitrepo-blame) | method | Commit sha that last touched each line of ``rel`` (index 0 is line 1); None if untracked. |
| [`GitRepo.blame_many`](#gitrepo-blame-many) | method | Blame several files concurrently; untracked files are left out. |
| [`GitRepo.removed_definitions`](#gitrepo-removed-definitions) | method | Names of functions/classes that history shows were deleted or renamed, newest removal first. |
| [`GitRepo.staged_files`](#gitrepo-staged-files) | method | Paths with changes staged for the next commit. |
| [`GitRepo.deleted_files`](#gitrepo-deleted-files) | method | Paths that history shows were deleted, mapped to the commit that deleted them. |
| [`GitRepo.web_url`](#gitrepo-web-url) | method | Browser URL of the ``origin`` remote, for linking commits and pull requests. |
| [`worktree_message`](#worktree-message) | function | Stand-in 'commit' for lines that are modified but not committed yet. |

## Reference
<!-- docweave:end contents -->

<!-- docweave:begin sym:UNCOMMITTED -->
<a id="uncommitted"></a>
### `UNCOMMITTED` <sup>constant</sup>

```python
UNCOMMITTED = '0' * 40
```

Uncommitted setting.

*No docstring in the source - this description is inferred from the name.*

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/gitrepo.py:14`](../../docweave/gitrepo.py#L14) · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:UNCOMMITTED -->

<!-- docweave:begin sym:Removal -->
<a id="removal"></a>
### `Removal` <sup>class</sup>

```python
@dataclass
class Removal
```

A definition that used to exist: which commit deleted it and what appeared in its place.

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/gitrepo.py:24`](../../docweave/gitrepo.py#L24) · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:Removal -->

<!-- docweave:begin sym:GitRepo -->
<a id="gitrepo"></a>
### `GitRepo` <sup>class</sup>

```python
class GitRepo
```

Thin, read-only wrapper around the ``git`` command line for one work tree.

| Parameter | Type |
| --- | --- |
| `root` | `Path` |

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/gitrepo.py:41`](../../docweave/gitrepo.py#L41) · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:GitRepo -->

<!-- docweave:begin sym:GitRepo.open -->
<a id="gitrepo-open"></a>
#### `GitRepo.open` <sup>method</sup>

```python
@classmethod
def open(cls, root: Path) -> 'GitRepo | None'
```

Return a repo handle if ``root`` is inside a git work tree that has at least one commit.

| Parameter | Type |
| --- | --- |
| `root` | `Path` |

**Returns:** `'GitRepo | None'`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/gitrepo.py:48`](../../docweave/gitrepo.py#L48) · complexity 3 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:GitRepo.open -->

<!-- docweave:begin sym:GitRepo.log -->
<a id="gitrepo-log"></a>
#### `GitRepo.log` <sup>method</sup>

```python
def log(self, limit: int) -> list[Message]
```

Commits reachable from HEAD, newest first, with per-file line counts.

| Parameter | Type |
| --- | --- |
| `limit` | `int` |

**Returns:** `list[Message]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/gitrepo.py:91`](../../docweave/gitrepo.py#L91) · complexity 1 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:GitRepo.log -->

<!-- docweave:begin sym:GitRepo.show -->
<a id="gitrepo-show"></a>
#### `GitRepo.show` <sup>method</sup>

```python
def show(self, shas: list[str]) -> list[Message]
```

Look up specific commits (those that blame found beyond the history limit).

| Parameter | Type |
| --- | --- |
| `shas` | `list[str]` |

**Returns:** `list[Message]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/gitrepo.py:96`](../../docweave/gitrepo.py#L96) · complexity 2 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:GitRepo.show -->

<!-- docweave:begin sym:GitRepo.blame -->
<a id="gitrepo-blame"></a>
#### `GitRepo.blame` <sup>method</sup>

```python
def blame(self, rel: str) -> list[str] | None
```

Commit sha that last touched each line of ``rel`` (index 0 is line 1); None if untracked.

| Parameter | Type |
| --- | --- |
| `rel` | `str` |

**Returns:** `list[str] | None`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/gitrepo.py:104`](../../docweave/gitrepo.py#L104) · complexity 5 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:GitRepo.blame -->

<!-- docweave:begin sym:GitRepo.blame_many -->
<a id="gitrepo-blame-many"></a>
#### `GitRepo.blame_many` <sup>method</sup>

```python
def blame_many(self, files: list[str]) -> dict[str, list[str]]
```

Blame several files concurrently; untracked files are left out.

| Parameter | Type |
| --- | --- |
| `files` | `list[str]` |

**Returns:** `dict[str, list[str]]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/gitrepo.py:119`](../../docweave/gitrepo.py#L119) · complexity 3 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:GitRepo.blame_many -->

<!-- docweave:begin sym:GitRepo.removed_definitions -->
<a id="gitrepo-removed-definitions"></a>
#### `GitRepo.removed_definitions` <sup>method</sup>

```python
def removed_definitions(self, limit: int) -> dict[str, Removal]
```

Names of functions/classes that history shows were deleted or renamed, newest removal first.

A definition counts as removed when a commit deletes its ``def``/``class``/``function`` line
without adding one for the same name. Definitions added by that same commit to the same
file are recorded as likely replacements (that is what a rename looks like in a diff).

| Parameter | Type |
| --- | --- |
| `limit` | `int` |

**Returns:** `dict[str, Removal]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/gitrepo.py:125`](../../docweave/gitrepo.py#L125) · complexity 9 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:GitRepo.removed_definitions -->

<!-- docweave:begin sym:GitRepo.staged_files -->
<a id="gitrepo-staged-files"></a>
#### `GitRepo.staged_files` <sup>method</sup>

```python
def staged_files(self) -> list[str]
```

Paths with changes staged for the next commit.

**Returns:** `list[str]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/gitrepo.py:153`](../../docweave/gitrepo.py#L153) · complexity 3 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:GitRepo.staged_files -->

<!-- docweave:begin sym:GitRepo.deleted_files -->
<a id="gitrepo-deleted-files"></a>
#### `GitRepo.deleted_files` <sup>method</sup>

```python
def deleted_files(self, limit: int) -> dict[str, str]
```

Paths that history shows were deleted, mapped to the commit that deleted them.

| Parameter | Type |
| --- | --- |
| `limit` | `int` |

**Returns:** `dict[str, str]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/gitrepo.py:157`](../../docweave/gitrepo.py#L157) · complexity 5 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:GitRepo.deleted_files -->

<!-- docweave:begin sym:GitRepo.web_url -->
<a id="gitrepo-web-url"></a>
#### `GitRepo.web_url` <sup>method</sup>

```python
def web_url(self) -> str | None
```

Browser URL of the ``origin`` remote, for linking commits and pull requests.

**Returns:** `str | None`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/gitrepo.py:167`](../../docweave/gitrepo.py#L167) · complexity 3 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:GitRepo.web_url -->

<!-- docweave:begin sym:worktree_message -->
<a id="worktree-message"></a>
### `worktree_message` <sup>function</sup>

```python
def worktree_message() -> Message
```

Stand-in 'commit' for lines that are modified but not committed yet.

**Returns:** `Message`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/gitrepo.py:176`](../../docweave/gitrepo.py#L176) · complexity 1 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:worktree_message -->
