# Handoff: collatz-sequence (sub-issue #309)

## What was requested
Process card "collatz-sequence" under work order #305 (第三十七轮 · 常规组二), scoped to exactly two new files:

- `collatz.py` with `steps(n: int) -> int` (Collatz rule: even → n/2, odd → 3n+1; `steps(1) == 0`; `n < 1` raises `ValueError`) and `peak(n: int) -> int` (max value of the sequence including start and ending 1; `n < 1` raises `ValueError`).
- `tests/test_collatz.py` with one test case per acceptance item, verbatim: `steps(1) == 0`, `steps(6) == 8`, `steps(27) == 111`, `peak(27) == 9232`, `peak(1) == 1`, `steps(0)` raises `ValueError`, `peak(-3)` raises `ValueError`.
- Standard library only; no imports of other deliverable modules (morse/levenshtein).

## What I did
- Created `collatz.py` (new file): `steps` and `peak` implemented with simple iteration; both validate `n < 1` and raise `ValueError`. No imports at all.
- Created `tests/test_collatz.py` (new file): 7 test functions, one per acceptance item above, using `pytest.raises` for the two error cases. Imports only `pytest` and `collatz`.
- Ran both mandated checks (see below).

## What I did not do
- Did not modify any existing file (roman.py, legacy_stringkit.py, tests/test_roman.py, tests/test_legacy_stringkit.py, README.md, worker-* files all untouched).
- Did not create or touch `morse.py`, `levenshtein.py`, or their tests (owned by other process cards).
- Did not commit or push.

## Checks run and results
1. `python3 -m pytest tests/test_collatz.py -q` → `7 passed in 0.01s`
2. `python3 -m pytest tests/ -q` → `18 passed in 0.03s`

Note: pytest was not present in the environment initially; I installed it with `python3 -m pip install --user --break-system-packages pytest` (pytest 9.2.0) so the checks could run. This does not modify repository files.

## For the validator
- Full-suite count 18 = 7 (collatz) + 7 (roman) + 4 (legacy_stringkit); the other two modules' tests will add more when merged.
- Both functions are O(steps) and use only integer arithmetic; `steps` and `peak` share the same validation rule (`n < 1` → `ValueError`).
- Only standard library (actually: zero imports in `collatz.py`); no cross-imports of deliverables.
