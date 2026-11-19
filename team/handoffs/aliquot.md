# Handoff: aliquot (sub-issue #465)

## What was requested

Process card "aliquot" under work order #456 (Round 45, concurrent B card): implement
`aliquot.py` with three functions — `aliquot_sum(n: int) -> int`, `classify(n: int) -> str`,
and `aliquot_sequence(n: int, count: int) -> list[int]` — plus `tests/test_aliquot.py`
covering every acceptance point verbatim from the work order.

Validation rules (verbatim from the order):
- `aliquot_sum`: proper divisors only (excludes n, includes 1); n must be int >= 1,
  else `ValueError` for n<1 and `TypeError` for non-int (bool rejected).
- `classify`: "perfect" / "abundant" / "deficient" by comparing the aliquot sum to n.
- `aliquot_sequence`: starts at n, count terms; stops early if a term's aliquot sum
  is 0 (0 not included); count must be int >= 1, else `ValueError` for count<1 and
  `TypeError` for non-int.

## What I did

- Created `aliquot.py` (standard library only, no imports of other modules).
  - Input validation centralized in a `_check_int` helper that rejects `bool` via
    `isinstance(value, bool)` before the `isinstance(value, int)` check, then enforces >= 1.
  - `aliquot_sum` uses trial division up to `sqrt(n)`, summing divisor pairs
    (`i` and `n // i`) with a duplicate guard for perfect squares. `n == 1` returns 0.
  - `classify` and `aliquot_sequence` validate their arguments (count also >= 1)
    and build on `aliquot_sum`. The sequence loop appends the next term only when
    it is nonzero, so a zero sum ends the sequence without being included.
- Created `tests/test_aliquot.py` with one test function per acceptance group:
  known aliquot sums, classification, sequences, early stop at 1, ValueError cases,
  TypeError cases (6.0, True), and bad `count` cases (0, 2.5). Every acceptance
  point in the card has a corresponding assertion.

## What I did not do

- Did not touch `bstree.py`, `massconv.py`, `roman.py`, `legacy_stringkit.py`,
  or any existing test file; did not commit or push.
- Did not implement the other two process cards (they belong to other workers).
- Created only `aliquot.py`, `tests/test_aliquot.py`, plus the two required team
  files (`team/handoffs/aliquot.md`, `team/status/aliquot.json`).

## Checks run and results

1. `python3 -m pytest tests/test_aliquot.py -q` → **7 passed** (exit 0)
2. `python3 -m pytest tests/ -q` → **18 passed** (exit 0)

Note: pytest was not preinstalled in this environment; installed `pytest 9.2.0`
via pip before running the checks. No other dependencies were added.

## Things the validator must pay attention to

- `bool` rejection: `isinstance(True, int)` is True in Python, so the helper checks
  `isinstance(value, bool)` first — `aliquot_sum(True)` raises `TypeError`, not `ValueError`.
- `aliquot_sequence(1, 3) == [1]`: the early-stop rule fires because `aliquot_sum(1) == 0`,
  so the sequence ends after one term and never contains 0.
- The `aliquot_sum` pair-summing loop skips the `other == i` duplicate for perfect
  squares (e.g. 496), which is what makes `aliquot_sum(496) == 496` exact.
- All three functions validate arguments themselves; `classify` and `aliquot_sequence`
  do not rely on the caller to pre-validate.
