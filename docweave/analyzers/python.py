"""Static analysis of Python source using the standard ``ast`` module."""

from __future__ import annotations

import ast
import hashlib
from pathlib import PurePosixPath

from ..model import Module, Param, Symbol

EXTENSIONS = (".py",)


def module_name(rel: str) -> str:
    """Dotted module name for a Python file path (``src/pkg/mod.py`` -> ``pkg.mod``)."""
    parts = list(PurePosixPath(rel).with_suffix("").parts)
    if len(parts) > 1 and parts[0] == "src":
        parts = parts[1:]
    if len(parts) > 1 and parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def _sha(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]


def _src(node: ast.AST | None) -> str | None:
    return ast.unparse(node) if node is not None else None


def _dotted(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _dotted(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    if isinstance(node, ast.Call):
        return _dotted(node.func)
    return None


def _complexity(node: ast.AST) -> int:
    """McCabe-style cyclomatic complexity."""
    score = 1
    for n in ast.walk(node):
        if isinstance(n, (ast.If, ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler, ast.IfExp, ast.Assert, ast.match_case)):
            score += 1
        elif isinstance(n, ast.BoolOp):
            score += len(n.values) - 1
        elif isinstance(n, ast.comprehension):
            score += 1 + len(n.ifs)
    return score


def _params(args: ast.arguments, drop_receiver: bool) -> list[Param]:
    out: list[Param] = []
    positional = args.posonlyargs + args.args
    defaults = [None] * (len(positional) - len(args.defaults)) + list(args.defaults)
    for a, d in zip(positional, defaults):
        out.append(Param(a.arg, _src(a.annotation), _src(d), "positional"))
    if args.vararg:
        out.append(Param(args.vararg.arg, _src(args.vararg.annotation), None, "vararg"))
    for a, d in zip(args.kwonlyargs, args.kw_defaults):
        out.append(Param(a.arg, _src(a.annotation), _src(d), "keyword"))
    if args.kwarg:
        out.append(Param(args.kwarg.arg, _src(args.kwarg.annotation), None, "kwarg"))
    if drop_receiver and out and out[0].name in ("self", "cls", "mcs"):
        out = out[1:]
    return out


def _is_stub(body: list[ast.stmt]) -> bool:
    for stmt in body:
        if isinstance(stmt, ast.Pass):
            continue
        if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant):
            continue
        if isinstance(stmt, ast.Raise) and stmt.exc is not None and _dotted(stmt.exc) == "NotImplementedError":
            continue
        return False
    return True


def _doc_range(node: ast.AST) -> tuple[int, int] | None:
    body = getattr(node, "body", None)
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
        return body[0].lineno, body[0].end_lineno or body[0].lineno
    return None


def _leading_comment(lines: list[str], lineno: int) -> tuple[str | None, tuple[int, int] | None]:
    """Comment block directly above ``lineno`` (1-based), used as documentation for constants."""
    i = lineno - 2
    found: list[str] = []
    while i >= 0 and lines[i].lstrip().startswith("#"):
        found.append(lines[i].lstrip().lstrip("#:").strip())
        i -= 1
    if not found:
        return None, None
    return " ".join(reversed(found)), (i + 2, lineno - 1)


class _Builder:
    def __init__(self, rel: str, text: str, tree: ast.Module) -> None:
        self.rel = rel
        self.lines = text.split("\n")
        self.module = module_name(rel)
        self.symbols: list[Symbol] = []
        self.exported = self._dunder_all(tree)

    @staticmethod
    def _dunder_all(tree: ast.Module) -> set[str] | None:
        for stmt in tree.body:
            if isinstance(stmt, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "__all__" for t in stmt.targets):
                if isinstance(stmt.value, (ast.List, ast.Tuple)):
                    return {e.value for e in stmt.value.elts if isinstance(e, ast.Constant) and isinstance(e.value, str)}
        return None

    def _public(self, name: str, parent: Symbol | None, documented: bool) -> bool:
        if parent is not None and not parent.is_public:
            return False
        if name == "__init__":
            return documented
        if name.startswith("_"):
            return False
        if parent is None and self.exported is not None:
            return name in self.exported
        return True

    def _base(self, node, name: str, kind: str, parent: Symbol | None, signature: str) -> Symbol:
        qualname = f"{parent.qualname}.{name}" if parent else name
        doc = ast.get_docstring(node) if not isinstance(node, (ast.Assign, ast.AnnAssign)) else None
        return Symbol(
            id=f"{self.module}:{qualname}", name=name, qualname=qualname, kind=kind, module=self.module,
            file=self.rel, language="python", lineno=node.lineno, end_lineno=node.end_lineno or node.lineno,
            sig_end=node.lineno, signature=signature, docstring=doc, doc_range=_doc_range(node),
            parent=parent.id if parent else None, is_public=self._public(name, parent, bool(doc)),
        )

    def function(self, node: ast.FunctionDef | ast.AsyncFunctionDef, parent: Symbol | None) -> None:
        is_async = isinstance(node, ast.AsyncFunctionDef)
        sig = f"{'async def' if is_async else 'def'} {node.name}({ast.unparse(node.args)})"
        if node.returns is not None:
            sig += f" -> {ast.unparse(node.returns)}"
        sym = self._base(node, node.name, "method" if parent else "function", parent, sig)
        sym.is_async = is_async
        sym.sig_end = max(node.lineno, node.body[0].lineno - 1)
        sym.decorators = [ast.unparse(d) for d in node.decorator_list]
        sym.params = _params(node.args, drop_receiver=parent is not None)
        sym.returns = _src(node.returns)
        body = node.body[1:] if sym.doc_range else node.body
        sym.is_stub = _is_stub(body) or any(d.split(".")[-1] in ("abstractmethod", "overload") for d in sym.decorators)
        calls: list[str] = []
        raises: list[str] = []
        for n in ast.walk(node):
            if isinstance(n, ast.Call) and (name := _dotted(n.func)):
                calls.append(name)
            elif isinstance(n, ast.Raise) and n.exc is not None and (name := _dotted(n.exc)):
                raises.append(name.split(".")[-1])
            elif isinstance(n, (ast.Yield, ast.YieldFrom)):
                sym.returns_value = True
            elif isinstance(n, ast.Return) and n.value is not None and not (isinstance(n.value, ast.Constant) and n.value.value is None):
                sym.returns_value = True
        sym.calls = sorted(set(calls))
        sym.raises = sorted(set(raises))
        sym.complexity = _complexity(node)
        sym.interface_hash = _sha(ast.dump(node.args) + (ast.dump(node.returns) if node.returns else "") + sig + "".join(sym.decorators))
        sym.body_hash = _sha("".join(ast.dump(s) for s in body))
        self.symbols.append(sym)

    def klass(self, node: ast.ClassDef, parent: Symbol | None) -> None:
        bases = [ast.unparse(b) for b in node.bases]
        sig = f"class {node.name}" + (f"({', '.join(bases)})" if bases else "")
        sym = self._base(node, node.name, "class", parent, sig)
        sym.sig_end = max(node.lineno, node.body[0].lineno - 1)
        sym.bases = bases
        sym.decorators = [ast.unparse(d) for d in node.decorator_list]
        init = next((n for n in node.body if isinstance(n, ast.FunctionDef) and n.name == "__init__"), None)
        if init is not None:
            sym.params = _params(init.args, drop_receiver=True)
        fields = [n for n in node.body if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name)]
        sym.interface_hash = _sha(sig + "".join(sym.decorators) + (ast.dump(init.args) if init else "") + "".join(ast.dump(f) for f in fields))
        sym.body_hash = _sha("".join(ast.dump(s) for s in (node.body[1:] if sym.doc_range else node.body)))
        sym.complexity = 1
        self.symbols.append(sym)
        for child in node.body:
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.function(child, sym)
            elif isinstance(child, ast.ClassDef):
                self.klass(child, sym)

    def constant(self, node: ast.Assign | ast.AnnAssign) -> None:
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        if len(targets) != 1 or not isinstance(targets[0], ast.Name) or node.value is None:
            return
        name = targets[0].id
        if not (name.isupper() and not name.startswith("_")) and not (self.exported and name in self.exported):
            return
        value = ast.unparse(node.value)
        annotation = f": {ast.unparse(node.annotation)}" if isinstance(node, ast.AnnAssign) else ""
        short = value if len(value) <= 80 else value[:77] + "..."
        sym = self._base(node, name, "constant", None, f"{name}{annotation} = {short}")
        sym.docstring, sym.doc_range = _leading_comment(self.lines, node.lineno)
        sym.interface_hash = _sha(name + annotation)
        sym.body_hash = _sha(value)
        self.symbols.append(sym)


def analyze(rel: str, text: str) -> Module:
    """Parse one Python file into a :class:`Module` with all of its documentable symbols."""
    module = Module(name=module_name(rel), file=rel, language="python", loc=text.count("\n") + 1)
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        module.error = f"syntax error on line {exc.lineno}: {exc.msg}"
        return module
    module.docstring = ast.get_docstring(tree)
    builder = _Builder(rel, text, tree)
    package = module.name if rel.endswith("__init__.py") else module.name.rpartition(".")[0]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            module.imports += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            base = node.module or ""
            if node.level:
                parts = package.split(".") if package else []
                parts = parts[: len(parts) - (node.level - 1)] if node.level > 1 else parts
                base = ".".join([*parts, base] if base else parts)
            # "from pkg import mod" may import a submodule, so record both candidates.
            module.imports += [base] + [f"{base}.{a.name}" for a in node.names if a.name != "*" and base]
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            builder.function(node, None)
        elif isinstance(node, ast.ClassDef):
            builder.klass(node, None)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            builder.constant(node)
    module.symbols = builder.symbols
    module.imports = sorted(set(i for i in module.imports if i))
    return module
