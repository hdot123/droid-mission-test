# Handoff: dijkstra (sub-issue #766)

## What was requested

Process card for work order #762 (第52轮并发B单): implement `dijkstra.py` and `tests/test_dijkstra.py` only, per the verbatim spec:

- Graph is a dict of node name (str) → adjacency dict (neighbor → weight). Directed edges; neighbor-only nodes have no outgoing edges.
- Weights must be int/float (bool rejected); non-numeric → TypeError; negative → ValueError; non-dict graph/adjacency or non-str node name → TypeError.
- `dijkstra(graph, source) -> (dist, prev)`: dist covers every node (key or neighbor), reachable = shortest distance (source 0), unreachable = `math.inf`; prev holds only reachable non-source → predecessor; source not in graph → ValueError.
- `shortest_path(graph, source, target) -> list`: both ends included, unreachable `[]`, source == target `[source]`, either endpoint missing → ValueError.
- Every acceptance item (G1/G2/G3 examples plus all error cases) needs a test case. Stdlib only; no imports of nthprime/windscale; no edits to existing files.

## What I did

- Created `dijkstra.py` (new): validation (`_validate_graph`) that walks the whole graph up front (rejects non-dict graph, non-str node names, non-dict adjacency, bool/non-numeric weights, negative weights), a classic Dijkstra over the collected node set using `math.inf` for unreachable nodes, and `shortest_path` that reuses `dijkstra` and walks `prev` back from target. Source/target existence is checked before the source==target shortcut so missing endpoints still raise ValueError.
- Created `tests/test_dijkstra.py` (new): 10 test functions covering every acceptance item — G1 dist/prev (A=0, B=1, C=3, D=4, E=inf, prev `{B:A, C:B, D:C}`), all five G1 path cases including the directed non-reversible `D→A == []`, G2 float weights (T==2.0, U==1.5, prev `{U:S, T:U}`, path `S,U,T`), G3 single edge, and the six error cases (negative weight, source Z, target Z → ValueError; list graph, "x" weight, True weight → TypeError).

## What I did not do

- Did not touch `nthprime.py`, `windscale.py`, or any pre-existing file (only the two owned files plus the two team files below were written).
- Did not commit or push.
- Did not import anything beyond the standard library (`math`) and pytest in tests; no cross-module imports.

## Checks run and results

1. `python3 -m pytest tests/test_dijkstra.py -q` → **10 passed** (exit 0).
2. `python3 -m pytest tests/ -q` → **147 passed, 1 skipped** (exit 0; the skip is a pre-existing test in the baseline, unrelated to this change).

Note: pytest was not present in the environment; installed from the repo's own `requirements-dev.txt` (`pytest>=7.4.0`, resolved to 9.2.0). No repo files were modified by that install.

## What the validator must pay attention to

- Both checks are green as written; the full-suite run includes other workers' concurrent files if they landed, so a full-suite count above 148 may reflect their additions, not mine.
- `shortest_path` validates the graph twice (once directly, once via `dijkstra`) — intentional for clear error precedence (missing endpoint beats weight errors is not required by spec; both paths validate the graph identically first, so any graph-level TypeError/ValueError fires before endpoint checks only insofar as `_validate_graph` runs first in both functions).
- `prev` excludes the source and unreachable nodes by construction (only set on successful relaxation); `dist` keys come from a set, so dict key order is unspecified — tests assert by key, not order.
