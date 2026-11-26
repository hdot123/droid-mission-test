"""Kruskal minimum spanning tree.

Given an undirected weighted graph, compute a minimum spanning tree (MST):
n - 1 edges covering all n nodes with minimum total weight. This is a
minimum spanning tree problem, not a shortest-path (dijkstra-class) problem.
"""

from __future__ import annotations


def _is_int(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _is_number(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def kruskal_mst(
    num_nodes: int, edges: list[tuple[int, int, float]]
) -> tuple[float, list[tuple[int, int, float]]]:
    """Return (MST total weight, MST edge table) for the given graph.

    Node indices must be in 0..num_nodes-1. Each edge is normalized to
    (min, max, w) and processed in canonical order (w, min, max); the
    returned edge table is exactly in that order. Parallel edges are
    allowed. Self-loops raise ValueError; a disconnected graph raises
    ValueError; num_nodes < 1 raises ValueError; node indices outside
    0..n-1 raise ValueError. num_nodes and node indices must be int
    (bool excluded) and weights must be numeric (bool excluded),
    otherwise TypeError. n == 1 returns (0, []).
    """
    if not _is_int(num_nodes):
        raise TypeError("num_nodes must be an int (bool is not accepted)")
    if num_nodes < 1:
        raise ValueError("num_nodes must be >= 1")

    normalized: list[tuple[int, int, float]] = []
    for edge in edges:
        try:
            u, v, w = edge
        except (TypeError, ValueError) as exc:
            raise TypeError(
                "each edge must be a (u, v, w) triple of two ints and a number"
            ) from exc
        if not _is_int(u) or not _is_int(v):
            raise TypeError("node indices must be ints (bool is not accepted)")
        if not _is_number(w):
            raise TypeError("edge weight must be numeric (bool is not accepted)")
        if u == v:
            raise ValueError("self-loop edge is not allowed")
        if not (0 <= u < num_nodes and 0 <= v < num_nodes):
            raise ValueError("node index out of range 0..num_nodes-1")
        lo, hi = (u, v) if u < v else (v, u)
        normalized.append((lo, hi, w))

    # Canonical processing order: (w, min, max).
    normalized.sort(key=lambda e: (e[2], e[0], e[1]))

    if num_nodes == 1:
        return (0, [])

    parent = list(range(num_nodes))
    rank = [0] * num_nodes

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    mst: list[tuple[int, int, float]] = []
    total = 0
    for u, v, w in normalized:
        ru, rv = find(u), find(v)
        if ru == rv:
            continue
        if rank[ru] < rank[rv]:
            parent[ru] = rv
        elif rank[ru] > rank[rv]:
            parent[rv] = ru
        else:
            parent[rv] = ru
            rank[ru] += 1
        mst.append((u, v, w))
        total = total + w
        if len(mst) == num_nodes - 1:
            break

    if len(mst) != num_nodes - 1:
        raise ValueError("graph is disconnected; no spanning tree exists")
    return (total, mst)
