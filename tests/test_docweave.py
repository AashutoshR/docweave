"""Tests for DocWeave. Run with:  python -m unittest discover -s tests -v"""

from __future__ import annotations

import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import types
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "examples"))

from docweave import drift, llm, regions, render  # noqa: E402
from docweave.comms import load_comms, pull_github  # noqa: E402
from docweave.analyzers import javascript, python  # noqa: E402
from docweave.changelog import build_changelog  # noqa: E402
from docweave.cli import build_parser, main  # noqa: E402
from docweave.config import load_config  # noqa: E402
from docweave.engine import analyze  # noqa: E402
from docweave.graph import cycles, mermaid  # noqa: E402
from docweave.nlp.describe import describe  # noqa: E402
from docweave.nlp.docstring import parse_docstring  # noqa: E402
from docweave.nlp.index import TextIndex  # noqa: E402
from docweave.nlp.intent import classify  # noqa: E402
from docweave.nlp.rationale import decision_score, rationale  # noqa: E402
from docweave.nlp.text import sentences, split_identifier, stem, tokenize  # noqa: E402
from docweave.search import search  # noqa: E402
from make_demo_repo import build  # noqa: E402

HAS_GIT = shutil.which("git") is not None


def run_cli(*argv: str) -> tuple[int, str]:
    out = io.StringIO()
    with redirect_stdout(out), redirect_stderr(out):
        code = main(list(argv))
    return code, out.getvalue()


class TextTests(unittest.TestCase):
    def test_split_identifier(self):
        self.assertEqual(split_identifier("get_user_by_id"), ["get", "user", "by", "id"])
        self.assertEqual(split_identifier("parseHTTPResponse2"), ["parse", "http", "response", "2"])

    def test_stem_is_consistent_across_forms(self):
        for forms in (["fix", "fixes", "fixed", "fixing"], ["remove", "removed", "removing"], ["cache", "caching", "cached"]):
            self.assertEqual(len({stem(f) for f in forms}), 1, forms)
        self.assertEqual(stem("added"), stem("add"))

    def test_tokenize_drops_stopwords_and_splits_code(self):
        self.assertEqual(tokenize("The retryCount is updated"), ["retry", "count", "updat"])

    def test_sentences_treat_bullets_and_wrapped_lines(self):
        text = "First line wraps\nonto a second. Then another.\n\n- a bullet\n- second bullet"
        self.assertEqual(sentences(text), ["First line wraps onto a second.", "Then another.", "a bullet", "second bullet"])


class IntentTests(unittest.TestCase):
    def test_conventional_commit(self):
        intent, scope, breaking, confidence, subject = classify("feat(api)!: drop v1 endpoints (#31)")
        self.assertEqual((intent, scope, breaking, confidence, subject), ("feature", "api", True, 1.0, "Drop v1 endpoints"))

    def test_plain_english_is_classified_by_lexicon(self):
        self.assertEqual(classify("Fixed crash when the cart is empty")[0], "fix")
        self.assertEqual(classify("Rename helper and tidy imports")[0], "refactor")
        self.assertEqual(classify("Bump requests to 2.32")[0], "chore")
        self.assertEqual(classify("Speed up parsing with a cache")[0], "perf")
        self.assertEqual(classify("wip")[0], "other")

    def test_breaking_change_footer(self):
        self.assertTrue(classify("refactor: remove old API", "BREAKING CHANGE: callers must migrate")[2])


class DocstringTests(unittest.TestCase):
    def test_google_style(self):
        info = parse_docstring("Do a thing.\n\nMore.\n\nArgs:\n    a (int): first\n        continued\n    *rest: others\n\nReturns:\n    bool: ok\n\nRaises:\n    ValueError: bad\n")
        self.assertEqual(info.summary, "Do a thing.")
        self.assertEqual(info.params, {"a": "first continued", "rest": "others"})
        self.assertEqual(info.param_types, {"a": "int"})
        self.assertEqual(info.returns, "bool: ok")
        self.assertEqual(info.raises, {"ValueError": "bad"})

    def test_numpy_style(self):
        info = parse_docstring("Sum.\n\nParameters\n----------\nx, y : int\n    operands\n\nReturns\n-------\nint\n")
        self.assertEqual(set(info.params), {"x", "y"})
        self.assertEqual(info.returns, "int")

    def test_sphinx_style(self):
        info = parse_docstring("Do.\n\n:param int a: first\n:param b: second\n    more\n:returns: x\n:raises KeyError: nope")
        self.assertEqual(info.params, {"a": "first", "b": "second more"})
        self.assertEqual(info.raises, {"KeyError": "nope"})
        self.assertEqual(info.description, "Do.")

    def test_jsdoc_with_nested_type_braces(self):
        info = parse_docstring("Sum.\n@param {Array<{price: number}>} items - Line items.\n@param {number} [rate=0] tax\n@returns {number} Total")
        self.assertEqual(info.params, {"items": "Line items.", "rate": "tax"})
        self.assertEqual(info.param_types["items"], "Array<{price: number}>")
        self.assertEqual(info.returns, "Total")


PY_SOURCE = '''"""Module doc."""
from . import sibling
from .pkg.util import helper

__all__ = ["Shape", "area"]
LIMIT = 10


class Shape:
    """A shape."""

    def __init__(self, sides: int = 4, *, name="x"):
        self.sides = sides

    def scale(self, factor):
        if factor <= 0 or factor > LIMIT:
            raise ValueError("bad")
        return [s * factor for s in range(self.sides) if s]

    def _private(self):
        pass


def area(w: float, h: float = 1.0, *args, **kw) -> float:
    """Area.

    Args:
        w: width
    """
    return helper(w) * h


def hidden():
    return 1
'''


class PythonAnalyzerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = python.analyze("src/geo/shapes.py", PY_SOURCE)
        cls.sym = {s.qualname: s for s in cls.module.symbols}

    def test_module_naming_and_imports(self):
        self.assertEqual(self.module.name, "geo.shapes")
        self.assertEqual(self.module.docstring, "Module doc.")
        self.assertIn("geo.sibling", self.module.imports)
        self.assertIn("geo.pkg.util", self.module.imports)

    def test_symbols_and_visibility_follow_dunder_all(self):
        self.assertEqual(set(self.sym), {"LIMIT", "Shape", "Shape.__init__", "Shape.scale", "Shape._private", "area", "hidden"})
        self.assertTrue(self.sym["Shape"].is_public and self.sym["area"].is_public and self.sym["Shape.scale"].is_public)
        self.assertFalse(self.sym["hidden"].is_public)  # not in __all__
        self.assertFalse(self.sym["Shape._private"].is_public)

    def test_signature_params_and_facts(self):
        area = self.sym["area"]
        self.assertEqual(area.signature, "def area(w: float, h: float=1.0, *args, **kw) -> float")
        self.assertEqual([(p.name, p.kind) for p in area.params], [("w", "positional"), ("h", "positional"), ("args", "vararg"), ("kw", "kwarg")])
        self.assertEqual(area.returns, "float")
        self.assertIn("helper", area.calls)
        scale = self.sym["Shape.scale"]
        self.assertEqual([p.name for p in scale.params], ["factor"])  # self is dropped
        self.assertEqual(scale.raises, ["ValueError"])
        self.assertTrue(scale.returns_value)
        self.assertEqual(scale.complexity, 5)  # 1 + if + or + comprehension + its filter
        self.assertEqual([p.name for p in self.sym["Shape"].params], ["sides", "name"])  # from __init__

    def test_hashes_ignore_comments_and_docstrings_but_not_code(self):
        base = python.analyze("m.py", "def f(a):\n    return a + 1\n").symbols[0]
        cosmetic = python.analyze("m.py", 'def f(a):\n    """Doc."""\n    # note\n    return a  +  1\n').symbols[0]
        changed = python.analyze("m.py", "def f(a, b):\n    return a + b\n").symbols[0]
        self.assertEqual((base.interface_hash, base.body_hash), (cosmetic.interface_hash, cosmetic.body_hash))
        self.assertNotEqual(base.interface_hash, changed.interface_hash)
        self.assertNotEqual(base.body_hash, changed.body_hash)

    def test_syntax_error_is_reported_not_raised(self):
        self.assertIn("syntax error", python.analyze("bad.py", "def (:\n").error)


JS_SOURCE = """/**
 * Cart utilities.
 */

import { tax } from './tax';
const fs = require("fs");

/**
 * Add two numbers.
 * @param {number} a - first
 * @returns {number} the sum
 */
export function add(a, b = 2) {
  if (a > 1 && b) { return a + b; }
  return a; // not a brace: {
}

export const double = (x) => x * 2;

export const load = async (path, opts = {}) => {
  const s = "}{";
  return fs.readFile(path);
};

export class Cart extends Base {
  /** Total price. */
  total(rate) {
    for (const i of this.items) { if (i) { throw new RangeError("x"); } }
    return tax(rate);
  }
  #secret() { return 1; }
}
function _hidden() {}
"""


class JavaScriptAnalyzerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = javascript.analyze("src/cart/index.js", JS_SOURCE)
        cls.sym = {s.qualname: s for s in cls.module.symbols}

    def test_module(self):
        self.assertEqual(self.module.name, "cart")
        self.assertEqual(self.module.docstring, "Cart utilities.")
        self.assertEqual(self.module.imports, ["cart.tax", "npm:fs"])

    def test_declarations(self):
        self.assertEqual(set(self.sym), {"add", "double", "load", "Cart", "Cart.total", "Cart.#secret", "_hidden"})
        self.assertEqual((self.sym["add"].lineno, self.sym["add"].end_lineno), (13, 16))
        self.assertEqual((self.sym["load"].lineno, self.sym["load"].end_lineno), (20, 23))  # braces in strings ignored
        self.assertEqual([p.name for p in self.sym["add"].params], ["a", "b"])
        self.assertEqual(self.sym["add"].params[1].default, "2")
        self.assertTrue(self.sym["load"].is_async)
        self.assertEqual(self.sym["Cart"].bases, ["Base"])
        self.assertEqual(self.sym["Cart.total"].raises, ["RangeError"])
        self.assertEqual(self.sym["Cart.total"].docstring, "Total price.")

    def test_visibility(self):
        self.assertTrue(self.sym["add"].is_public and self.sym["Cart.total"].is_public)
        self.assertFalse(self.sym["_hidden"].is_public or self.sym["Cart.#secret"].is_public)

    def test_jsdoc_claims_are_checked(self):
        kinds = {i.kind for i in drift.check_claims(self.sym["add"])}
        self.assertEqual(kinds, {"param-undocumented"})  # b is not in the JSDoc


TS_SOURCE = r"""import type { Thing } from './types';

/** A listener. */
export interface Listener<T> {
  (event: T): void;
}

export type Shape =
  | { kind: 'circle'; r: number }
  | { kind: 'square'; side: number };

export enum Color { Red, Green }

export function on(event: string, handler: (e: Event) => void, opts: { once?: boolean } = {}): () => void {
  return () => handler(new Event(event));
}

export function overload(a: string): string;
export function overload(a: any): any { return a; }

export async function load<T extends { id: number }>(url: string): Promise<{ data: T[] }> {
  return (await fetch(url)).json();
}

export function point(): { x: number; y: number } {
  return { x: 1, y: 2 };
}

export const pick = <T, K extends keyof T>(obj: T, ...keys: K[]): Pick<T, K> => {
  return keys.reduce((acc, k) => ({ ...acc, [k]: obj[k] }), {} as Pick<T, K>);
};

export const sum = (xs: number[]) =>
  xs.reduce((a, b) => a + b, 0);

export const id = x => x;

const internal = function helper(a, b) { return a + b; };

@Injectable()
export abstract class Store<S> extends Base implements OnInit {
  private state: S;

  constructor(private readonly http: HttpClient, initial: S) { super(); }

  /** Current value. */
  get value(): S { return this.state; }

  abstract reduce(action: Action): S;

  protected async dispatch<A extends Action>(action: A, cb: (s: S) => void = () => {}): Promise<void> {
    if (!action) { throw new TypeError('no action'); }
  }

  onClick = (e: MouseEvent) => {
    this.dispatch(e as any);
  };

  private secret() { return 1; }
}
"""

CJS_SOURCE = """const path = require('node:path')
function helper (a) { return a }
function exposed (a, b) { return helper(a) + b }
exports.direct = async (x) => { return x }
module.exports.other = function (y) { return y }
module.exports = { exposed }
"""


class TypeScriptAnalyzerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = javascript.analyze("src/store.ts", TS_SOURCE)
        cls.sym = {s.qualname: s for s in cls.module.symbols}

    def test_every_declaration_is_found_once(self):
        self.assertEqual(
            [(s.kind, s.qualname) for s in self.module.symbols],
            [("interface", "Listener"), ("type", "Shape"), ("enum", "Color"), ("function", "on"), ("function", "overload"),
             ("function", "load"), ("function", "point"), ("function", "pick"), ("function", "sum"), ("function", "id"),
             ("function", "internal"), ("class", "Store"), ("method", "Store.constructor"), ("method", "Store.value"),
             ("method", "Store.dispatch"), ("method", "Store.onClick"), ("method", "Store.secret")],
        )  # overload signatures and the abstract method have no body, so they are not separate symbols

    def test_callback_and_object_types_do_not_confuse_the_scanner(self):
        on = self.sym["on"]
        self.assertEqual([p.name for p in on.params], ["event", "handler", "opts"])
        self.assertEqual(on.params[1].annotation, "(e: Event) => void")
        self.assertEqual((on.params[2].annotation, on.params[2].default), ("{ once?: boolean }", "{}"))
        self.assertEqual(self.sym["Store.dispatch"].params[1].default, "() => {}")
        self.assertEqual(on.returns, "() => void")
        self.assertEqual(self.sym["point"].returns, "{ x: number; y: number }")
        self.assertEqual((self.sym["point"].lineno, self.sym["point"].end_lineno), (25, 27))
        self.assertEqual(self.sym["load"].returns, "Promise<{ data: T[] }>")
        self.assertTrue(self.sym["load"].is_async)
        self.assertEqual(self.sym["Shape"].end_lineno - self.sym["Shape"].lineno, 2)

    def test_arrows_generics_and_rest_parameters(self):
        self.assertEqual([(p.name, p.kind) for p in self.sym["pick"].params], [("obj", "positional"), ("keys", "vararg")])
        self.assertEqual(self.sym["pick"].returns, "Pick<T, K>")
        self.assertEqual((self.sym["sum"].lineno, self.sym["sum"].end_lineno), (33, 34))
        self.assertEqual([p.name for p in self.sym["id"].params], ["x"])

    def test_classes(self):
        store = self.sym["Store"]
        self.assertEqual(store.bases, ["Base"])
        self.assertEqual([p.name for p in store.params], ["http", "initial"])  # parameter properties
        self.assertEqual(store.docstring, None)
        self.assertEqual(self.sym["Store.value"].docstring, "Current value.")
        dispatch = self.sym["Store.dispatch"]
        self.assertEqual([p.name for p in dispatch.params], ["action", "cb"])
        self.assertEqual(dispatch.raises, ["TypeError"])
        self.assertTrue(dispatch.is_async)
        self.assertEqual([p.name for p in self.sym["Store.onClick"].params], ["e"])

    def test_visibility(self):
        public = {s.qualname for s in self.module.symbols if s.is_public}
        self.assertNotIn("internal", public)  # not exported
        self.assertNotIn("Store.secret", public)  # private
        self.assertTrue({"Listener", "Shape", "Color", "on", "Store", "Store.dispatch"} <= public)

    def test_commonjs_exports_decide_visibility(self):
        module = javascript.analyze("lib/util.cjs", CJS_SOURCE)
        self.assertEqual({s.name: s.is_public for s in module.symbols},
                         {"helper": False, "exposed": True, "direct": True, "other": True})
        self.assertEqual(module.imports, ["npm:node:path"])


class ClaimTests(unittest.TestCase):
    def check(self, source: str) -> list:
        return drift.check_claims(python.analyze("m.py", source).symbols[0])

    def test_renamed_parameter_is_detected_with_a_guess(self):
        issues = self.check('def f(timeout_s):\n    """Do.\n\n    Args:\n        timeout: seconds\n    """\n    return timeout_s\n')
        ghost = next(i for i in issues if i.kind == "param-not-in-signature")
        self.assertEqual(ghost.severity, "high")
        self.assertIn("renamed to `timeout_s`", ghost.detail[0])

    def test_kwargs_and_undocumented_functions_are_not_flagged(self):
        self.assertEqual(self.check('def f(**options):\n    """Do.\n\n    Args:\n        verbose: chatty\n    """\n'), [])
        self.assertEqual(self.check('def f(a, b):\n    """Just a summary."""\n    return a\n'), [])

    def test_returns_and_raises_mismatch(self):
        issues = self.check('def f(a):\n    """Do.\n\n    Returns:\n        int: value\n\n    Raises:\n        KeyError: x\n    """\n    raise ValueError(a)\n')
        self.assertEqual({i.kind for i in issues}, {"returns-mismatch", "raises-mismatch"})

    def test_rename_guess_considers_star_args(self):
        issues = self.check('def f(*renderables, style=None):\n    """Do.\n\n    Args:\n        renderable: things\n        style: look\n    """\n')
        self.assertIn("renamed to `renderables`", issues[0].detail[0])

    def test_exception_aliases_and_catch_alls_are_not_flagged(self):
        aliased = 'def f(a):\n    """Do.\n\n    Raises:\n        JSONDecodeError: bad\n        Exception: anything else\n    """\n    raise RequestsJSONDecodeError(a)\n'
        self.assertEqual(self.check(aliased), [])

    def test_stubs_are_exempt(self):
        self.assertEqual(self.check('def f(a):\n    """Do.\n\n    Returns:\n        int: value\n    """\n    raise NotImplementedError\n'), [])


class RegionTests(unittest.TestCase):
    def test_new_file(self):
        self.assertEqual(regions.merge(None, [("a", "A"), ("b", "B")]),
                         "<!-- docweave:begin a -->\nA\n<!-- docweave:end a -->\n\n<!-- docweave:begin b -->\nB\n<!-- docweave:end b -->\n")

    def test_human_text_survives_and_blocks_update_in_place(self):
        first = regions.merge(None, [("a", "A1"), ("b", "B1")])
        edited = first.replace("<!-- docweave:begin b -->", "My own notes about b.\n\n<!-- docweave:begin b -->")
        merged = regions.merge(edited, [("a", "A2"), ("b", "B2")])
        self.assertIn("My own notes about b.", merged)
        self.assertIn("A2", merged)
        self.assertNotIn("A1", merged)
        self.assertLess(merged.index("My own notes"), merged.index("B2"))

    def test_removed_and_inserted_blocks(self):
        first = regions.merge(None, [("a", "A"), ("b", "B"), ("d", "D")])
        merged = regions.merge(first, [("a", "A"), ("c", "C"), ("d", "D")])
        self.assertEqual(regions.region_ids(merged), ["a", "c", "d"])  # b dropped, c slotted after a
        self.assertEqual(regions.merge(merged, [("a", "A"), ("c", "C"), ("d", "D")]), merged)  # idempotent

    def test_inject_only_touches_existing_regions(self):
        readme = "# Mine\n\n<!-- docweave:begin modules -->\n<!-- docweave:end modules -->\n\nBye\n"
        merged = regions.merge(readme, [("health", "H"), ("modules", "TABLE")], inject_only=True)
        self.assertEqual(merged, "# Mine\n\n<!-- docweave:begin modules -->\nTABLE\n<!-- docweave:end modules -->\n\nBye\n")


class SmallUnitTests(unittest.TestCase):
    def test_cycles_and_mermaid(self):
        edges = {"a": {"b"}, "b": {"c"}, "c": {"a"}, "d": {"a"}, "e": set()}
        self.assertEqual(cycles(edges), [["a", "b", "c"]])
        self.assertIn("m_d --> m_a", mermaid(edges))

    def test_rationale_prefers_explanations(self):
        body = "Updated the handler.\nWe chose a queue instead of threads because ordering matters.\nSigned-off-by: x"
        self.assertEqual(rationale("refactor: handler", body, limit=1), ["We chose a queue instead of threads because ordering matters."])
        self.assertGreaterEqual(decision_score("refactor: handler", body), 3.5)
        self.assertLess(decision_score("bump version", ""), 3.5)

    def test_describe(self):
        self.assertEqual(describe("get_user_by_id", "function"), "Return user by id.")
        self.assertEqual(describe("PaymentProcessor", "class"), "Payment processor.")

    def test_index_ranking(self):
        index = TextIndex()
        index.add("retry", tokenize("retry the request with exponential backoff"))
        index.add("parse", tokenize("parse the config file"))
        index.add("other", tokenize("render markdown output"))
        index.finalize()
        self.assertEqual(index.bm25(tokenize("backoff retries"))[0][0], "retry")
        self.assertEqual(index.cosine(tokenize("parsing config"))[0][0], "parse")
        self.assertEqual(index.cosine(tokenize("parsing config"), restrict={"other"}), [])


@unittest.skipUnless(HAS_GIT, "git is required for the end-to-end tests")
class DemoRepoTests(unittest.TestCase):
    """End-to-end: the scripted history in examples/make_demo_repo.py plants known drift."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        cls.repo = build(Path(cls.tmp.name) / "payflow")
        cls.a = analyze(load_config(cls.repo))
        cls.issues = {(i.kind, i.symbol.split(":")[1] if i.symbol else i.file): i for i in cls.a.issues}

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def copy(self) -> Path:
        target = Path(tempfile.mkdtemp(dir=self.tmp.name)) / "payflow"
        shutil.copytree(self.repo, target)
        return target

    def test_signature_change_without_docstring_update(self):
        stale = self.issues[("stale-docstring", "charge")]
        self.assertEqual(stale.severity, "high")
        self.assertTrue(any("retry charges on 429" in d for d in stale.detail))
        self.assertIn("`retries`", self.issues[("param-undocumented", "charge")].message)

    def test_removed_parameter_still_documented(self):
        self.assertEqual(self.issues[("param-not-in-signature", "refund")].severity, "high")

    def test_behaviour_change_under_an_old_docstring(self):
        self.assertIn(("stale-docstring", "Ledger.balance"), self.issues)

    def test_formatting_commit_does_not_make_docs_stale(self):
        self.assertNotIn(("stale-docstring", "Ledger.record"), self.issues)
        self.assertEqual(self.a.messages[next(c.id for c in self.a.commits if "black" in c.title)].intent, "style")

    def test_javascript_drift(self):
        self.assertIn(("stale-docstring", "total"), self.issues)
        self.assertIn("`taxRate`", self.issues[("param-undocumented", "total")].message)

    def test_readme_references_to_renamed_and_removed_code(self):
        dangling = {i.message.split("`")[1]: i for i in self.a.issues if i.kind == "dangling-reference"}
        self.assertEqual(set(dangling), {"convert_currency", "legacy_charge"})
        self.assertIn("did you mean `convert`?", dangling["convert_currency"].detail)
        self.assertIn("Lena Fischer", dangling["convert_currency"].detail[0])
        self.assertEqual(dangling["convert_currency"].file, "README.md")

    def test_stale_prose_and_deleted_path(self):
        prose = next(i for i in self.a.issues if i.kind == "stale-prose")
        self.assertEqual((prose.file, prose.symbol), ("README.md", "payflow.gateway:charge"))
        missing = next(i for i in self.a.issues if i.kind == "missing-path")
        self.assertIn("notes/ledger.md", missing.message)
        self.assertIn("deleted in", missing.detail[0])

    def test_communication_is_linked_to_code(self):
        def linked(symbol_id):
            return {l.message_id.split(":")[0] + ":" + self.a.messages[l.message_id].title for l in self.a.links[symbol_id]}

        charge = linked("payflow.gateway:charge")
        self.assertIn("pr:Retry charges on 429", charge)  # inherited through "(#4)" in the commit subject
        self.assertIn("commit:fix(gateway): retry charges on 429 (#4)", charge)
        convert = [self.a.messages[l.message_id] for l in self.a.links["payflow.fx:convert"]]
        self.assertTrue(any(m.source == "chat" and "Decimal" in m.body for m in convert))
        self.assertFalse(any("Lunch" in m.body for m in self.a.messages.values() if self.a.symbols_of(m.id)))

    def test_changelog_releases_and_intents(self):
        releases = build_changelog(self.a.cfg, self.a.commits)
        self.assertEqual([r.name for r in releases], ["Unreleased", "v0.1.0"])
        self.assertEqual([c.subject for c in releases[0].breaking], ["Remove legacy_charge"])
        self.assertEqual([c.subject for c in releases[0].sections["security"]], ["Harden charge against negative amounts"])
        self.assertIn("Rename convert_currency to convert and switch to Decimal", [c.subject for c in releases[1].sections["refactor"]])

    def test_search_finds_code_through_the_discussion_about_it(self):
        titles = [h.title for h in search(self.a, "why do we use Decimal for money", k=4)]
        self.assertIn("convert", titles)

    def test_generate_is_idempotent_and_preserves_human_edits(self):
        repo = self.copy()
        code, out = run_cli("generate", "--root", str(repo))
        self.assertEqual(code, 0, out)
        gateway = repo / "docs" / "api" / "payflow.gateway.md"
        text = gateway.read_text(encoding="utf-8")
        self.assertIn("Docs may be out of date", text)
        self.assertIn("We chose exponential backoff rather than a fixed delay", text)
        self.assertIn("| [`payflow.fx`](docs/api/payflow.fx.md)", (repo / "README.md").read_text(encoding="utf-8"))
        self.assertIn("### ⚠️ Breaking changes", (repo / "docs" / "CHANGELOG.md").read_text(encoding="utf-8"))

        gateway.write_text(text.replace("<!-- docweave:begin sym:charge -->", "Ask the payments team before changing this.\n\n<!-- docweave:begin sym:charge -->"), encoding="utf-8", newline="\n")
        before = {p: p.read_bytes() for p in (repo / "docs").rglob("*.md")}
        code, out = run_cli("generate", "--root", str(repo))
        self.assertIn("docs already up to date", out)
        self.assertEqual(before, {p: p.read_bytes() for p in (repo / "docs").rglob("*.md")})
        self.assertIn("Ask the payments team", gateway.read_text(encoding="utf-8"))
        self.assertEqual(run_cli("check", "--root", str(repo), "--fail-on", "low", "--require-fresh", "--quiet")[1].count("STALE"), 0)

    def test_fixing_the_docs_clears_the_issue_and_updates_the_page(self):
        repo = self.copy()
        run_cli("generate", "--root", str(repo))
        source = repo / "payflow" / "gateway.py"
        source.write_text(source.read_text(encoding="utf-8").replace(
            "        currency: ISO 4217 currency code.\n", "        currency: ISO 4217 currency code.\n        retries: How many times to retry after a 429.\n"),
            encoding="utf-8", newline="\n")
        a = analyze(load_config(repo))
        self.assertFalse([i for i in a.issues if i.symbol == "payflow.gateway:charge" and i.file.endswith(".py")])
        code, out = run_cli("check", "--root", str(repo), "--require-fresh")
        self.assertIn("STALE  docs/api/payflow.gateway.md", out)
        run_cli("generate", "--root", str(repo))
        self.assertIn("How many times to retry after a 429.", (repo / "docs" / "api" / "payflow.gateway.md").read_text(encoding="utf-8"))

    def test_check_exit_codes(self):
        self.assertEqual(run_cli("check", "--root", str(self.repo), "--quiet")[0], 1)
        code, out = run_cli("check", "--root", str(self.repo), "--format", "github")
        self.assertIn("::error file=README.md,line=", out)

    def test_staged_check_only_blames_files_in_the_commit(self):
        repo = self.copy()

        def touch_and_stage(rel: str) -> None:
            path = repo / rel
            path.write_text(path.read_text(encoding="utf-8") + "\n# touched\n", encoding="utf-8", newline="\n")
            subprocess.run(["git", "add", rel], cwd=repo, check=True, capture_output=True)

        touch_and_stage("payflow/fx.py")  # fx.py itself is clean; the drift lives elsewhere
        self.assertEqual(run_cli("check", "--root", str(repo), "--staged", "--quiet"), (0, ""))
        touch_and_stage("payflow/gateway.py")
        code, out = run_cli("check", "--root", str(repo), "--staged", "--quiet")
        self.assertEqual(code, 1)
        self.assertIn("payflow/gateway.py", out)
        self.assertNotIn("web/cart.js", out)

    def test_housekeeping_commits_are_not_design_decisions(self):
        repo = self.copy()
        readme = repo / "README.md"
        readme.write_text(readme.read_text(encoding="utf-8") + "\nMore notes.\n", encoding="utf-8", newline="\n")
        subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-q", "-m", "docs: refresh the notes\n\nWe decided to rewrite them because the decision log moved."],
                       cwd=repo, check=True, capture_output=True)
        pages = render.Renderer(analyze(load_config(repo))).decisions_page()
        text = "\n".join(body for _id, body in pages)
        self.assertNotIn("Refresh the notes", text)
        self.assertIn("Rename convert_currency to convert", text)  # real decisions are still there

    def test_removed_module_page_is_cleaned_up(self):
        repo = self.copy()
        run_cli("generate", "--root", str(repo))
        (repo / "web" / "money.js").unlink()
        code, out = run_cli("generate", "--root", str(repo))
        self.assertIn("removed docs/api/web.money.md", out)
        self.assertFalse((repo / "docs" / "api" / "web.money.md").exists())

    def test_why_command(self):
        code, out = run_cli("why", "Ledger.balance", "--root", str(self.repo))
        self.assertEqual(code, 0)
        self.assertIn("Large merchant accounts timed out because balance() rescanned every entry.", out)
        self.assertEqual(run_cli("why", "no_such_thing", "--root", str(self.repo))[0], 1)

    def test_without_git_signature_drift_is_anchored_in_state(self):
        repo = self.copy()
        shutil.rmtree(repo / ".git", onerror=lambda func, path, _exc: (Path(path).chmod(0o700), func(path)))
        run_cli("generate", "--root", str(repo), "--no-git")
        fx = repo / "payflow" / "fx.py"
        fx.write_text(fx.read_text(encoding="utf-8").replace("def convert(amount, source, target):", "def convert(amount, source, target, places=2):"), encoding="utf-8", newline="\n")
        a = analyze(load_config(repo), use_git=False)
        self.assertIn("signature-drift", {i.kind for i in a.issues if i.symbol == "payflow.fx:convert"})
        run_cli("generate", "--root", str(repo), "--no-git")  # regenerating must not hide the problem
        a = analyze(load_config(repo), use_git=False)
        self.assertIn("signature-drift", {i.kind for i in a.issues if i.symbol == "payflow.fx:convert"})
        fx.write_text(fx.read_text(encoding="utf-8").replace("amount: Amount as a Decimal.", "amount: Amount as a Decimal.\n        places: Decimal places to round to."), encoding="utf-8", newline="\n")
        a = analyze(load_config(repo), use_git=False)
        self.assertNotIn("signature-drift", {i.kind for i in a.issues})


class FakeAnthropic:
    """Stands in for the ``anthropic`` package: records requests and answers every symbol asked about."""

    def __init__(self, stop_reason: str = "end_turn") -> None:
        self.requests: list[tuple[str, dict]] = []
        self.stop_reason = stop_reason
        self.module = types.ModuleType("anthropic")
        for name in ("AuthenticationError", "NotFoundError", "RateLimitError", "APIStatusError", "APIConnectionError"):
            setattr(self.module, name, type(name, (Exception,), {}))
        self.module.Anthropic = lambda: types.SimpleNamespace(
            messages=types.SimpleNamespace(create=lambda **kw: self.respond("stable", kw)),
            beta=types.SimpleNamespace(messages=types.SimpleNamespace(create=lambda **kw: self.respond("beta", kw))),
        )

    def respond(self, endpoint: str, request: dict):
        self.requests.append((endpoint, request))
        ids = re.findall(r'<symbol id="([^"]+)"', request["messages"][0]["content"])
        text = json.dumps({"summaries": [{"id": i, "summary": f"Summary of {i}."} for i in ids]})
        return types.SimpleNamespace(stop_reason=self.stop_reason, content=[types.SimpleNamespace(type="text", text=text)])


class LLMTests(unittest.TestCase):
    """The optional AI layer, exercised against a fake SDK (no network, no credentials)."""

    SOURCE = 'def alpha(x):\n    return x + 1\n\n\ndef beta(y):\n    return y * 2\n\n\ndef documented(z):\n    """Already explained."""\n    return z\n'

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "app.py").write_text(self.SOURCE, encoding="utf-8")
        self.fake = FakeAnthropic()
        self.patch = mock.patch.dict(sys.modules, {"anthropic": self.fake.module})
        self.patch.start()

    def tearDown(self):
        self.patch.stop()
        self.tmp.cleanup()

    def summarize(self) -> dict[str, str]:
        return llm.summarize_undocumented(analyze(load_config(self.root), use_git=False))

    def test_only_undocumented_symbols_are_sent_and_results_are_cached(self):
        self.assertEqual(self.summarize(), {"app:alpha": "Summary of app:alpha.", "app:beta": "Summary of app:beta."})
        self.assertEqual(len(self.fake.requests), 1)
        endpoint, request = self.fake.requests[0]
        prompt = request["messages"][0]["content"]
        self.assertIn("return x + 1", prompt)
        self.assertNotIn("Already explained", prompt)
        self.assertEqual((endpoint, request["model"], request["fallbacks"]), ("beta", "claude-opus-5-5", "default"))
        self.assertEqual(request["output_config"]["format"]["type"], "json_schema")
        self.summarize()
        self.assertEqual(len(self.fake.requests), 1)  # second run is served entirely from the cache

    def test_only_changed_code_is_sent_again(self):
        self.summarize()
        (self.root / "app.py").write_text(self.SOURCE.replace("return y * 2", "return y * 3"), encoding="utf-8")
        self.summarize()
        resent = self.fake.requests[1][1]["messages"][0]["content"]
        self.assertIn('id="app:beta"', resent)
        self.assertNotIn('id="app:alpha"', resent)

    def test_refusal_is_handled_without_crashing(self):
        self.fake.stop_reason = "refusal"
        self.assertEqual(self.summarize(), {})

    def test_models_without_server_side_fallback_use_the_plain_endpoint(self):
        (self.root / "docweave.toml").write_text('llm_model = "claude-haiku-5-5"\n', encoding="utf-8")
        self.summarize()
        endpoint, request = self.fake.requests[0]
        self.assertEqual(endpoint, "stable")
        self.assertNotIn("fallbacks", request)

    def test_summaries_are_rendered_and_labelled(self):
        code, out = run_cli("generate", "--root", str(self.root), "--no-git", "--llm")
        self.assertEqual(code, 0, out)
        page = (self.root / "docs" / "api" / "app.md").read_text(encoding="utf-8")
        self.assertIn("Summary of app:alpha.", page)
        self.assertIn("AI-generated", page)
        self.assertIn("Already explained.", page)

    def test_missing_sdk_gives_a_clear_message(self):
        with mock.patch.dict(sys.modules, {"anthropic": None}):
            with self.assertRaises(SystemExit) as caught:
                run_cli("generate", "--root", str(self.root), "--no-git", "--llm")
        self.assertEqual(caught.exception.code, 2)


class CommsTests(unittest.TestCase):
    def test_each_supported_format_is_normalised(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "prs.json").write_text(json.dumps([{"number": 9, "title": "Add retries", "body": "Because flaky.", "author": {"login": "sam"},
                                                        "mergedAt": "2026-02-01T10:00:00Z", "url": "https://github.com/o/r/pull/9"}]), encoding="utf-8")
            (root / "issues.json").write_text(json.dumps([{"number": 3, "title": "Crash", "body": "", "url": "https://github.com/o/r/issues/3"}]), encoding="utf-8")
            (root / "general.json").write_text(json.dumps([{"user_name": "kim", "text": "ship it", "ts": "1767225600.5"}, {"ts": "1"}]), encoding="utf-8")
            (root / "log.jsonl").write_text('{"body": "note one", "author": "al", "date": "2026-01-02"}\nnot json\n', encoding="utf-8")
            (root / "adr-1.md").write_text("# Use Postgres\n\nDate: 2026-01-03\n\nWe decided to use Postgres.\n", encoding="utf-8")
            (root / "broken.json").write_text("{nope", encoding="utf-8")
            messages = {m.id: m for m in load_comms(root)}
        self.assertEqual({m.source for m in messages.values()}, {"pr", "issue", "chat", "note"})
        self.assertEqual((messages["pr:9"].author, messages["pr:9"].day), ("sam", "2026-02-01"))
        self.assertIn("issue:3", messages)
        chat = next(m for m in messages.values() if m.source == "chat")
        self.assertEqual((chat.author, chat.label, chat.text, chat.day), ("kim", "#general", "ship it", "2026-01-01"))
        self.assertEqual((messages["note:adr-1.md"].title, messages["note:adr-1.md"].day), ("Use Postgres", "2026-01-03"))
        self.assertEqual(messages["note:log:2026-01-02"].body, "note one")  # the corrupt line beside it is skipped
        self.assertEqual(len(messages), 5)

    def test_pull_github_reports_a_missing_or_failing_gh(self):
        failed = types.SimpleNamespace(returncode=1, stdout="", stderr="gh: not logged in")
        with tempfile.TemporaryDirectory() as tmp, mock.patch("docweave.comms.subprocess.run", return_value=failed):
            with self.assertRaisesRegex(RuntimeError, "not logged in"):
                pull_github(Path(tmp), Path(tmp) / "comms")
        ok = types.SimpleNamespace(returncode=0, stdout="[]", stderr="")
        with tempfile.TemporaryDirectory() as tmp, mock.patch("docweave.comms.subprocess.run", return_value=ok) as run:
            written = pull_github(Path(tmp), Path(tmp) / "comms")
            self.assertEqual([p.name for p in written], ["github-prs.json", "github-issues.json"])
            self.assertEqual(run.call_args_list[0].args[0][:3], ["gh", "pr", "list"])


class WatchTests(unittest.TestCase):
    def test_watch_builds_then_rebuilds_when_a_file_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "app.py"
            source.write_text('def run(port):\n    """Start."""\n    return port\n', encoding="utf-8")
            args = build_parser().parse_args(["watch", "--root", str(root), "--no-git", "--interval", "0"])
            args.cycles = 1
            out = io.StringIO()
            with redirect_stdout(out):
                self.assertEqual(args.func(args), 0)
                self.assertTrue((root / "docs" / "api" / "app.md").is_file())
                args.cycles = 1
                self.assertEqual(args.func(args), 0)
            self.assertEqual(out.getvalue().count("initial build"), 2)

            # Within one watch session: a change on disk between polls triggers exactly one rebuild.
            snapshots = iter([lambda: None, lambda: source.write_text('def run(port, host):\n    """Start."""\n    return port\n', encoding="utf-8")])
            real_sleep = __import__("time").sleep

            def edit_then_sleep(_seconds):
                next(snapshots)()
                real_sleep(0.05)

            args.cycles = 3
            out = io.StringIO()
            with redirect_stdout(out), mock.patch("docweave.cli.time.sleep", edit_then_sleep):
                args.func(args)
            self.assertIn("changed: app.py", out.getvalue())
            self.assertIn("def run(port, host)", (root / "docs" / "api" / "app.md").read_text(encoding="utf-8"))


class RenderWithoutGitTests(unittest.TestCase):
    def test_plain_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "app.py").write_text('"""App."""\n\n\ndef run(port):\n    return port\n', encoding="utf-8")
            a = analyze(load_config(root), use_git=False)
            files = render.render(a)
            self.assertEqual(set(files), {"docs/index.md", "docs/architecture.md", "docs/health.md", "docs/api/app.md"})
            self.assertIn("this description is inferred from the name", files["docs/api/app.md"])
            self.assertEqual(a.health.documented, 0)


if __name__ == "__main__":
    unittest.main()
