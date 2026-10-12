"""Module dependency graph: internal edges, external dependencies, cycles and a Mermaid drawing."""

from __future__ import annotations

import re
import sys

from .model import Project

_NODE_BUILTINS = {"fs", "path", "os", "http", "https", "url", "util", "crypto", "events", "child_process", "stream"}


def internal_edges(project: Project) -> dict[str, set[str]]:
    """Map each module to the project modules it imports."""
    names = set(project.modules)
    edges: dict[str, set[str]] = {name: set() for name in names}
    for module in project.modules.values():
        for imp in module.imports:
            target = imp if imp in names else imp.rpartition(".")[0]
            if target in names and target != module.name:
                edges[module.name].add(target)
    return edges


def external_dependencies(project: Project) -> list[str]:
    """Third-party packages the project imports (standard-library modules are left out)."""
    roots = {name.split(".")[0] for name in project.modules}
    found: set[str] = set()
    for module in project.modules.values():
        for imp in module.imports:
            if module.language == "python":
                top = imp.split(".")[0]
                if top and top not in roots and top not in sys.stdlib_module_names:
                    found.add(top)
            elif imp.startswith("npm:"):  # the JS analyzer tags non-relative specifiers this way
                spec = imp[4:].removeprefix("node:")
                top = "/".join(spec.split("/")[:2]) if spec.startswith("@") else spec.split("/")[0]
                if top not in _NODE_BUILTINS:
                    found.add(top)
    return sorted(found)


def cycles(edges: dict[str, set[str]]) -> list[list[str]]:
    """Import cycles, as strongly connected components with more than one module (Tarjan)."""
    index: dict[str, int] = {}
    low: dict[str, int] = {}
    stack: list[str] = []
    on_stack: set[str] = set()
    found: list[list[str]] = []

    def visit(root: str) -> None:
        work = [(root, iter(sorted(edges.get(root, ()))))]
        index[root] = low[root] = len(index)
        stack.append(root)
        on_stack.add(root)
        while work:
            node, it = work[-1]
            advanced = False
            for nxt in it:
                if nxt not in index:
                    index[nxt] = low[nxt] = len(index)
                    stack.append(nxt)
                    on_stack.add(nxt)
                    work.append((nxt, iter(sorted(edges.get(nxt, ())))))
                    advanced = True
                    break
                if nxt in on_stack:
                    low[node] = min(low[node], index[nxt])
            if advanced:
                continue
            work.pop()
            if work:
                low[work[-1][0]] = min(low[work[-1][0]], low[node])
            if low[node] == index[node]:
                component = []
                while True:
                    top = stack.pop()
                    on_stack.discard(top)
                    component.append(top)
                    if top == node:
                        break
                if len(component) > 1:
                    found.append(sorted(component))

    for name in sorted(edges):
        if name not in index:
            visit(name)
    return sorted(found)


def _node_id(name: str) -> str:
    return "m_" + re.sub(r"\W", "_", name)


def mermaid(edges: dict[str, set[str]], collapse_over: int = 40) -> str:
    """Draw the dependency graph; large projects are collapsed to one node per package."""
    if len(edges) > collapse_over:
        package = lambda n: n.rpartition(".")[0] or n  # noqa: E731
        collapsed: dict[str, set[str]] = {}
        for src, targets in edges.items():
            collapsed.setdefault(package(src), set()).update(package(t) for t in targets if package(t) != package(src))
        edges = collapsed
    groups: dict[str, list[str]] = {}
    for name in sorted(edges):
        groups.setdefault(name.rpartition(".")[0], []).append(name)
    lines = ["graph LR"]
    for group, members in sorted(groups.items()):
        indent = "  "
        if group and len(members) > 1:
            lines.append(f'  subgraph {_node_id("pkg." + group)}["{group}"]')
            indent = "    "
        for name in members:
            label = name[len(group) + 1 :] if group and len(members) > 1 else name
            lines.append(f'{indent}{_node_id(name)}["{label}"]')
        if group and len(members) > 1:
            lines.append("  end")
    for src in sorted(edges):
        for dst in sorted(edges[src]):
            lines.append(f"  {_node_id(src)} --> {_node_id(dst)}")
    return "\n".join(lines)
