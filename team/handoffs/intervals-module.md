# Handoff: intervals-module (sub-issue #253)

## What was requested
Process card `intervals-module` under work order #247 (round 33, group C):
- Implement `intervals.py` with `merge(intervals)` and `total_length(intervals)` per spec:
  - intervals given as `[start, end]` (list or tuple), `start <= end`;
  - sort by start ascending (ties by end ascending), then merge when next `start <= current merged end`;
  - return non-overlapping ascending list of `[start, end]` lists;
  - any `start > end` raises `ValueError`; empty input returns `[]`;
  - `total_length` sums `end - start` over the merged intervals.
- Provide `tests/test_intervals.py` covering all required examples plus the ValueError case.
- Scope limits: only `intervals.py` and `tests/test_intervals.py`; standard library only; no cross-module imports; no package directory; no CLI.

## What I did
- Created `intervals.py` (root): `_validate` helper raises `ValueError` on malformed/inverted intervals; `merge` validates all inputs first (so a bad interval anywhere raises even if sorting would place it late), sorts by `(start, end)`, merges on `start <= current end` keeping the max end, returns `[]` for empty input; `total_length` sums `end - start` over `merge(...)` output.
- Created `tests/test_intervals.py` (13 tests) covering every required example:
  - `merge([[1, 3], [2, 6], [8, 10], [15, 18]]) -> [[1, 6], [8, 10], [15, 18]]`
  - `total_length(...) -> 10`
  - `merge([[1, 3], [3, 5]]) -> [[1, 5]]` (endpoint sharing)
  - `merge([[1, 3], [4, 5]]) -> [[1, 3], [4, 5]]` (disjoint)
  - `merge([[8, 10], [1, 3], [2, 6]]) -> [[1, 6], [8, 10]]` (unsorted input)
  - `merge([]) -> []`
  - plus tuple inputs, tie-on-start ordering, contained-interval absorption, empty/disjoint `total_length`, and `ValueError` for `start > end` in both `merge` and `total_length`.

## What I did NOT do
- Did not touch `weekday.py`, `monthshift.py`, their tests, `roman.py`, `legacy_stringkit.py`, `tests/test_roman.py`, or any other file.
- Did not create a package directory, CLI, `__init__.py`, or any cross-module import.
- Did not commit or push (per instructions).
- Not in my scope: the other two deliverables of work order #247 (their modules/tests are owned by other processes).

## Checks run and results
- `python -m pytest -q tests/test_intervals.py` → **13 passed in 0.02s** (exit 0).
  - Note: pytest was not installed in the environment; I installed it via `python3 -m pip install pytest` (pytest 9.2.0) to run the mandated check. No repo files were changed by that install.

## What the validator must pay attention to
- The mandated check command is exactly `python -m pytest -q tests/test_intervals.py`; it passes with 13 tests.
- The work-order-level gate (`python -m pytest -q tests/test_weekday.py`, `tests/test_monthshift.py`, and full suite) depends on the other two processes' deliverables landing; I did not run or affect those.
- Behavior notes worth verifying against spec: validation of all intervals happens before merging (any inverted interval raises `ValueError` regardless of position); output elements are always fresh `[start, end]` lists (input lists/tuples are not mutated); merged output for empty input is `[]`.
