<!-- docweave:begin module -->
# `docweave.changelog`

Group commits into a release-by-release changelog, using classified intent rather than prefixes.

Source: [`docweave/changelog.py`](../../docweave/changelog.py) · 46 lines · main authors: AashutoshR (100%)

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

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/changelog.py:12`](../../docweave/changelog.py#L12) · written by AashutoshR (100%)</sub>
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

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/changelog.py:21`](../../docweave/changelog.py#L21) · complexity 2 · written by AashutoshR (100%)</sub>
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

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/changelog.py:26`](../../docweave/changelog.py#L26) · complexity 3 · written by AashutoshR (100%)</sub>
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

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/changelog.py:32`](../../docweave/changelog.py#L32) · complexity 9 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:build_changelog -->
