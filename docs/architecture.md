<!-- docweave:begin title -->
# Architecture
<!-- docweave:end title -->

<!-- docweave:begin health -->
**Documentation health: 100/100** · 100% of 144 public symbols documented · 0 drift issues ([report](health.md))
<!-- docweave:end health -->

<!-- docweave:begin graph -->
## Module dependencies

An arrow means *imports*.

```mermaid
graph LR
  m_docweave["docweave"]
  subgraph m_pkg_docweave["docweave"]
    m_docweave___main__["__main__"]
    m_docweave_analyzers["analyzers"]
    m_docweave_changelog["changelog"]
    m_docweave_cli["cli"]
    m_docweave_comms["comms"]
    m_docweave_config["config"]
    m_docweave_drift["drift"]
    m_docweave_engine["engine"]
    m_docweave_gitrepo["gitrepo"]
    m_docweave_graph["graph"]
    m_docweave_hooks["hooks"]
    m_docweave_linker["linker"]
    m_docweave_llm["llm"]
    m_docweave_model["model"]
    m_docweave_nlp["nlp"]
    m_docweave_regions["regions"]
    m_docweave_render["render"]
    m_docweave_search["search"]
  end
  subgraph m_pkg_docweave_analyzers["docweave.analyzers"]
    m_docweave_analyzers_javascript["javascript"]
    m_docweave_analyzers_python["python"]
  end
  subgraph m_pkg_docweave_nlp["docweave.nlp"]
    m_docweave_nlp_describe["describe"]
    m_docweave_nlp_docstring["docstring"]
    m_docweave_nlp_index["index"]
    m_docweave_nlp_intent["intent"]
    m_docweave_nlp_rationale["rationale"]
    m_docweave_nlp_text["text"]
  end
  m_docweave___main__ --> m_docweave_cli
  m_docweave_analyzers --> m_docweave_analyzers_javascript
  m_docweave_analyzers --> m_docweave_analyzers_python
  m_docweave_analyzers --> m_docweave_config
  m_docweave_analyzers --> m_docweave_model
  m_docweave_analyzers_javascript --> m_docweave_model
  m_docweave_analyzers_python --> m_docweave_model
  m_docweave_changelog --> m_docweave_config
  m_docweave_changelog --> m_docweave_model
  m_docweave_cli --> m_docweave
  m_docweave_cli --> m_docweave_analyzers
  m_docweave_cli --> m_docweave_changelog
  m_docweave_cli --> m_docweave_comms
  m_docweave_cli --> m_docweave_config
  m_docweave_cli --> m_docweave_drift
  m_docweave_cli --> m_docweave_engine
  m_docweave_cli --> m_docweave_gitrepo
  m_docweave_cli --> m_docweave_hooks
  m_docweave_cli --> m_docweave_linker
  m_docweave_cli --> m_docweave_llm
  m_docweave_cli --> m_docweave_nlp_intent
  m_docweave_cli --> m_docweave_nlp_rationale
  m_docweave_cli --> m_docweave_render
  m_docweave_cli --> m_docweave_search
  m_docweave_comms --> m_docweave_model
  m_docweave_drift --> m_docweave_analyzers
  m_docweave_drift --> m_docweave_config
  m_docweave_drift --> m_docweave_gitrepo
  m_docweave_drift --> m_docweave_linker
  m_docweave_drift --> m_docweave_model
  m_docweave_drift --> m_docweave_nlp_docstring
  m_docweave_drift --> m_docweave_nlp_intent
  m_docweave_engine --> m_docweave
  m_docweave_engine --> m_docweave_analyzers
  m_docweave_engine --> m_docweave_comms
  m_docweave_engine --> m_docweave_config
  m_docweave_engine --> m_docweave_drift
  m_docweave_engine --> m_docweave_gitrepo
  m_docweave_engine --> m_docweave_graph
  m_docweave_engine --> m_docweave_linker
  m_docweave_engine --> m_docweave_model
  m_docweave_engine --> m_docweave_nlp_intent
  m_docweave_gitrepo --> m_docweave_model
  m_docweave_graph --> m_docweave_model
  m_docweave_hooks --> m_docweave_config
  m_docweave_linker --> m_docweave_gitrepo
  m_docweave_linker --> m_docweave_model
  m_docweave_linker --> m_docweave_nlp_index
  m_docweave_linker --> m_docweave_nlp_text
  m_docweave_llm --> m_docweave_engine
  m_docweave_llm --> m_docweave_model
  m_docweave_llm --> m_docweave_nlp_rationale
  m_docweave_nlp_describe --> m_docweave_nlp_text
  m_docweave_nlp_docstring --> m_docweave_nlp_text
  m_docweave_nlp_intent --> m_docweave_nlp_text
  m_docweave_nlp_rationale --> m_docweave_nlp_text
  m_docweave_render --> m_docweave
  m_docweave_render --> m_docweave_changelog
  m_docweave_render --> m_docweave_drift
  m_docweave_render --> m_docweave_engine
  m_docweave_render --> m_docweave_graph
  m_docweave_render --> m_docweave_linker
  m_docweave_render --> m_docweave_model
  m_docweave_render --> m_docweave_nlp_describe
  m_docweave_render --> m_docweave_nlp_docstring
  m_docweave_render --> m_docweave_nlp_intent
  m_docweave_render --> m_docweave_nlp_rationale
  m_docweave_render --> m_docweave_nlp_text
  m_docweave_render --> m_docweave_regions
  m_docweave_search --> m_docweave_engine
  m_docweave_search --> m_docweave_nlp_docstring
  m_docweave_search --> m_docweave_nlp_index
  m_docweave_search --> m_docweave_nlp_rationale
  m_docweave_search --> m_docweave_nlp_text
```
<!-- docweave:end graph -->

<!-- docweave:begin cycles -->
## Import cycles

None found.
<!-- docweave:end cycles -->

<!-- docweave:begin external -->
## External dependencies

`anthropic`
<!-- docweave:end external -->

<!-- docweave:begin coupling -->
## Most depended-upon modules

Changes here ripple furthest, so these deserve the best documentation.

| Module | Imported by | Imports | Lines |
| --- | ---: | ---: | ---: |
| `docweave.model` | 12 | 0 | 168 |
| `docweave.nlp.text` | 7 | 0 | 88 |
| `docweave.config` | 6 | 0 | 85 |
| `docweave.engine` | 4 | 10 | 99 |
| `docweave.gitrepo` | 4 | 1 | 182 |
| `docweave.linker` | 4 | 4 | 188 |
| `docweave.nlp.intent` | 4 | 1 | 90 |
| `docweave.nlp.rationale` | 4 | 1 | 67 |
| `docweave` | 3 | 0 | 4 |
| `docweave.analyzers` | 3 | 4 | 61 |
| `docweave.drift` | 3 | 7 | 395 |
| `docweave.nlp.docstring` | 3 | 1 | 171 |
| `docweave.changelog` | 2 | 2 | 46 |
| `docweave.comms` | 2 | 1 | 122 |
| `docweave.graph` | 2 | 1 | 121 |
<!-- docweave:end coupling -->

<!-- docweave:begin hotspots -->
## Hotspots

Files that are both complex and frequently changed - where stale documentation costs the most.

| File | Commits | Complexity | Undocumented public symbols |
| --- | ---: | ---: | ---: |
| [`docweave/render.py`](api/docweave.render.md) | 2 | 233 | 0 of 26 |
| [`docweave/analyzers/javascript.py`](api/docweave.analyzers.javascript.md) | 1 | 185 | 0 of 3 |
| [`docweave/drift.py`](api/docweave.drift.md) | 1 | 178 | 0 of 16 |
| [`docweave/analyzers/python.py`](api/docweave.analyzers.python.md) | 1 | 138 | 0 of 2 |
| [`docweave/cli.py`](api/docweave.cli.md) | 1 | 110 | 0 of 11 |
| [`docweave/linker.py`](api/docweave.linker.md) | 1 | 79 | 0 of 7 |
| [`docweave/nlp/docstring.py`](api/docweave.nlp.docstring.md) | 1 | 72 | 0 of 2 |
| [`docweave/comms.py`](api/docweave.comms.md) | 1 | 64 | 0 of 2 |
| [`docweave/gitrepo.py`](api/docweave.gitrepo.md) | 1 | 49 | 0 of 12 |
| [`docweave/graph.py`](api/docweave.graph.md) | 1 | 49 | 0 of 4 |
<!-- docweave:end hotspots -->
