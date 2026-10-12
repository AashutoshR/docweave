<!-- docweave:begin module -->
# `docweave.changelog`

Group commits into a release-by-release changelog, using classified intent rather than prefixes.

Source: [`docweave/changelog.py`](../../docweave/changelog.py) · 46 lines

**Imports:** [`docweave.config`](docweave.config.md), [`docweave.model`](docweave.model.md)

**Imported by:** [`docweave.cli`](docweave.cli.md), [`docweave.render`](docweave.render.md)
<!-- docweave:end module -->

<!-- docweave:begin contents -->
## Contents

| Symbol | Kind | Summary |
| --- | --- | --- |
| [`Release`](#release) | class | One changelog section: a tagged version, or the unreleased work since the last tag. |
| [`Release.empty`](#release-empty) | method | True when no commit in this release is worth listing. |
| [`is_docs_only`](#is-docs-only) | function | True for commits that only touched generated output, so regenerating docs is a fixpoint. |
| [`build_changelog`](#build-changelog) | function | Split ``commits`` (newest first) into releases at tagged commits, grouped by intent. |

## Reference
<!-- docweave:end contents -->

<!-- docweave:begin sym:Release -->
<a id="release"></a>
### `Release` <sup>class</sup>

```python
@dataclass
class Release
```

One changelog section: a tagged version, or the unreleased work since the last tag.

<sub>[`docweave/changelog.py:12`](../../docweave/changelog.py#L12)</sub>
<!-- docweave:end sym:Release -->

<!-- docweave:begin sym:Release.empty -->
<a id="release-empty"></a>
#### `Release.empty` <sup>method</sup>

```python
@property
def empty(self) -> bool
```

True when no commit in this release is worth listing.

**Returns:** `bool`

<sub>[`docweave/changelog.py:21`](../../docweave/changelog.py#L21) · complexity 2</sub>
<!-- docweave:end sym:Release.empty -->

<!-- docweave:begin sym:is_docs_only -->
<a id="is-docs-only"></a>
### `is_docs_only` <sup>function</sup>

```python
def is_docs_only(cfg: Config, commit: Message) -> bool
```

True for commits that only touched generated output, so regenerating docs is a fixpoint.

| Parameter | Type |
| --- | --- |
| `cfg` | `Config` |
| `commit` | `Message` |

**Returns:** `bool`

<sub>[`docweave/changelog.py:26`](../../docweave/changelog.py#L26) · complexity 3</sub>
<!-- docweave:end sym:is_docs_only -->

<!-- docweave:begin sym:build_changelog -->
<a id="build-changelog"></a>
### `build_changelog` <sup>function</sup>

```python
def build_changelog(cfg: Config, commits: list[Message]) -> list[Release]
```

Split ``commits`` (newest first) into releases at tagged commits, grouped by intent.

| Parameter | Type |
| --- | --- |
| `cfg` | `Config` |
| `commits` | `list[Message]` |

**Returns:** `list[Release]`

<sub>[`docweave/changelog.py:32`](../../docweave/changelog.py#L32) · complexity 9</sub>
<!-- docweave:end sym:build_changelog -->
