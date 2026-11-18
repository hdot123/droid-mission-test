# Handoff: catalan-module (sub-issue #412)

## What was requested

Process card `catalan-module` under work order #409 (第四十三轮 · C 单):

- Create `catalan.py` with `catalan(n: int) -> int` returning the n-th Catalan number C_n (C_0 = 1), raising `ValueError` for negative n.
- Create `tests/test_catalan.py` with a corresponding test case for every acceptance example: `catalan(0) == 1`, `catalan(1) == 1`, `catalan(2) == 2`, `catalan(3) == 5`, `catalan(4) == 14`, `catalan(5) == 42`, `catalan(10) == 16796`, `catalan(15) == 9694845`, `catalan(-1)` raises `ValueError`.
- New files only; standard library only; no cross-imports; do not touch totient, factorize, or any existing file.

## What I did

- Implemented `catalan(n)` in `catalan.py` using `math.comb(2n, n) // (n + 1)` (standard library), with a `ValueError` guard for `n < 0`.
- Added `tests/test_catalan.py` with a parametrized test covering all eight numeric acceptance values and a separate test asserting `catalan(-1)` raises `ValueError`.

## What I did not do

- Did not create or modify `totient.py`, `factorize.py`, or their tests (other process cards own those).
- Did not modify any pre-existing file (`roman.py`, `legacy_stringkit.py`, tests, README, etc.).
- Did not commit or push.

## Checks run and results

- `python3 -m pytest tests/test_catalan.py -q` → 9 passed
- `python3 -m pytest tests/ -q` → 20 passed (includes pre-existing roman/legacy_stringkit tests, all green)

Note: pytest was not present in the environment; it was installed via `python3 -m pip install pytest` (pytest 9.2.0) so the mandated checks could run. This does not change any repository file.

## Notes for the validator

- `catalan` is exact-integer arithmetic; `math.comb` requires Python 3.8+ (environment runs 3.14).
- Each acceptance example maps to an assertion in `tests/test_catalan.py`; `catalan(-1)` coverage is in `test_catalan_negative_raises`.
- Only `catalan.py` and `tests/test_catalan.py` were added by this card.
