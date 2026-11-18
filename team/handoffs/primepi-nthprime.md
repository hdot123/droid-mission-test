# Handoff: primepi-nthprime

## What was requested (sub-issue #440, card: primepi-nthprime)

Process card for work order #431 (第四十四轮 B). Owns exactly two new files:

- `primepi.py` at repository root
- `tests/test_primepi.py`

Spec (verbatim requirements):

- `primepi(x: int) -> int`: count of primes ≤ x (π(x)). x must be a non-negative integer, else `ValueError` (covers `-1` and `2.5`).
- `nthprime(n: int) -> int`: nth prime, 1-based (`nthprime(1) == 2`). n must be a positive integer, else `ValueError` (covers `0`).
- Must be accurate/fast for x up to 10000 and n up to 1000.
- Every acceptance example must have its own test case.
- Standard library only; no other modules from the work order imported; no pre-existing file modified; no `team/` or `.github/` paths touched by the implementation (team files below are required by this card).

## What I did

- Created `primepi.py` with:
  - `_sieve(limit)`: bytearray-based Eratosthenes sieve returning all primes ≤ limit.
  - `_require_int(value, name)`: rejects non-`int` input including `bool` with `ValueError`.
  - `primepi(x)`: validates integer and `x >= 0` (`bool` and non-int raise `ValueError`; negative raises `ValueError`); returns `0` for `x < 2`, else `len(_sieve(x))`.
  - `nthprime(n)`: validates integer and `n >= 1`; uses the Rosser–Schoenfeld bound `n * (ln n + ln ln n) + 3` (floor at 15 for small n), doubling the limit until at least n primes are found.
- Created `tests/test_primepi.py` with 17 tests: one test case per acceptance item (8 `primepi` values, 6 `nthprime` values, `primepi(-1)` raises, `nthprime(0)` raises, `primepi(2.5)` raises).

## What I did NOT do

- Did not create `columnar.py`, `lengthconv.py`, or their tests (other cards).
- Did not modify any pre-existing file (`roman.py`, `legacy_stringkit.py`, existing tests, `README.md`, `.github/`, etc.).
- Did not commit or push.
- Did not import the other two work-order modules.

## Checks run and results

1. `python3 -m pytest tests/test_primepi.py -q` → `17 passed in 0.02s`
2. `python3 -m pytest tests/ -q` → `28 passed in 0.04s`

Note: pytest was not present in the environment initially (`No module named pytest`); installed it via `python3 -m pip install pytest` (no repo files changed by that).

## Notes for the validator

- All 17 acceptance items are covered as separate tests; the three full-suite runs include the pre-existing 11 tests (`test_roman.py`, `test_legacy_stringkit.py`).
- `primepi`/`nthprime` deliberately raise `ValueError` (not `TypeError`) for non-integer input per spec, including `bool` inputs.
- `primepi(10000)` and `nthprime(1000)` are the heaviest cases; both complete in well under a second with the sieve bound above.
