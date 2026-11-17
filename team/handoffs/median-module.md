# Handoff: median-module (sub-issue #22)

## What was requested
Process card `median-module` for work order #18: create `median.py` at the repository root exposing `median(nums)` with the lower-median rule (sort ascending; odd count -> middle element; even count -> smaller of the two middle values, never averaged; empty list -> `ValueError`), plus `tests/test_median.py` covering the three spec examples, another even-length lower-middle (not average) case, unsorted input, single-element, negatives, and `ValueError` on empty input. Standard library only; no imports of other project modules; no package directory; no CLI. Only `median.py` and `tests/test_median.py` owned.

## What I did
- Created `median.py` with a single function `median(nums)` (module docstring + function docstring; `sorted` + middle-index logic; `ValueError("median() arg is an empty sequence")` on empty input).
- Created `tests/test_median.py` with 7 tests using `pytest.raises`:
  - `median([1, 2, 3, 4]) == 2` (spec example)
  - `median([5, 1, 9]) == 5` (spec example, unsorted)
  - `median([7]) == 7` (spec example, single element)
  - `median([10, 2, 8, 4]) == 4` (even length; average would be 6, proves lower-middle)
  - `median([3, 1, 2]) == 2` (unsorted odd length)
  - `median([-5, -1, -3]) == -3` and `median([-4, -3, -2, -1]) == -3` (negatives, odd + even)
  - `median([])` raises `ValueError`

## What I did NOT do
- Did not create or touch `roman.py`, `csvline.py`, or their tests (owned by other processes).
- Did not create package directories, CLI entry points, or `__init__.py`.
- Did not import any other project module; `median.py` imports nothing; only `pytest` used in the test file.
- Did not commit or push.

## Checks run
- `python -m pytest -q tests/test_median.py` → **7 passed in 0.02s** (exit 0).
- Note: the environment initially had no `pytest` module (`python -m pytest` failed with "No module named pytest"); I installed it with `pip install pytest` (pytest 9.2.0) so the check could run. Full-suite `python -m pytest -q` was not run here since sibling files are owned by other processes; only this process's check was executed as instructed.

## What the validator must pay attention to
- Even-length rule is deliberately **lower-middle, not average** — `median([1,2,3,4]) == 2` and `median([10,2,8,4]) == 4` (not 2.5 / 6).
- `median([])` raises `ValueError` (message: "median() arg is an empty sequence").
- Signature is exactly `median(nums)`; returns the element value (no copy of the input list is mutated — `sorted` returns a new list).
- Files owned by this card: `median.py`, `tests/test_median.py`, `team/handoffs/median-module.md`, `team/status/median-module.json`.
