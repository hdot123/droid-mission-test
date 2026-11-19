# Handoff: century (sub-issue #497)

## What was requested

Work order #481, module 三 (century): add `century.py` and `tests/test_century.py` implementing three helpers for the 46th round deliverable:

- `century(year: int) -> int` — century a year belongs to: years 1–100 are the 1st century, 101–200 the 2nd, i.e. `(year - 1) // 100 + 1`.
- `century_range(year: int) -> tuple[int, int]` — inclusive start/end years of that century (21st → `(2001, 2100)`).
- `millennium(year: int) -> int` — millennium a year belongs to: years 1–1000 are the 1st, i.e. `(year - 1) // 1000 + 1`.

Shared validation for all three: `year` must be an `int`; `bool` (True/False) is rejected as `TypeError`; non-int raises `TypeError`; `year < 1` raises `ValueError`.

Constraints: only add `century.py` and `tests/test_century.py`; no edits to existing files; standard library only; no imports from other deliverables; every acceptance point must have a corresponding test case.

## What I did

- Created `century.py` with a private `_validate_year(year)` helper implementing the shared rules (bool rejected first via `isinstance(year, bool)`, then non-int `TypeError`, then `< 1` `ValueError`), and the three public functions delegating to it.
- Created `tests/test_century.py` with 22 test functions, one per acceptance point listed in the work order (7 century value checks, 3 century_range checks, 5 millennium checks, 4 ValueError cases, 3 TypeError cases), using `pytest.raises`.

## What I did not do

- Did not touch `pressureconv.py`, `ringbuffer.py`, or any other existing file (including `roman.py`, `legacy_stringkit.py`, and existing tests).
- Did not import from any other deliverable; `century.py` uses only the standard library (no imports at all).
- Did not commit or push anything.
- Did not modify the work order or acceptance criteria.

## Checks run and results

The environment had no pytest installed (`python3 -m pytest` → "No module named pytest"), so I installed pytest 9.2.0 with `pip3 install pytest` in order to run the mandated checks. No repository files were affected by the install.

- `python3 -m pytest tests/test_century.py -q` → **22 passed in 0.03s**
- `python3 -m pytest tests/ -q` → **33 passed in 0.04s** (my 22 + 11 pre-existing baseline tests)

## Notes for the validator

- Ordering of validation matters for one spec point: `century(True)` must raise `TypeError`, not be treated as `1`. The bool check runs before the `< 1` range check, so this holds.
- `century_range` derives its result from `century`, so it inherits identical validation; `century_range(0)` raises `ValueError` (via `century`) as required.
- Only two files were added by this process: `century.py`, `tests/test_century.py`. The `team/` handoff/status files were required by the workflow instructions.
