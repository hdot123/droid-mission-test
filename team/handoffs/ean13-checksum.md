# Handoff: ean13-checksum (sub-issue #182)

## What was requested
Process card `ean13-checksum` under work order #157 (round 26 A, foreman v2.6.5):
- Create `ean13.py` in the repo root with exactly two public functions:
  - `check_digit(first12)` — takes a 12-digit numeric string, returns the EAN-13
    check digit as an `int`. Odd positions (1-based from the left) weigh 1,
    even positions weigh 3; weighted sum's last digit is subtracted from 10,
    and a result of 10 becomes 0. Non-12-pure-digit input raises `ValueError`.
  - `is_valid(code)` — returns whether a 13-digit string has a correct check
    digit; wrong format returns `False` without raising.
  - Required examples: `check_digit("400638133393") == 1`,
    `is_valid("4006381333931") is True`, `is_valid("4006381333932") is False`.
- Create `tests/test_ean13.py` covering only this module: the three examples,
  `ValueError` on invalid `check_digit` inputs, `is_valid` returning `False`
  for malformed codes without raising, and odd/even weighting.
- Constraints: Python stdlib only; no import of `vigenere.py` or
  `temperature.py`; no package directory; no CLI.

## What I did
- Created `ean13.py` with `check_digit` and `is_valid` as specified.
  - `check_digit` validates `isinstance(str)`, `len == 12`, and `str.isdigit()`
    (rejects non-str, wrong length, non-digits, whitespace), then computes
    `result = (10 - (total % 10)) % 10`, which handles the "10 -> 0" rule.
  - `is_valid` returns `False` for anything that is not 13 pure digits
    (including non-str input), otherwise compares `check_digit(code[:12])`
    to `int(code[12])`.
- Created `tests/test_ean13.py` (19 tests): the three required examples,
  parametrized `ValueError` cases for `check_digit` (empty, 11/13 digits,
  non-digit, trailing space, int, None), parametrized `False`-without-raise
  cases for `is_valid`, an odd/even weighting test asserting a +1 change at an
  odd position shifts the weighted sum by 1 while at an even position by 3
  (and that the two resulting check digits differ), and a round-trip test.

## What I did NOT do
- Did not touch `vigenere.py`, `temperature.py`, or any other module's tests.
- Did not touch `team/` paths other than the two files assigned to me
  (`team/handoffs/ean13-checksum.md`, `team/status/ean13-checksum.json`).
- Did not touch `.github/` or any other path.
- Did not create a package directory, CLI, or any non-stdlib import.
- Did not commit or push.

## Checks run and results
Executed verbatim from the card's checks column, from the repo root:

1. `python -m pytest -q tests/test_ean13.py`
   → exit 0, `19 passed in 0.02s`
2. `python -m pytest -q`
   → exit 0, `19 passed in 0.01s`

Note on environment: pytest was not installed in this runner
(`/usr/bin/python: No module named pytest`). I installed it with
`python -m pip install --quiet pytest` (pytest 9.2.0) so the acceptance
command could run. This was an environment prerequisite only; no repository
file was changed for it.

## Notes for the validator
- The two check commands above are the card's checks, run verbatim; both pass.
- Full-suite pass currently reflects only this module's tests (sibling modules
  `vigenere.py` / `temperature.py` are owned by other processes and may not
  exist yet); the suite will grow as sibling cards land.
- Behavior matches the spec exactly, including the `int` return type of
  `check_digit`, the `ValueError` contract, and `is_valid` never raising.
