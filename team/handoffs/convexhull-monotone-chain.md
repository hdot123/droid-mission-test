# Handoff: convexhull-monotone-chain (sub-issue #472)

## What was requested

Process card `convexhull-monotone-chain` under work order #458 (round 45, order D): create exactly two new files, `convexhull.py` and `tests/test_convexhull.py`, implementing `convex_hull(points)` with the monotone chain (Andrew) algorithm, per the verbatim spec in the work order's acceptance section (convex hull section). Constraints: only these two files plus the two team files; no modifications to any existing file; standard library only; no import of `porta` or `primorial`.

## What I did

- `convexhull.py`: implemented `convex_hull(points)` using monotone chain. Validation order and semantics follow the spec:
  - `points` not a `list`/`tuple` → `TypeError` (a string such as `"abc"` is rejected here).
  - a point that is not a 2-tuple → `ValueError`.
  - non-numeric coordinate → `TypeError`; `bool` coordinates are explicitly rejected (`isinstance(v, Number) and not isinstance(v, bool)`).
  - duplicates removed first via a `set`, then sorted lexicographically (`sorted(unique)`), which gives the required start point (smallest x, ties broken by smallest y) and the required `<3` results (0 → `[]`, 1 → the point, 2 → the two points sorted).
  - standard monotone chain builds the lower and upper chains with `cross <= 0` popping (so collinear edge points are dropped, keeping only endpoints), concatenating `lower[:-1] + upper[:-1]` to avoid duplicating the shared endpoints. The start point of the result is the lexicographically smallest point.
- `tests/test_convexhull.py`: one test case per acceptance example (square, interior point, edge-collinear point, triangle, all-collinear line, duplicate points, mixed polygon with interior point, single point, two points, empty, float coordinates) plus the validation cases (`"abc"` → `TypeError`, `(0, 0, 0)` → `ValueError`, `(0, "a")` → `TypeError`, `(0, True)` → `TypeError`) and a few extra coverage cases (tuple input, `<3` dedup/sort, non-list points, `None` coordinate, `False` coordinate).

## What I did not do

- Did not create or touch `porta.py`, `primorial.py`, `tests/test_porta.py`, `tests/test_primorial.py` (owned by other processes).
- Did not modify any pre-existing file (`roman.py`, `legacy_stringkit.py`, `README.md`, existing tests, CI config, etc.).
- Did not commit or push anything.
- Did not add any dependency beyond the standard library; the only environment change was installing `pytest` (it was not present) so the required checks could run.

## Checks run and results

1. `python3 -m pytest tests/test_convexhull.py -q` → **17 passed** (exit 0).
2. `python3 -m pytest tests/ -q` → **28 passed** (exit 0), which is the 17 new convexhull tests plus the 11 pre-existing baseline tests (`tests/test_roman.py`, `tests/test_legacy_stringkit.py`).

## What the validator must pay attention to

- The `team/` paths written by this process are `team/handoffs/convexhull-monotone-chain.md` and `team/status/convexhull-monotone-chain.json`; nothing else under `team/` was written.
- Result ordering guarantee: hull vertices are returned counterclockwise starting at the lexicographically smallest point; for `k < 3` distinct points the return is `sorted(set(points))`, which for the two-point case means ascending order (e.g. `[(1, 2), (3, 4)]`), matching the acceptance example.
- Collinear handling: interior collinear points on an edge are dropped (`cross <= 0` pop), so a fully collinear input returns only its two extreme points.
- Type-rejection nuance: `bool` coordinates raise `TypeError` (not `ValueError`) and a non-2-tuple point raises `ValueError` (not `TypeError`); a non-list/tuple `points` argument (including `str`) raises `TypeError`.
- No cross-module imports: `convexhull.py` imports only `numbers.Number` from the standard library.
