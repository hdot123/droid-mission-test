# Handoff: sieve-module (sub-issue #388)

## What was requested
Work order #382, process card `sieve-module`: create `sieve.py` and `tests/test_sieve.py` (new files only, no modifications to existing files). Specs, verbatim:

- `primes_up_to(n: int) -> list[int]`: ascending list of all primes <= n; negative n raises ValueError; n < 2 returns empty list.
- `is_prime(n: int) -> bool`: whether n is prime; n < 2 returns False.

Acceptance points, each with a corresponding test case:
- `primes_up_to(10) == [2, 3, 5, 7]`
- `primes_up_to(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]`
- `primes_up_to(2) == [2]`
- `primes_up_to(1) == []`
- `is_prime(97) == True`
- `is_prime(100) == False`
- `is_prime(2) == True`
- `is_prime(1) == False`
- `is_prime(0) == False`
- `primes_up_to(-1)` raises ValueError

## What I did
- Created `sieve.py`: `primes_up_to` uses a bytearray Sieve of Eratosthenes (raises `ValueError` for negative input, returns `[]` for n < 2); `is_prime` uses trial division up to sqrt(n) (returns False for n < 2). Standard library only; no imports of `fib` or `factorial`.
- Created `tests/test_sieve.py`: one test case per acceptance point (plus extra edge cases `primes_up_to(0)` and `is_prime(-7)`).

## What I did not do
- Did not create or modify `fib.py`, `factorial.py`, their test files, or any other existing file.
- Did not commit or push (workflow handles that).

## Checks run and results
- `python3 -m pytest tests/test_sieve.py -q` — passed (12 passed, exit 0).
- `python3 -m pytest tests/ -q` — passed (23 passed, exit 0; full suite green).

## Notes for the validator
- All ten acceptance points are covered by named test methods in `tests/test_sieve.py`.
- The module is self-contained (standard library only, no cross-module imports), as required by the three-piece concurrency card.
