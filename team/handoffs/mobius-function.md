# Handoff: mobius-function (sub-issue #648)

## What was requested

Implement process card #648 of work order #630 (round 47, concurrent batch A):

- Create new file `mobius.py` (standard library only) with `mobius(n: int) -> int`:
  - `n` must be a positive `int`; `bool` is rejected.
  - If `n` has a squared prime factor, return `0`.
  - Otherwise let `k` be the number of distinct prime factors of `n` and return `(-1)^k`.
  - By convention `mobius(1) == 1`.
  - `n < 1` raises `ValueError`; non-`int` raises `TypeError`.
- Create new file `tests/test_mobius.py` with a test case for each acceptance criterion.
- Do not modify any pre-existing file; no cross-module imports; own only `mobius.py`, `tests/test_mobius.py`, and the two team files.
- Run checks: `python3 -m pytest tests/test_mobius.py -q` and `python3 -m pytest tests/ -q`.

## What I did

- Added `mobius.py`:
  - Type gate: `isinstance(n, bool)` or non-`int` raises `TypeError` (rejects `2.5`, `"6"`, `True`).
  - Range gate: `n < 1` raises `ValueError` (rejects `0`, `-6`).
  - Trial division by 2 then odd divisors only; on a first divisor `d`, `n //= d` and a second divisibility by `d` means `d^2 | n` → return `0`; otherwise count `k` distinct primes (including any remaining factor `> 1`).
  - Return `-1` if `k` is odd, `1` if `k` is even (`mobius(1)` → `k = 0` → `1`).
- Added `tests/test_mobius.py` with one test function per acceptance group (18 value assertions plus `ValueError`/`TypeError` cases; `mobius(1)` has its own test).
- Installed `pytest` via `python3 -m pip install` (it was absent from the environment; `requirements-dev.txt` lists `pytest>=7.4.0`).

## What I did not do

- Did not touch `trifid.py`, `gasmark.py`, or any pre-existing file (`roman.py`, `legacy_stringkit.py`, existing tests, docs, etc.).
- Did not add cross-module imports; `mobius.py` uses only the standard library.
- Did not commit or push.

## Checks run and results

- `python3 -m pytest tests/test_mobius.py -q` → `6 passed in 0.01s`
- `python3 -m pytest tests/ -q` → `35 passed in 1.92s`

Both process checks pass.

## Notes for the validator

- Full-suite count includes the new 6 tests (29 pre-existing + 6 new = 35).
- All 18 numeric acceptance values, both `ValueError` cases, and all three `TypeError` cases are asserted in `tests/test_mobius.py`.
- `bool` rejection is tested explicitly (`mobius(True)` → `TypeError`); note `isinstance(True, int)` is `True` in Python, so the `bool` check must come before the `int` check (it does).
- `tests/test_mobius.py` imports `from mobius import mobius`, relying on the repo's existing root-on-path test setup (same pattern as `tests/test_roman.py`).
