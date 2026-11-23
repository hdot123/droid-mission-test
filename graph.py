"""Undirected, unweighted graph with an adjacency-list representation.

Node names are restricted to ``str``. All iteration orders exposed by the
public API are lexicographic ascending, so results are deterministic.
"""

from __future__ import annotations

from collections import deque


class Graph:
    """Undirected unweighted graph stored as an adjacency list."""

    def __init__(self) -> None:
        self._adj: dict[str, set[str]] = {}

    def add_node(self, v) -> None:
        """Add ``v``; a non-str name raises TypeError, repeats are a no-op."""
        if not isinstance(v, str):
            raise TypeError(f"node name must be str, got {type(v).__name__}")
        if v not in self._adj:
            self._adj[v] = set()

    def add_edge(self, u, v) -> None:
        """Add the undirected edge ``u -- v``.

        Both endpoints must be str (TypeError otherwise), self-loops raise
        ValueError, missing endpoints are added automatically, and duplicate
        edges are a no-op.
        """
        if not isinstance(u, str):
            raise TypeError(f"node name must be str, got {type(u).__name__}")
        if not isinstance(v, str):
            raise TypeError(f"node name must be str, got {type(v).__name__}")
        if u == v:
            raise ValueError("self-loops are not allowed")
        self.add_node(u)
        self.add_node(v)
        self._adj[u].add(v)
        self._adj[v].add(u)

    def nodes(self) -> list:
        """All node names in lexicographic ascending order."""
        return sorted(self._adj)

    def neighbors(self, v) -> list:
        """Neighbors of ``v`` in lexicographic ascending order."""
        if v not in self._adj:
            raise ValueError(f"node {v!r} is not in the graph")
        return sorted(self._adj[v])

    def bfs(self, start) -> list:
        """Breadth-first visit order over ``start``'s connected component.

        On dequeue, each unvisited neighbor is enqueued in lexicographic
        ascending order.
        """
        if start not in self._adj:
            raise ValueError(f"node {start!r} is not in the graph")
        visited: set[str] = set()
        order: list[str] = []
        queue = deque([start])
        visited.add(start)
        while queue:
            node = queue.popleft()
            order.append(node)
            for nb in sorted(self._adj[node]):
                if nb not in visited:
                    visited.add(nb)
                    queue.append(nb)
        return order

    def dfs(self, start) -> list:
        """Depth-first preorder over ``start``'s connected component.

        Equivalent to the recursive definition: after visiting a node,
        recurse into each unvisited neighbor in lexicographic ascending
        order.
        """
        if start not in self._adj:
            raise ValueError(f"node {start!r} is not in the graph")
        visited: set[str] = set()
        order: list[str] = []

        def visit(node: str) -> None:
            visited.add(node)
            order.append(node)
            for nb in sorted(self._adj[node]):
                if nb not in visited:
                    visit(nb)

        visit(start)
        return order

    def connected_components(self) -> list[list]:
        """Connected components; each sorted, ordered by smallest element."""
        components: list[list[str]] = []
        seen: set[str] = set()
        for node in self.nodes():
            if node in seen:
                continue
            component = self.bfs(node)
            seen.update(component)
            components.append(component)
        return components

    def has_path(self, u, v) -> bool:
        """True when a path exists between ``u`` and ``v``."""
        if u not in self._adj:
            raise ValueError(f"node {u!r} is not in the graph")
        if v not in self._adj:
            raise ValueError(f"node {v!r} is not in the graph")
        return v in set(self.bfs(u))
