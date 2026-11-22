# Handoff: factorize-module (sub-issue #414)

## What was requested

Process card `factorize-module` under work order #409 (第四十三轮 · 并发 C 单):

- Create **only** two new files: `factorize.py` and `tests/test_factorize.py`.
- Implement `prime_factors(n: int) -> list[int]`: prime factors of `n` in ascending order with multiplicity (repeats included); raise `ValueError` for `n < 2`.
- Implement `factor_count(n: int) -> int`: number of prime factors with multiplicity, exactly `len(prime_factors(n))`; raise `ValueError` for `n < 2`.
- Standard library only; no imports of catalan/totient or other repo modules.
- Every acceptance example must have a corresponding test case:
  - `prime_factors(2) == [2]`
  - `prime_factors(12) == [2, 2, 3]`
  - `prime_factors(97) == [97]`
  - `prime_factors(360) == [2, 2, 2, 3, 3, 5]`
  - `factor_count(12) == 3`
  - `factor_count(97) == 1`
  - `factor_count(360) == 6`
  - `prime_factors(1)` raises `ValueError`
  - `prime_factors(-10)` raises `ValueError`
- Checks (verbatim): `python3 -m pytest tests/test_factorize.py -q`, `python3 -m pytest tests/ -q`.
- Do not commit or push; do not modify files owned by other processes.

## What I did

- Created `factorize.py` with:
  - `prime_factors(n)`: validates `n < 2` → `ValueError`; trial-division from divisor 2 upward while `divisor * divisor <= rest`, appending each factor on every exact division (preserves multiplicity and ascending order), then appends the leftover prime `> 1`. No external imports.
  - `factor_count(n)`: returns `len(prime_factors(n))`, so it inherits the same `ValueError` for `n < 2` by construction (spec requires it be exactly that).
- Created `tests/test_factorize.py` with one test per acceptance example (9 required cases covered) plus two consistency tests: `factor_count(n) == len(prime_factors(n))` for valid inputs, and `factor_count` raising `ValueError` for `0, -1, 1`.

## What I did NOT do

- Did not create or touch `catalan.py`, `totient.py`, `tests/test_catalan.py`, `tests/test_totient.py` (owned by other process cards).
- Did not modify any existing file (README.md, roman.py, legacy_stringkit.py, tests/test_roman.py, tests/test_legacy_stringkit.py, worker-prompt.txt, worker-stream.jsonl all untouched).
- Did not commit or push anything.
- Did not add any dependency beyond the standard library (`pytest` used only as the test runner; it was already the repo's check command).

## Checks I ran and results

Environment note: `pytest` was not installed initially (`No module named pytest`); I installed it with `python3 -m pip install --user pytest` (pytest 9.2.0) purely to run the mandated checks. No repo files were changed by this.

1. `python3 -m pytest tests/test_factorize.py -q` → **11 passed in 0.02s** (exit 0)
2. `python3 -m pytest tests/ -q` → **22 passed in 0.03s** (exit 0) — my 11 tests plus the 11 pre-existing baseline tests.

## What the validator must pay attention to

- All 9 mandated acceptance examples have dedicated test functions in `tests/test_factorize.py`; plus `factor_count` invalid-input tests (spec implies it via delegation to `prime_factors`, I made it explicit).
- `factor_count` is implemented as `len(prime_factors(n))`, matching the spec's "exactly len(prime_factors(n))" wording.
- The full-suite count (22) reflects concurrent rounds: if catalan/totient cards land too, expect their tests to add to this number. My card's scope is only the two files above.
- Only standard library is used; no cross-imports between the three round-43 modules.
