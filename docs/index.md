<!-- docweave:begin title -->
# DocWeave documentation
<!-- docweave:end title -->

<!-- docweave:begin health -->
**Documentation health: 100/100** · 100% of 144 public symbols documented · 0 drift issues ([report](health.md))
<!-- docweave:end health -->

<!-- docweave:begin overview -->
27 modules · 234 symbols · 3855 lines of python · no git history available, so rationale and staleness tracking are limited

[Architecture](architecture.md) · [Health report](health.md)
<!-- docweave:end overview -->

<!-- docweave:begin modules -->
## Modules

| Module | What it does | Public API | Documented |
| --- | --- | ---: | ---: |
| [`docweave`](api/docweave.md) | DocWeave: living documentation woven from code structure and developer communication. | 0 | - |
| [`docweave.analyzers`](api/docweave.analyzers.md) | Language analyzers and source discovery. | 3 | 100% |
| [`docweave.analyzers.javascript`](api/docweave.analyzers.javascript.md) | Structural analysis of JavaScript / TypeScript. | 3 | 100% |
| [`docweave.analyzers.python`](api/docweave.analyzers.python.md) | Static analysis of Python source using the standard ``ast`` module. | 2 | 100% |
| [`docweave.changelog`](api/docweave.changelog.md) | Group commits into a release-by-release changelog, using classified intent rather than prefixes. | 4 | 100% |
| [`docweave.cli`](api/docweave.cli.md) | Command-line interface: ``docweave <command>``. | 11 | 100% |
| [`docweave.comms`](api/docweave.comms.md) | Load developer communication that lives outside git: PRs, issues, chat exports, notes. | 2 | 100% |
| [`docweave.config`](api/docweave.config.md) | Configuration: defaults, overridden by ``docweave.toml`` or ``[tool.docweave]`` in pyproject. | 4 | 100% |
| [`docweave.drift`](api/docweave.drift.md) | Detect documentation that no longer matches the code. | 16 | 100% |
| [`docweave.engine`](api/docweave.engine.md) | The analysis pipeline: code structure + developer communication -> one linked model. | 5 | 100% |
| [`docweave.gitrepo`](api/docweave.gitrepo.md) | Read developer communication and line-level authorship out of git. | 12 | 100% |
| [`docweave.graph`](api/docweave.graph.md) | Module dependency graph: internal edges, external dependencies, cycles and a Mermaid drawing. | 4 | 100% |
| [`docweave.hooks`](api/docweave.hooks.md) | Keep docs in sync automatically: a git pre-commit hook and a CI workflow template. | 3 | 100% |
| [`docweave.linker`](api/docweave.linker.md) | Link developer communication to the code it is about. | 7 | 100% |
| [`docweave.llm`](api/docweave.llm.md) | Optional AI layer (``--llm``): Claude writes summaries for code nobody documented. | 3 | 100% |
| [`docweave.model`](api/docweave.model.md) | Core data model shared by analyzers, the linker, drift detection and renderers. | 16 | 100% |
| [`docweave.nlp`](api/docweave.nlp.md) | Dependency-free NLP building blocks: tokenising, intent, docstrings, rationale, retrieval. | 0 | - |
| [`docweave.nlp.describe`](api/docweave.nlp.describe.md) | Synthesise a one-line description for symbols nobody documented. | 1 | 100% |
| [`docweave.nlp.docstring`](api/docweave.nlp.docstring.md) | Parse docstrings (Google, NumPy, Sphinx and JSDoc styles) into structured claims. | 2 | 100% |
| [`docweave.nlp.index`](api/docweave.nlp.index.md) | A small inverted index offering BM25 ranking and TF-IDF cosine similarity. | 5 | 100% |
| [`docweave.nlp.intent`](api/docweave.nlp.intent.md) | Classify what a piece of developer communication is *doing*: fixing, adding, refactoring... | 1 | 100% |
| [`docweave.nlp.rationale`](api/docweave.nlp.rationale.md) | Mine the *why* out of developer communication. | 3 | 100% |
| [`docweave.nlp.text`](api/docweave.nlp.text.md) | Tokenising, identifier splitting, light stemming and sentence segmentation. | 5 | 100% |
| [`docweave.regions`](api/docweave.regions.md) | Managed regions: let generated and hand-written text share a file without clobbering. | 4 | 100% |
| [`docweave.render`](api/docweave.render.md) | Render an :class:`~docweave.engine.Analysis` as a Markdown documentation site. | 26 | 100% |
| [`docweave.search`](api/docweave.search.md) | Ask questions of the codebase: BM25 retrieval over symbols and the communication linked to them. | 2 | 100% |
<!-- docweave:end modules -->
