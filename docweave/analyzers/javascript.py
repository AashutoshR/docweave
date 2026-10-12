"""Structural analysis of JavaScript / TypeScript.

There is no JS parser in the Python standard library, so this is a scanner rather than a full
parser. It blanks out comments and strings, finds the *head* of each declaration with a regular
expression, and then walks balanced brackets to find its parameter list, return type and body -
which is what lets it cope with callback types, object-literal types and multi-line signatures.

It understands top-level functions, arrow functions and function expressions assigned to
constants or to ``exports.x``, classes with their methods and arrow-function properties,
TypeScript interfaces, type aliases and enums, JSDoc blocks, and ES / CommonJS imports and exports.
Declarations nested inside other functions are deliberately ignored.
"""

from __future__ import annotations

import hashlib
import posixpath
import re
from bisect import bisect_right

from ..model import Module, Param, Symbol

EXTENSIONS = (".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx")

_ID = r"[A-Za-z_$][\w$]*"
_IDENT = re.compile(_ID)
_EXPORT = r"(?P<export>export\s+(?:default\s+)?)?"
_MODIFIERS = r"public|private|protected|static|async|override|readonly|abstract|declare|get|set"
_HEAD_FUNC = re.compile(rf"^{_EXPORT}(?:declare\s+)?(?P<async>async\s+)?function\s*\*?\s*(?P<name>{_ID})\s*", re.M)
_HEAD_ASSIGN = re.compile(
    rf"^(?:{_EXPORT}(?:const|let|var)\s+(?P<name>{_ID})\s*(?::[^=\n]+?)?|(?P<cjs>(?:module\.)?exports\.)(?P<name2>{_ID})\s*)"
    rf"=\s*(?P<async>async\s+)?(?P<fn>function\s*\*?\s*(?:{_ID})?\s*)?",
    re.M,
)
_HEAD_CLASS = re.compile(
    rf"^{_EXPORT}(?:declare\s+)?(?:abstract\s+)?class\s+(?P<name>{_ID})(?:\s*<[^>{{]*>)?"
    rf"(?:\s+extends\s+(?P<base>[\w$.]+))?[^{{]*\{{",
    re.M,
)
_HEAD_METHOD = re.compile(rf"^[ \t]+(?P<mods>(?:(?:{_MODIFIERS})\s+)*)\*?(?P<name>#?{_ID})\s*", re.M)
_HEAD_TYPE = re.compile(rf"^{_EXPORT}(?:declare\s+)?(?P<kind>interface|type|(?:const\s+)?enum)\s+(?P<name>{_ID})", re.M)
_IMPORT = re.compile(r"""(?:\bfrom\s+|\bimport\s+|\brequire\(\s*|\bimport\(\s*)(['"])(?P<spec>[^'"]+)\1""")
_CJS_OBJECT = re.compile(r"\bmodule\.exports\s*=\s*\{([^}]*)\}")
_CJS_SINGLE = re.compile(rf"\bmodule\.exports\s*=\s*(?:new\s+)?({_ID})")
_KEYWORDS = {"if", "for", "while", "switch", "catch", "function", "return", "else", "do", "try", "with", "new", "throw", "await", "yield", "typeof", "delete", "super"}
_BRANCH = re.compile(r"\b(?:if|for|while|case|catch)\b|&&|\|\||\?(?![.:?])")
_PARAM = re.compile(rf"({_ID})\??\s*((?:[:=].*)?)$", re.S)
_PARAM_MODIFIERS = re.compile(r"^(?:(?:public|private|protected|readonly|override)\s+)+")


def module_name(rel: str) -> str:
    """Dotted module name for a JS/TS file path (``src/cart/index.ts`` -> ``cart``)."""
    stem = posixpath.splitext(rel)[0]
    parts = stem.split("/")
    if len(parts) > 1 and parts[0] == "src":
        parts = parts[1:]
    if len(parts) > 1 and parts[-1] == "index":
        parts = parts[:-1]
    return ".".join(parts)


def _sha(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]


def mask(text: str, strings: bool = True) -> str:
    """Replace comments (and optionally string contents) with spaces, preserving offsets and newlines."""
    out = list(text)
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch == "/" and text[i + 1 : i + 2] == "/":
            j = text.find("\n", i)
            lo, hi = i, n if j == -1 else j
            nxt = hi
        elif ch == "/" and text[i + 1 : i + 2] == "*":
            j = text.find("*/", i + 2)
            lo, hi = i, n if j == -1 else j + 2
            nxt = hi
        elif ch in "'\"`":
            j = i + 1
            while j < n and text[j] != ch and (ch == "`" or text[j] != "\n"):
                j += 2 if text[j] == "\\" else 1
            nxt = min(j + 1, n)
            lo, hi = (i + 1, min(j, n)) if strings else (i, i)  # the quotes themselves are kept
        else:
            i += 1
            continue
        for k in range(lo, hi):
            if out[k] != "\n":
                out[k] = " "
        i = nxt
    return "".join(out)


def _match(masked: str, open_idx: int, opener: str = "{", closer: str = "}") -> int:
    """Index of the bracket that closes the one at ``open_idx``."""
    depth = 0
    for i in range(open_idx, len(masked)):
        if masked[i] == opener:
            depth += 1
        elif masked[i] == closer:
            depth -= 1
            if depth == 0:
                return i
    return len(masked) - 1


def _skip_ws(masked: str, i: int) -> int:
    while i < len(masked) and masked[i] in " \t\r\n":
        i += 1
    return i


def _skip_generics(masked: str, i: int) -> int | None:
    """Index just past a ``<...>`` type-parameter list starting at ``i`` (``i`` if there is none)."""
    if masked[i : i + 1] != "<":
        return i
    depth = 0
    for j in range(i, min(len(masked), i + 400)):
        if masked[j] == "<":
            depth += 1
        elif masked[j] == ">" and masked[j - 1] != "=":
            depth -= 1
            if depth == 0:
                return _skip_ws(masked, j + 1)
    return None


def _tail(masked: str, i: int, arrow: bool) -> tuple[tuple[int, int] | None, int, int | None] | None:
    """Scan what follows a parameter list: an optional return type, then ``{`` or ``=>``.

    Returns ``(return type span, end of the declaration head, index of the body's "{")``; the last
    is None for an expression-bodied arrow function. Returns None when there is no body at all
    (an overload, an abstract method, an interface member).
    """
    i = _skip_ws(masked, i)
    ret = None
    if masked[i : i + 1] == ":":
        start = j = i + 1
        depth = 0
        limit = min(len(masked), start + 600)
        while j < limit:
            c = masked[j]
            if arrow and depth == 0 and masked[j : j + 2] == "=>":
                break
            if c == "{":
                before = masked[start:j].rstrip()
                if arrow or depth > 0 or before[-1:] in ("", "|", "&", ",", ":", "<", "(") or before.endswith("=>"):
                    j = _match(masked, j) + 1  # an object-literal type, not the body
                    continue
                break
            if c in "(<[":
                depth += 1
            elif c in ")]" or (c == ">" and masked[j - 1] != "="):
                depth = max(0, depth - 1)
            elif c == ";" and depth == 0:
                return None
            j += 1
        else:
            return None
        ret, i = (start, j), j
    if arrow:
        if masked[i : i + 2] != "=>":
            return None
        after = _skip_ws(masked, i + 2)
        return ret, i + 2, (after if masked[after : after + 1] == "{" else None)
    if masked[i : i + 1] != "{":
        return None
    return ret, i, i


def _expr_end(masked: str, i: int) -> int:
    """Last index of the expression or type that starts at ``i`` (for bodies without braces)."""
    depth = 0
    for j in range(i, len(masked)):
        c = masked[j]
        if c in "([{":
            depth += 1
        elif c in ")]}":
            if depth == 0:
                return j - 1
            depth -= 1
        elif depth == 0 and c == ";":
            return j
        elif depth == 0 and c == "\n" and masked[i:j].strip():
            if masked[j + 1 :].lstrip(" \t")[:1] not in tuple(".?:+-*/|&"):
                return j - 1  # the next line does not continue this expression
    return len(masked) - 1


def _split_default(rest: str) -> tuple[str, str | None]:
    """Split ``": type = default"`` at the ``=`` that starts the default (not one inside ``=>``)."""
    depth = 0
    for i, ch in enumerate(rest):
        if ch in "([{<":
            depth += 1
        elif ch in ")]}" or (ch == ">" and rest[i - 1 : i] != "="):
            depth -= 1
        elif ch == "=" and depth <= 0 and rest[i + 1 : i + 2] not in (">", "=") and rest[i - 1 : i] not in ("=", "!", "<", ">"):
            return rest[:i], rest[i + 1 :].strip() or None
    return rest, None


def _split_params(raw: str) -> list[Param]:
    params: list[Param] = []
    depth, buf = 0, ""
    for ch in raw + ",":
        if ch in "([{<":
            depth += 1
        elif ch in ")]}" or (ch == ">" and not buf.endswith("=")):
            depth -= 1
        if ch == "," and depth <= 0:
            piece = " ".join(buf.split())
            buf = ""
            if not piece:
                continue
            kind = "vararg" if piece.startswith("...") else "positional"
            piece = _PARAM_MODIFIERS.sub("", piece.lstrip("."))
            m = _PARAM.match(piece)
            if m:
                annotation, default = _split_default(m[2])
                params.append(Param(m[1], annotation.lstrip(":").strip() or None, default, kind))
            else:  # destructured parameter: cannot be checked by name
                params.append(Param("{...}", None, None, "kwarg"))
        else:
            buf += ch
    return params


def _jsdoc(lines: list[str], lineno: int) -> tuple[str | None, tuple[int, int] | None]:
    """Find the ``/** ... */`` block that ends on the line directly above ``lineno``."""
    end = lineno - 2
    while end >= 0 and lines[end].strip().startswith("@"):  # decorators
        end -= 1
    if end < 0 or not lines[end].rstrip().endswith("*/"):
        return None, None
    start = end
    while start >= 0 and "/**" not in lines[start]:
        if start < end and "*/" in lines[start]:
            return None, None
        start -= 1
    if start < 0:
        return None, None
    body = "\n".join(lines[start : end + 1])
    body = re.sub(r"^\s*/\*\*+", "", body)
    body = re.sub(r"\*+/\s*$", "", body)
    cleaned = [re.sub(r"^\s*\* ?", "", ln) for ln in body.split("\n")]
    return "\n".join(cleaned).strip() or None, (start + 1, end + 1)


class _Scanner:
    def __init__(self, rel: str, text: str) -> None:
        self.rel = rel
        self.text = text
        self.name = module_name(rel)
        self.masked = mask(text)
        self.code = mask(text, strings=False)  # comments removed, strings kept: used for hashing
        self.lines = text.split("\n")
        self.starts = [0]
        for line in self.lines[:-1]:
            self.starts.append(self.starts[-1] + len(line) + 1)
        self.uses_esm = bool(re.search(r"^export\b", self.masked, re.M))
        self.cjs_names: set[str] | None = None
        if m := _CJS_OBJECT.search(self.masked):
            self.cjs_names = set(_IDENT.findall(m[1]))
        elif m := _CJS_SINGLE.search(self.masked):
            self.cjs_names = {m[1]}
        self.symbols: list[Symbol] = []

    def line_of(self, offset: int) -> int:
        return bisect_right(self.starts, offset)

    def add(self, kind: str, name: str, start: int, head_end: int, end: int, *, name_at: int, body_open: int | None = None,
            parent: Symbol | None = None, params: str | None = None, ret: tuple[int, int] | None = None,
            exported: bool = False, is_async: bool = False, mods: str = "", base: str | None = None) -> Symbol:
        lineno = self.line_of(name_at)
        qualname = f"{parent.qualname}.{name}" if parent else name
        signature = " ".join(self.text[start:head_end].split()).rstrip("{").strip()
        doc, doc_range = _jsdoc(self.lines, self.line_of(start))
        if parent is not None:
            public = parent.is_public and not name.startswith(("#", "_")) and "private" not in mods
        elif self.uses_esm:
            public = exported and not name.startswith("_")
        else:
            public = (exported or self.cjs_names is None or name in self.cjs_names) and not name.startswith("_")
        sym = Symbol(
            id=f"{self.name}:{qualname}", name=name, qualname=qualname, kind=kind, module=self.name, file=self.rel,
            language="javascript", lineno=lineno, end_lineno=max(lineno, self.line_of(end)), sig_end=max(lineno, self.line_of(head_end)),
            signature=signature, docstring=doc, doc_range=doc_range, parent=parent.id if parent else None,
            is_public=public, is_async=is_async or "async" in mods, bases=[base] if base else [],
        )
        if kind in ("function", "method"):
            sym.params = _split_params(params or "")
            sym.returns = self.text[ret[0] : ret[1]].strip() if ret else None
            inner = self.masked[(body_open if body_open is not None else head_end) : end + 1]
            sym.returns_value = body_open is None or bool(re.search(r"\breturn\s+[^;\s}]|\byield\b", inner))
            sym.raises = sorted(set(re.findall(rf"\bthrow\s+new\s+({_ID})", inner)))
            sym.calls = sorted(set(re.findall(rf"\b((?:{_ID}\.)*{_ID})\s*\(", inner)) - _KEYWORDS - {name})
            sym.complexity = 1 + len(_BRANCH.findall(inner))
            sym.is_stub = body_open is not None and not inner.strip("{} \n\t")
        sym.interface_hash = _sha(signature)
        sym.body_hash = _sha(" ".join(self.code[start : end + 1].split()))
        self.symbols.append(sym)
        return sym

    def callable_at(self, p: int, arrow: bool):
        """Parse ``(params) [: type] {`` or ``(params) [: type] =>`` starting at the ``(`` at ``p``."""
        close = _match(self.masked, p, "(", ")")
        tail = _tail(self.masked, close + 1, arrow)
        if tail is None:
            return None
        ret, head_end, body_open = tail
        end = _match(self.masked, body_open) if body_open is not None else _expr_end(self.masked, head_end)
        return self.text[p + 1 : close], ret, head_end, body_open, end

    def assigned_function(self, m: re.Match, p: int, *, kind: str, name: str, start: int, parent: Symbol | None = None,
                          exported: bool = False, mods: str = "") -> Symbol | None:
        """Handle ``= [async] (params) => ...``, ``= x => ...`` and ``= function (params) {...}`` at ``p``."""
        masked = self.masked
        is_function = bool(m.groupdict().get("fn"))
        p = _skip_generics(masked, p)
        if p is None:
            return None
        common = dict(name_at=m.start("name") if m["name"] else m.start("name2"), parent=parent, exported=exported,
                      is_async=bool(m.groupdict().get("async")), mods=mods)
        if masked[p : p + 1] == "(":
            parsed = self.callable_at(p, arrow=not is_function)
            if parsed is None:
                return None
            params, ret, head_end, body_open, end = parsed
            return self.add(kind, name, start, head_end, end, body_open=body_open, params=params, ret=ret, **common)
        single = _IDENT.match(masked, p)
        if is_function or not single:
            return None
        arrow_at = _skip_ws(masked, single.end())
        if masked[arrow_at : arrow_at + 2] != "=>":
            return None
        after = _skip_ws(masked, arrow_at + 2)
        body_open = after if masked[after : after + 1] == "{" else None
        end = _match(masked, body_open) if body_open is not None else _expr_end(masked, arrow_at + 2)
        return self.add(kind, name, start, arrow_at + 2, end, body_open=body_open, params=single.group(0), **common)

    def scan(self) -> None:
        masked = self.masked
        for m in _HEAD_FUNC.finditer(masked):
            p = _skip_generics(masked, m.end())
            if p is None or masked[p : p + 1] != "(":
                continue
            if parsed := self.callable_at(p, arrow=False):
                params, ret, head_end, body_open, end = parsed
                self.add("function", m["name"], m.start(), head_end, end, name_at=m.start("name"), body_open=body_open,
                         params=params, ret=ret, exported=bool(m["export"]), is_async=bool(m["async"]))

        for m in _HEAD_ASSIGN.finditer(masked):
            self.assigned_function(m, m.end(), kind="function", name=m["name"] or m["name2"], start=m.start(),
                                   exported=bool(m["export"] or m["cjs"]))

        for m in _HEAD_CLASS.finditer(masked):
            open_idx = m.end() - 1
            close = _match(masked, open_idx)
            klass = self.add("class", m["name"], m.start(), open_idx, close, name_at=m.start("name"),
                             exported=bool(m["export"]), base=m["base"])
            depth, depth_at = 0, {}
            for i in range(open_idx, close + 1):
                if masked[i] == "{":
                    depth += 1
                elif masked[i] == "}":
                    depth -= 1
                elif masked[i] == "\n":
                    depth_at[i + 1] = depth
            for mm in _HEAD_METHOD.finditer(masked, open_idx + 1, close):
                name, mods = mm["name"], mm["mods"] or ""
                if depth_at.get(mm.start()) != 1 or name in _KEYWORDS:
                    continue
                p = _skip_generics(masked, mm.end())
                if p is None:
                    continue
                method = None
                if masked[p : p + 1] == "(":
                    if parsed := self.callable_at(p, arrow=False):
                        params, ret, head_end, body_open, end = parsed
                        method = self.add("method", name, mm.start("mods"), head_end, end, name_at=mm.start("name"), body_open=body_open,
                                          parent=klass, params=params, ret=ret, mods=mods)
                elif masked[p : p + 1] == "=" and masked[p : p + 2] != "==":  # handler = (e) => {...}
                    q = _skip_ws(masked, p + 1)
                    is_async = masked[q : q + 6] == "async "
                    q = _skip_ws(masked, q + 5) if is_async else q
                    if masked[q : q + 1] == "(" and (parsed := self.callable_at(q, arrow=True)):
                        params, ret, head_end, body_open, end = parsed
                        method = self.add("method", name, mm.start("mods"), head_end, end, name_at=mm.start("name"), body_open=body_open,
                                          parent=klass, params=params, ret=ret, mods=mods, is_async=is_async)
                if method is not None and method.name == "constructor":
                    klass.params = method.params
                    method.is_public = method.is_public and bool(method.docstring)

        if self.rel.lower().endswith((".ts", ".tsx")):
            for m in _HEAD_TYPE.finditer(masked):
                kind = "enum" if "enum" in m["kind"] else m["kind"]
                if kind == "type":
                    end = _expr_end(masked, m.end())
                else:
                    brace = masked.find("{", m.end())
                    if brace == -1:
                        continue
                    end = _match(masked, brace)
                self.add(kind, m["name"], m.start(), m.end(), end, name_at=m.start("name"), exported=bool(m["export"]))


def analyze(rel: str, text: str) -> Module:
    """Scan one JS/TS file into a :class:`Module`."""
    text = text.replace("\r\n", "\n")
    scanner = _Scanner(rel, text)
    module = Module(name=scanner.name, file=rel, language="javascript", loc=text.count("\n") + 1)
    here = posixpath.dirname(rel)
    for m in _IMPORT.finditer(scanner.code):
        spec = m["spec"]
        if spec.startswith("."):
            module.imports.append(module_name(posixpath.normpath(posixpath.join(here, spec)) + ".js"))
        else:
            module.imports.append(f"npm:{spec}")
    module.imports = sorted(set(module.imports))
    # A leading /** block */ followed by a blank line documents the file itself.
    lines = scanner.lines
    if lines and lines[0].lstrip().startswith("/**"):
        end = next((i for i, ln in enumerate(lines) if "*/" in ln), None)
        if end is not None and end + 1 < len(lines) and not lines[end + 1].strip():
            module.docstring = _jsdoc(lines, end + 2)[0]
    scanner.scan()
    module.symbols = sorted(scanner.symbols, key=lambda s: (s.lineno, s.qualname))
    return module
