# Handoff: tempconv-six-functions (sub-issue #363)

## What was requested
Implement the temperature conversion component of work order #347 (round 40, concurrent D):
- New file `tempconv.py` with exactly six functions: `c_to_f`, `f_to_c`, `c_to_k`, `k_to_c`, `f_to_k`, `k_to_f`. Each takes a numeric value in its source unit and returns the conversion result rounded to two decimals (`round(x, 2)`).
- New file `tests/test_tempconv.py` with a test case for every acceptance item, verbatim:
  `c_to_f(0) == 32.0`, `c_to_f(100) == 212.0`, `c_to_f(-40) == -40.0`, `c_to_f(37) == 98.6`,
  `f_to_c(212) == 100.0`, `f_to_c(32) == 0.0`, `c_to_k(0) == 273.15`, `k_to_c(0) == -273.15`,
  `k_to_c(273.15) == 0.0`, `f_to_k(32) == 273.15`, `k_to_f(0) == -459.67`.
- Constraints: new files only, no modification of any existing file, standard library only, no imports from other project modules.

## What I did
- Created `tempconv.py` (new file) implementing the six conversions with `round(x, 2)` on every return:
  - `c_to_f`: `c * 9/5 + 32`; `f_to_c`: `(f - 32) * 5/9`
  - `c_to_k`: `c + 273.15`; `k_to_c`: `k - 273.15`
  - `f_to_k`: `(f - 32) * 5/9 + 273.15`; `k_to_f`: `(k - 273.15) * 9/5 + 32`
- Created `tests/test_tempconv.py` (new file) with one test function per acceptance item (11 tests), all using the exact literal expectations from the work order.
- Wrote this handoff and `team/status/tempconv-six-functions.json`.

## What I did NOT do
- Did not touch `isbn13.py`, `baseconv.py`, `tests/test_isbn13.py`, `tests/test_baseconv.py`, or any other process's files.
- Did not modify any pre-existing file (`roman.py`, `legacy_stringkit.py`, existing tests, README, etc.).
- Did not add extra public functions beyond the six required.
- Did not commit or push anything.

## Checks ran and results
The environment had no `pytest` installed (`python3 -m pytest` failed with "No module named pytest"), so I installed it with `python3 -m pip install --quiet pytest` (pytest 9.2.0). Then:

1. `python3 -m pytest tests/test_tempconv.py -q` → `11 passed in 0.02s` (exit 0)
2. `python3 -m pytest tests/ -q` → `22 passed in 0.02s` (exit 0) — the full suite at the time this process ran (tempconv's 11 plus the 11 pre-existing roman/legacy_stringkit tests).

## Notes for the validator
- Rounding is applied on every return value as `round(x, 2)`; floating-point results such as `c_to_f(37) == 98.6` and `k_to_f(0) == -459.67` hold exactly under the given formulas.
- Acceptance items are covered 1:1 by test functions; `tests/test_tempconv.py` should pass standalone and as part of the full suite.
- Note that the full-suite count (22) reflects the repo state when I ran it; if other processes land their own tests before merge, the total will grow but `tests/test_tempconv.py` remains 11 passing tests.
- No existing files were modified by this process (only the two owned files plus the two team files were created).
