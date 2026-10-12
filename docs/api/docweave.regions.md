<!-- docweave:begin module -->
# `docweave.regions`

Managed regions: let generated and hand-written text share a file without clobbering.

Generated content is wrapped in ``<!-- docweave:begin ID -->`` / ``<!-- docweave:end ID -->``
markers. Regenerating rewrites only what is between markers; everything a person wrote outside
them survives. Blocks for code that no longer exists are removed; new blocks are slotted in after
their natural predecessor.

Source: [`docweave/regions.py`](../../docweave/regions.py) · 72 lines · main authors: AashutoshR (100%)

**Imported by:** [`docweave.render`](docweave.render.md)
<!-- docweave:end module -->

<!-- docweave:begin contents -->
## Contents

| Symbol | Kind | Summary |
| --- | --- | --- |
| [`wrap`](#wrap) | function | Wrap ``body`` in the begin/end markers for ``block_id``. |
| [`region_ids`](#region-ids) | function | Ids of the managed regions present in ``text``, in order. |
| [`strip_regions`](#strip-regions) | function | What remains of a file once every managed region is removed (the hand-written part). |
| [`merge`](#merge) | function | Merge freshly generated ``blocks`` into ``existing`` text. |

## Reference
<!-- docweave:end contents -->

<!-- docweave:begin sym:wrap -->
<a id="wrap"></a>
### `wrap` <sup>function</sup>

```python
def wrap(block_id: str, body: str) -> str
```

Wrap ``body`` in the begin/end markers for ``block_id``.

| Parameter | Type |
| --- | --- |
| `block_id` | `str` |
| `body` | `str` |

**Returns:** `str`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/regions.py:20`](../../docweave/regions.py#L20) · complexity 1 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:wrap -->

<!-- docweave:begin sym:region_ids -->
<a id="region-ids"></a>
### `region_ids` <sup>function</sup>

```python
def region_ids(text: str) -> list[str]
```

Ids of the managed regions present in ``text``, in order.

| Parameter | Type |
| --- | --- |
| `text` | `str` |

**Returns:** `list[str]`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/regions.py:25`](../../docweave/regions.py#L25) · complexity 2 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:region_ids -->

<!-- docweave:begin sym:strip_regions -->
<a id="strip-regions"></a>
### `strip_regions` <sup>function</sup>

```python
def strip_regions(text: str) -> str
```

What remains of a file once every managed region is removed (the hand-written part).

| Parameter | Type |
| --- | --- |
| `text` | `str` |

**Returns:** `str`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/regions.py:30`](../../docweave/regions.py#L30) · complexity 1 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:strip_regions -->

<!-- docweave:begin sym:merge -->
<a id="merge"></a>
### `merge` <sup>function</sup>

```python
def merge(existing: str | None, blocks: list[tuple[str, str]], inject_only: bool=False) -> str
```

Merge freshly generated ``blocks`` into ``existing`` text.

With ``inject_only`` (used for files people own, like the README) nothing is added or removed:
only regions already present in the file are refreshed.

| Parameter | Type | Default |
| --- | --- | --- |
| `existing` | `str \| None` |  |
| `blocks` | `list[tuple[str, str]]` |  |
| `inject_only` | `bool` | `False` |

**Returns:** `str`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/regions.py:35`](../../docweave/regions.py#L35) · complexity 15 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:merge -->
