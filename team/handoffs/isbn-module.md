# Handoff: isbn-module (sub-issue #117)

## What was requested
Process card `isbn-module` for work order #113 (round 22A, foreman v2.6.4): implement the ISBN-10
validation module only.

- `isbn.py` in the repository root with exactly one function, `is_valid_isbn10(s)`:
  - ignore hyphens and spaces;
  - cleaned string must be 9 digits plus 1 check character (digit or `X`);
  - weighted sum `10*d1 + 9*d2 + ... + 1*d10` must be divisible by 11;
  - `X` allowed only in the last position, representing 10.
- `tests/test_isbn.py` covering this module's behavior only: valid ISBNs with/without hyphens
  and spaces, wrong check digits, wrong length, `X` anywhere except last position, correct
  trailing `X`, and empty/garbage input.
- Constraints: Python standard library only; no imports of `roman`/`piglatin`; no package
  directory; no CLI; test file tests only this module.

## What I did
- Created `isbn.py` with `is_valid_isbn10(s)`. Implementation: strips `-` and spaces; rejects
  non-`str` input, lengths other than 10, non-digit first 9 characters, and any non-digit
  check character other than a trailing `X`; computes the weighted sum with `X` = 10 in the
  last position; returns `total % 11 == 0`. Returns `False` (rather than raising) for invalid
  input, since the spec asks for a boolean validity predicate.
- Created `tests/test_isbn.py` with 8 test functions covering all required cases, including
  `080442957X` (valid trailing X), `X306406152` / `0X06406152` (X not last), `030640615X`
  (trailing X but wrong sum), wrong length, empty, and garbage input.
- Ran both card checks verbatim from the repository root (results below).

## What I did NOT do
- Did not touch `roman.py`, `piglatin.py`, their test files, or any other repository file.
- Did not create a package directory, CLI, or any non-standard-library dependency in the code.
- Did not commit or push (left to the workflow).
- Note: `pytest` was not present in the environment (`python -m pytest` failed with
  "No module named pytest"), so I installed it with `python3 -m pip install pytest`
  (pytest 9.2.0) to be able to run the mandated check commands. This changes only the
  environment, not repository files.

## Checks I ran and results
Both commands run verbatim from the repository root:

1. `python -m pytest -q tests/test_isbn.py`
   - Result: PASS — `........ [100%]` / `8 passed in 0.01s` (exit 0).
2. The card's `python - <<'PY' ... PY` assertion script (10 asserts on
   `is_valid_isbn10`).
   - Result: PASS — printed `isbn OK` (exit 0).

## What the validator must pay attention to
- Both checks must be run from the repository root; `isbn.py` sits at the root and is
  imported as a top-level module (no package).
- The full-suite gate `python -m pytest -q` belongs to the 汇总收口 step, not this card;
  this card only guarantees its own test file passes (it does).
- Behavior note: invalid input returns `False` instead of raising. The work order specifies
  `ValueError` only for `roman.py`; for ISBN the spec asks the function to "判断是否合法"
  (return validity), so a boolean predicate was implemented. If the foreman intended
  `ValueError` here too, that is the one interpretation point to confirm.
- Expected test count for this file: 8 tests, all passing.
