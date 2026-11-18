# Handoff: totient-module (sub-issue #413)

## What was requested

Process card `totient-module` under work order #409 (第四十三轮 · C 单). Create exactly two new files:

- `totient.py` — implement `totient(n: int) -> int` returning Euler's totient φ(n); raise `ValueError` for `n < 1`; standard library only.
- `tests/test_totient.py` — a test case for every acceptance example: `totient(1) == 1`, `totient(9) == 6`, `totient(12) == 4`, `totient(97) == 96`, `totient(100) == 40`, `totient(1_000_000) == 400000`, `totient(0)` raises `ValueError`, `totient(-5)` raises `ValueError`.

Constraints: new files only, no modification of any existing file, no cross-imports with `catalan`/`factorize`.

## What I did

- Implemented `totient(n)` in `totient.py` via trial division: start with `result = n`, divide out each prime factor `p` and apply `result -= result // p` (standard product formula φ(n) = n ∏(1 − 1/p)). Handles `n = 1` (returns 1, loop never applies a factor) and the large input `1_000_000` efficiently (trial division up to √n, i.e. ≤ 1000).
- Wrote `tests/test_totient.py` with 8 tests, one per acceptance example, following the existing `tests/test_roman.py` style (`pytest.raises(ValueError)` for the error cases).

## What I did not do

- Did not touch `catalan.py`, `factorize.py`, or any other process's files.
- Did not modify any pre-existing repository file (`roman.py`, `legacy_stringkit.py`, existing tests, README, CI configs).
- Did not commit or push.
- Did not implement `catalan` or `factorize` (owned by sibling process cards).

## Checks run and results

Note: `pytest` was not installed in the environment; I installed it with `python3 -m pip install --user pytest` (pytest 9.2.0) to run the required checks. This only affects the local user site-packages, no repository file was changed.

1. `python3 -m pytest tests/test_totient.py -q` → `8 passed in 0.01s`
2. `python3 -m pytest tests/ -q` → `19 passed in 0.03s` (full suite: `test_roman.py` + `test_totient.py`)

## What the validator must pay attention to

- All 8 acceptance points have a dedicated test; both required check commands pass with the full suite green.
- `totient(0)` and `totient(-5)` both raise `ValueError` (guard is `n < 1`, so `0` is rejected).
- `totient(1) == 1` is correct: the product formula yields 1 for the empty prime set.
- Sibling modules `catalan.py` and `factorize.py` are produced by other process cards; the merged full-suite result depends on all three landing together.
