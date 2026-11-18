# Handoff: factorial-module (sub-issue #390)

## What was requested
Process card for work order #382 (round 42 · concurrent unit C): own only the factorial module.
Create exactly two new files — `factorial.py` and `tests/test_factorial.py` — with:

- `factorial(n: int) -> int`: n! with `factorial(0) == 1`; negative n raises `ValueError`.
- `binom(n: int, k: int) -> int`: binomial coefficient C(n, k); must satisfy `0 <= k <= n`,
  otherwise raise `ValueError`.
- A corresponding test case for every acceptance point: `factorial(0) == 1`,
  `factorial(5) == 120`, `factorial(10) == 3628800`,
  `factorial(20) == 2432902008176640000`, `binom(5, 2) == 10`, `binom(10, 3) == 120`,
  `binom(10, 0) == 1`, `binom(7, 7) == 1`, and `ValueError` for `factorial(-1)`,
  `binom(5, 6)`, `binom(-1, 0)`.
- Standard library only; must not import `fib` or `sieve` (the three modules are independent).
- New files only; no existing file may be modified.

## What I did
- Created `factorial.py` with `factorial` (iterative product) and `binom` (multiplicative
  C(n,k) accumulation with `k = min(k, n - k)` for symmetry, exact integer arithmetic via
  `// i` at each step, which is exact because the running product stays divisible by i).
  Guards: `factorial` raises `ValueError` for n < 0; `binom` raises `ValueError` unless
  `0 <= k <= n`. No imports from `fib`/`sieve`; no third-party code.
- Created `tests/test_factorial.py` with 11 tests, one per acceptance point (5 for
  `factorial`, 6 for `binom`, including the three `ValueError` cases via
  `pytest.raises(ValueError)`).
- Wrote this handoff and `team/status/factorial-module.json`.

## What I did NOT do
- Did not create or touch `fib.py`, `sieve.py`, `tests/test_fib.py`, `tests/test_sieve.py`
  (owned by other process cards).
- Did not modify any existing file (`roman.py`, `legacy_stringkit.py`, README, existing
  tests, workflows, or anything else).
- Did not commit or push (left to the workflow).

## Checks run and results
Environment note: the base interpreter had no pytest, so I installed `pytest` 9.2.0
user-level (`python3 -m pip install --user pytest`) to run the mandated checks. This is an
environment setup step, not a repository change.

1. `python3 -m pytest tests/test_factorial.py -q` → **11 passed in 0.01s** (exit 0)
2. `python3 -m pytest tests/ -q` → **22 passed in 0.02s** (exit 0; 11 mine + 11 pre-existing)

## What the validator must pay attention to
- Only two source files were added: `factorial.py` and `tests/test_factorial.py`
  (plus the two required team/ files). `git status` should show no modifications to
  tracked files.
- All 11 acceptance points are covered by named tests in `tests/test_factorial.py`;
  the full suite (22 tests) passes.
- `binom` uses exact integer arithmetic (no floating point); `binom(-1, 0)` raises
  `ValueError` because the `0 <= k <= n` check compares k > n first (k=0 > n=-1).
- Cross-process note: full-suite greenness also depends on fib/sieve cards landing their
  own files; my changes cannot affect them.
