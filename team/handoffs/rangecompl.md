# Handoff: rangecompl (sub-issue #296, card "rangecompl")

## What was requested
Implement `rangecompl.complement(ranges: list[tuple[int, int]], lo: int, hi: int) -> list[tuple[int, int]]` in a new `rangecompl.py`, plus `tests/test_rangecompl.py`. Only new files; no edits to pre-existing files; standard library only; no imports of `baseconv` or `hmsconv`.

Behavior required:
- `ranges` is a list of closed integer intervals (may overlap, unordered, endpoints any integers).
- Return closed intervals inside `[lo, hi]` not covered by any input interval, sorted ascending by start, non-overlapping and non-adjacent (adjacent gaps merged — any two output intervals separated by at least one covered point).
- Raise `ValueError` if `lo > hi`.
- Raise `ValueError` if any interval has `start > end`.

## What I did
- Created `rangecompl.py` with `complement()`:
  - Validates `lo > hi` and `start > end` first (raises `ValueError`).
  - Clamps each interval to `[lo, hi]` (so intervals extending outside the window, e.g. `(-5, 1)` with `[0, 3]`, are handled), sorts, then sweeps with a cursor to emit uncovered gaps. Merging happens implicitly via the cursor (`cursor = max(cursor, e + 1)`), so overlapping/adjacent coverage is merged and output intervals are never adjacent.
- Created `tests/test_rangecompl.py` with 13 tests, including every acceptance criterion verbatim:
  - `complement([(2, 3), (5, 5)], 0, 7) == [(0, 1), (4, 4), (6, 7)]`
  - `complement([], 1, 3) == [(1, 3)]`
  - `complement([(0, 10)], 0, 7) == []`
  - `complement([(3, 4), (1, 2)], 0, 5) == [(0, 0), (5, 5)]`
  - `complement([(-5, 1)], 0, 3) == [(2, 3)]`
  - `complement([(5, 2)], 0, 7)` raises `ValueError`
  - Plus: `lo > hi` raises, overlapping ranges merged, single-point window, empty result edge, ranges entirely outside window, point gap between covered blocks, negative window.

## What I did not do
- Did not create or modify `baseconv.py`, `hmsconv.py`, or their tests (owned by other cards).
- Did not modify any pre-existing file (including `legacy_stringkit.py`, `roman.py`, `README.md`, existing tests).
- Did not commit or push.
- No non-standard-library imports; `rangecompl.py` does not import the sibling modules.

## Checks run and results
- `python3 -m pytest tests/test_rangecompl.py -q` → `13 passed`
- `python3 -m pytest tests/ -q` → `24 passed`

(Note: `pytest` was not installed in the environment initially; I installed it with `python3 -m pip install pytest` to run the checks. No repository files were changed by that.)

## For the validator
- Acceptance cases are covered one-for-one; if a hidden acceptance test differs on a detail, check the non-adjacency rule: output intervals must never be consecutive (e.g. `(0,0)` and `(1,1)` must merge into `(0,1)` when both are gaps — but a gap of one point between two covered points, e.g. `[(0,0),(2,2)]` over `[0,3]`, correctly yields `[(1,1),(3,3)]`).
- Input validation order: `lo > hi` and bad intervals both raise `ValueError` before any computation.
- Intervals are clamped to `[lo, hi]`, so inputs extending outside the window are accepted (per spec).
