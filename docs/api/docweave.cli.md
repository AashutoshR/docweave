<!-- docweave:begin module -->
# `docweave.cli`

Command-line interface: ``docweave <command>``.

Source: [`docweave/cli.py`](../../docweave/cli.py) · 339 lines · main authors: AashutoshR (100%)

**Imports:** [`docweave`](docweave.md), [`docweave.analyzers`](docweave.analyzers.md), [`docweave.changelog`](docweave.changelog.md), [`docweave.comms`](docweave.comms.md), [`docweave.config`](docweave.config.md), [`docweave.drift`](docweave.drift.md), [`docweave.engine`](docweave.engine.md), [`docweave.gitrepo`](docweave.gitrepo.md), [`docweave.hooks`](docweave.hooks.md), [`docweave.linker`](docweave.linker.md), [`docweave.llm`](docweave.llm.md), [`docweave.nlp.intent`](docweave.nlp.intent.md), [`docweave.nlp.rationale`](docweave.nlp.rationale.md), [`docweave.render`](docweave.render.md), [`docweave.search`](docweave.search.md)

**Imported by:** `docweave.__main__`
<!-- docweave:end module -->

<!-- docweave:begin contents -->
## Contents

| Symbol | Kind | Summary |
| --- | --- | --- |
| [`cmd_init`](#cmd-init) | function | Write a starter docweave.toml and, on request, the CI workflow and git hook. |
| [`cmd_generate`](#cmd-generate) | function | Analyse the project and write the documentation site. |
| [`cmd_check`](#cmd-check) | function | Report drift in the chosen format and return 1 if anything reaches the failure threshold. |
| [`cmd_why`](#cmd-why) | function | Print who wrote a symbol, what is wrong with its docs, and the discussion linked to it. |
| [`cmd_ask`](#cmd-ask) | function | Answer a question with the best-matching symbols and discussions. |
| [`cmd_changelog`](#cmd-changelog) | function | Print the changelog to standard output without writing any files. |
| [`cmd_hook`](#cmd-hook) | function | Install or remove the pre-commit hook. |
| [`cmd_comms`](#cmd-comms) | function | Export pull requests and issues from GitHub into the comms folder. |
| [`cmd_watch`](#cmd-watch) | function | Poll source and Markdown files and regenerate the docs whenever one changes. |
| [`build_parser`](#build-parser) | function | Define the command-line interface. |
| [`main`](#main) | function | Entry point: parse arguments, run the command, return its exit code. |

## Reference
<!-- docweave:end contents -->

<!-- docweave:begin sym:cmd_init -->
<a id="cmd-init"></a>
### `cmd_init` <sup>function</sup>

```python
def cmd_init(args) -> int
```

Write a starter docweave.toml and, on request, the CI workflow and git hook.

| Parameter |
| --- |
| `args` |

**Returns:** `int`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/cli.py:73`](../../docweave/cli.py#L73) · complexity 4 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:cmd_init -->

<!-- docweave:begin sym:cmd_generate -->
<a id="cmd-generate"></a>
### `cmd_generate` <sup>function</sup>

```python
def cmd_generate(args) -> int
```

Analyse the project and write the documentation site.

| Parameter |
| --- |
| `args` |

**Returns:** `int`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/cli.py:90`](../../docweave/cli.py#L90) · complexity 1 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:cmd_generate -->

<!-- docweave:begin sym:cmd_check -->
<a id="cmd-check"></a>
### `cmd_check` <sup>function</sup>

```python
def cmd_check(args) -> int
```

Report drift in the chosen format and return 1 if anything reaches the failure threshold.

| Parameter |
| --- |
| `args` |

**Returns:** `int`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/cli.py:96`](../../docweave/cli.py#L96) · complexity 26 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:cmd_check -->

<!-- docweave:begin sym:cmd_why -->
<a id="cmd-why"></a>
### `cmd_why` <sup>function</sup>

```python
def cmd_why(args) -> int
```

Print who wrote a symbol, what is wrong with its docs, and the discussion linked to it.

| Parameter |
| --- |
| `args` |

**Returns:** `int`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/cli.py:145`](../../docweave/cli.py#L145) · complexity 14 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:cmd_why -->

<!-- docweave:begin sym:cmd_ask -->
<a id="cmd-ask"></a>
### `cmd_ask` <sup>function</sup>

```python
def cmd_ask(args) -> int
```

Answer a question with the best-matching symbols and discussions.

| Parameter |
| --- |
| `args` |

**Returns:** `int`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/cli.py:169`](../../docweave/cli.py#L169) · complexity 8 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:cmd_ask -->

<!-- docweave:begin sym:cmd_changelog -->
<a id="cmd-changelog"></a>
### `cmd_changelog` <sup>function</sup>

```python
def cmd_changelog(args) -> int
```

Print the changelog to standard output without writing any files.

| Parameter |
| --- |
| `args` |

**Returns:** `int`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/cli.py:193`](../../docweave/cli.py#L193) · complexity 9 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:cmd_changelog -->

<!-- docweave:begin sym:cmd_hook -->
<a id="cmd-hook"></a>
### `cmd_hook` <sup>function</sup>

```python
def cmd_hook(args) -> int
```

Install or remove the pre-commit hook.

| Parameter |
| --- |
| `args` |

**Returns:** `int`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/cli.py:211`](../../docweave/cli.py#L211) · complexity 4 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:cmd_hook -->

<!-- docweave:begin sym:cmd_comms -->
<a id="cmd-comms"></a>
### `cmd_comms` <sup>function</sup>

```python
def cmd_comms(args) -> int
```

Export pull requests and issues from GitHub into the comms folder.

| Parameter |
| --- |
| `args` |

**Returns:** `int`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/cli.py:225`](../../docweave/cli.py#L225) · complexity 3 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:cmd_comms -->

<!-- docweave:begin sym:cmd_watch -->
<a id="cmd-watch"></a>
### `cmd_watch` <sup>function</sup>

```python
def cmd_watch(args) -> int
```

Poll source and Markdown files and regenerate the docs whenever one changes.

| Parameter |
| --- |
| `args` |

**Returns:** `int`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/cli.py:237`](../../docweave/cli.py#L237) · complexity 16 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:cmd_watch -->

<!-- docweave:begin sym:build_parser -->
<a id="build-parser"></a>
### `build_parser` <sup>function</sup>

```python
def build_parser() -> argparse.ArgumentParser
```

Define the command-line interface.

**Returns:** `argparse.ArgumentParser`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/cli.py:265`](../../docweave/cli.py#L265) · complexity 1 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:build_parser -->

<!-- docweave:begin sym:main -->
<a id="main"></a>
### `main` <sup>function</sup>

```python
def main(argv: list[str] | None=None) -> int
```

Entry point: parse arguments, run the command, return its exit code.

| Parameter | Type | Default |
| --- | --- | --- |
| `argv` | `list[str] \| None` | `None` |

**Returns:** `int`

**Raises:** `ValueError`

<details><summary>History and rationale (1)</summary>

- 2026-10-12 · **feature** · DocWeave, living documentation from code and developer communication ([`00f6a67`](https://github.com/AashutoshR/docweave/commit/00f6a671df46bc2c98a4d65bcaffa2115e4e5d36), AashutoshR)<br>*Why:* Drift detection: docstring claims checked against the code, dangling references in hand-written Markdown traced to the commit that removed them, and blame-based staleness weighted by classified commit intent so that for…

</details>

<sub>[`docweave/cli.py:326`](../../docweave/cli.py#L326) · complexity 5 · written by AashutoshR (100%)</sub>
<!-- docweave:end sym:main -->
