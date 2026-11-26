# Handoff: kruskal (sub-issue #894, work order #876 round-56 A unit)

## What was requested

Implement the Kruskal minimum spanning tree component as two new files only:

- `kruskal.py` at the repository root exposing `kruskal_mst(num_nodes: int, edges: list[tuple[int, int, float]]) -> tuple[float, list[tuple[int, int, float]]]`
- `tests/test_kruskal.py` covering every acceptance point verbatim from the process card

Spec highlights transcribed from the card:

- Edge normalization to `(min, max, w)`; process and return edges in canonical order `(w, min, max)`; parallel edges allowed.
- Self-loop → `ValueError`; disconnected graph → `ValueError`; `num_nodes < 1` → `ValueError`; node index outside `0..n-1` → `ValueError`; `num_nodes`/node index not `int` (bool included) → `TypeError`; weight not numeric (bool included) → `TypeError`; `n = 1` returns `(0, [])`.
- This is a minimum spanning tree (n-1 edges covering all nodes plus total weight), not a shortest-path/dijkstra-class problem.
- Standard library only; no import of `energyconv` or `unaccent`; no existing repository file may be modified.

## What I did

- Created `kruskal.py` with a union-find (path compression + union by rank) Kruskal implementation:
  - Type validation first: `num_nodes` must be `int` and not `bool` (`TypeError`), then `num_nodes < 1` (`ValueError`).
  - Each edge triple is validated: both endpoints must be `int` and not `bool` (`TypeError`), weight must be `int`/`float` and not `bool` (`TypeError`), self-loop (`u == v`) → `ValueError`, out-of-range endpoint → `ValueError`. Endpoints are normalized to `(min, max, w)`.
  - Normalized edges are sorted by `(w, min, max)` and processed greedily; the returned edge table is exactly in that order (break once `n - 1` edges are collected).
  - If fewer than `n - 1` edges are collected, the graph is disconnected → `ValueError`.
  - `n = 1` returns `(0, [])` (after validating an empty/any edge list; with `n == 1` any edge would be a self-loop or out of range anyway).
  - Total weight starts at `0` (int) so `kruskal_mst(1, []) == (0, [])` compares equal per the card's exact expected tuple.
- Created `tests/test_kruskal.py` with one test function per acceptance point, values transcribed verbatim:
  - `kruskal_mst(1, []) == (0, [])`
  - `kruskal_mst(2, [(0, 1, 7)]) == (7, [(0, 1, 7)])`
  - `kruskal_mst(3, [(0, 1, 1), (1, 2, 2), (0, 2, 3)]) == (3, [(0, 1, 1), (1, 2, 2)])`
  - Textbook 9-node graph: total `37`, edge table `[(6, 7, 1), (2, 8, 2), (5, 6, 2), (0, 1, 4), (2, 5, 4), (2, 3, 7), (0, 7, 8), (3, 4, 9)]`
  - Equal-weight tie → `[(0, 1, 5), (0, 2, 5)]`
  - Unordered endpoints → `[(0, 1, 1), (0, 2, 1)]`
  - Parallel edges → `(3, [(0, 1, 3)])`
  - `ValueError`: `(0, [])`, disconnected `(3, [(0, 1, 1)])`, self-loop `(2, [(0, 0, 1)])`, out-of-range `(2, [(0, 2, 1)])`
  - `TypeError`: `True`, `2.0`, `(0, True, 1)`, `(0, 1, "x")`
  - Extra guard case: `kruskal_mst(-1, [])` raises `ValueError`

## What I did not do

- Did not touch `energyconv.py`, `unaccent.py`, or any other worker's files.
- Did not modify any pre-existing repository file (only added the two owned files plus the two `team/` files required by the card instructions).
- Did not implement dijkstra/shortest-path behavior (out of scope by spec).
- Did not commit or push (workflow owns that).

## Checks run and results

From the repository root:

1. `python3 -m pytest tests/test_kruskal.py -q` → `16 passed in 0.02s`
2. `python3 -m pytest tests/ -q` → `358 passed, 2 skipped in 21.39s` (exit code 0)

The full-suite run did not leave `verdict.json` / `verdict.md` behind in this checkout; if pipeline by-products appear later they are outside this card.

## Notes for the validator

- Returned total for `n = 1` is int `0` (not `0.0`) so the exact equality `== (0, [])` in the card holds; for other graphs the total is a sum of the given weights (int weights yield an int total, e.g. `7`, `3`, `37`), which still compares equal to the card's expected numbers.
- The edge table ordering guarantee comes from sorting the normalized list by `(w, min, max)` before union-find processing; ties in `w` are broken by `(min, max)` as required.
- Edge validation happens before sorting, so `ValueError`/`TypeError` precedence is: type checks on `num_nodes`, then per-edge type checks, then self-loop/range `ValueError`s, then connectivity `ValueError` at the end.
- The module imports only `from __future__ import annotations` (standard library); no cross-imports of sibling components.
