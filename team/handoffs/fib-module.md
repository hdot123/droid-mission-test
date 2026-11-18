# Handoff: fib-module (sub-issue #386)

## What was requested
Process card "fib-module": implement the Fibonacci module for work order #382 (round 42 C unit).

- `fib(n: int) -> int`: n-th Fibonacci number (fib(0)=0, fib(1)=1); negative n raises ValueError.
- `fib_list(n: int) -> list[int]`: first n Fibonacci numbers (fib_list(0) == []); negative n raises ValueError.
- Create only new files `fib.py` and `tests/test_fib.py`; do not modify any existing file; standard library only; no imports of sieve/factorial.
- Every acceptance point must have a corresponding test case.
- Checks: `python3 -m pytest tests/test_fib.py -q` and `python3 -m pytest tests/ -q`.

## What I did
- Created `fib.py` with iterative implementations of `fib` and `fib_list` (both raise ValueError on negative input).
- Created `tests/test_fib.py` with one test per acceptance point (11 tests total):
  - fib: 0, 1, 2, 10, 20, 50 values; fib(-1) raises ValueError.
  - fib_list: [0,1,1,2,3,5] for n=6, [0] for n=1, [] for n=0; fib_list(-1) raises ValueError.
- Wrote this handoff and `team/status/fib-module.json`.

## What I did not do
- Did not create or modify sieve.py, factorial.py, their tests, or any other existing file.
- Did not commit or push.
- Did not import any non-standard-library module, and fib.py does not import sieve or factorial.

## Checks and results
- `python3 -m pytest tests/test_fib.py -q` — passed (11 passed).
- `python3 -m pytest tests/ -q` — passed (full suite green at time of writing).

## Notes for the validator
- `fib` and `fib_list` use an iterative loop, so `fib(50)` is exact and fast; no recursion depth issues.
- Test file imports `pytest` for the ValueError cases; pytest is the project's test runner.
- All acceptance points from the work order are covered one-to-one by test functions in `tests/test_fib.py`.
