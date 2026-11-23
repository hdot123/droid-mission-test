# Handoff: graph (sub-issue #819)

## What was requested

Process card #819 under work order #812 (round 54, concurrent card A): implement
the undirected unweighted graph component — new files `graph.py` and
`tests/test_graph.py` only. No existing files may be modified; standard library
only; must not import `easterorthodox` or `damm`. Every acceptance point in the
spec must have a corresponding test case. Checks, verbatim:

- `python3 -m pytest tests/test_graph.py -q`
- `python3 -m pytest tests/ -q`

## What I did

- Added `graph.py` with class `Graph` (adjacency list of `str` nodes):
  - `add_node(v)`: TypeError on non-str, idempotent for existing nodes.
  - `add_edge(u, v)`: TypeError on non-str endpoints, ValueError on self-loop
    `u == v`, auto-adds missing endpoints, duplicate edges are a no-op,
    undirected (registered both directions).
  - `nodes()`, `neighbors(v)`: lexicographic ascending lists; `neighbors`
    raises ValueError for unknown `v`.
  - `bfs(start)`: deque-based; enqueues unvisited neighbors in lexicographic
    order on dequeue; only the component of `start`; ValueError if missing.
  - `dfs(start)`: recursive preorder equivalent (visit, then recurse into
    unvisited neighbors lexicographically); only the component of `start`;
    ValueError if missing.
  - `connected_components()`: each component lexicographic-ascending, ordered
    by each component's smallest element ascending.
  - `has_path(u, v)`: ValueError if either endpoint missing; True for `u == v`
    when both are in the graph; otherwise checks membership in `bfs(u)`.
- Added `tests/test_graph.py` (17 tests) covering every acceptance point
  verbatim from the spec: the reference graph G (edges a-b, a-c, b-d, c-d, d-e
  plus isolated z) with all listed `nodes`/`neighbors`/`bfs`/`dfs`/
  `connected_components`/`has_path` expectations, graph G2 (m-n, m-o, n-p,
  o-p, p-q) bfs/dfs expectations, the empty-graph cases, all ValueError cases
  (self-loop, `neighbors("q")`, `bfs("q")`, `has_path("a", "q")`), all
  TypeError cases (`add_node(1)`, `add_edge("a", 2)`), and the duplicate-edge
  no-op check (`add_edge("a", "b")` again leaves `neighbors("a") == ["b", "c"]`).
  A few extra defensive tests (idempotent `add_node`, non-str endpoints on the
  other side of `add_edge`, `has_path` with a missing first endpoint and on an
  empty graph) were added as hardening; they are consistent with the spec.

## What I did not do

- Did not touch `easterorthodox.py`, `damm.py`, or any existing file (those
  belong to other process cards).
- Did not modify `tests/test_roman.py`, `legacy_stringkit.py`, `roman.py`, or
  any other pre-existing file.
- Did not import anything outside the standard library (`collections.deque`
  only), and no cross-imports of the sibling components.
- Did not commit or push (the workflow does that).
- `team/` files are process artifacts required by the work order, not part of
  the six-file deliverable list.

## Checks run and results

1. `python3 -m pytest tests/test_graph.py -q` → `17 passed in 0.03s` (exit 0)
2. `python3 -m pytest tests/ -q` → `204 passed, 2 skipped in 16.44s` (exit 0)

Note: pytest was initially missing from the environment; I installed
`requirements-dev.txt` (jsonschema, pytest) first — no repo files changed by
that install. The 2 skips are pre-existing suite skips, unrelated to this card.
No `verdict.json` / `verdict.md` by-products appeared in the repo root (checked
and removed defensively with `rm -f`).

## What the validator must pay attention to

- The DFS order in the spec is the *recursive* preorder, not a stack-based
  iterative simulation (they differ on this graph: the spec requires
  `G.dfs("a") == ["a", "b", "d", "c", "e"]`, which the recursive definition
  yields and a naive stack-with-reversed-neighbors loop can also yield — but
  the test pins the exact expected list, so any divergence fails).
- BFS must enqueue unvisited neighbors in lexicographic order *at dequeue
  time*; the test pins `G.bfs("a") == ["a", "b", "c", "d", "e"]` and
  `G2.bfs("m") == ["m", "n", "o", "p", "q"]`.
- `connected_components()` ordering (by minimum element) is pinned by
  `[["a", "b", "c", "d", "e"], ["z"]]`.
- Duplicate `add_edge("a", "b")` must leave `neighbors("a") == ["b", "c"]`
  (no duplication, no reordering).
- Both checks are green as required; the full-suite result (204 passed,
  2 skipped) matches the baseline behavior of the untouched suite.
