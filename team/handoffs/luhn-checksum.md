# Handoff: luhn-checksum (sub-issue #356)

## What was requested
Process card `luhn-checksum` for work order #344 (round 40 · batch A): own exactly two new files,
`luhn.py` and `tests/test_luhn.py`, implementing:

- `is_valid(number: str) -> bool` — non-empty pure-digit string or `ValueError`; Luhn algorithm
  (from the right, double every second digit, subtract 9 from products > 9, valid iff sum % 10 == 0).
- `check_digit(payload: str) -> int` — non-empty pure-digit string or `ValueError`; returns the
  single digit 0-9 that makes `payload + digit` pass Luhn validation.

Standard library only; no imports from other project modules. No other file touched; no commit/push.

## What I did
- Created `luhn.py` with a shared `_digits()` validator (rejects non-`str`, empty, and any
  character outside ASCII `0`-`9`; deliberately avoids `str.isdigit()` so Unicode digit characters
  such as `"１"` or `"²"` cannot slip through as "digits").
- `is_valid` sums right-to-left doubling positions 1,3,5,... (0-based from the right).
- `check_digit` sums right-to-left doubling positions 0,2,4,... (the check digit itself is never
  doubled), then returns `(10 - total % 10) % 10`.
- Created `tests/test_luhn.py` covering every acceptance item verbatim, plus a consistency test
  that `check_digit` output appended to its payload passes `is_valid`.

## What I did NOT do
- Did not create or modify `base32.py`, `crc16.py`, or their tests (owned by other process cards).
- Did not modify any pre-existing file (`roman.py`, `legacy_stringkit.py`, existing tests, README,
  etc.). Only the two owned files plus the two team files were written.
- Did not commit or push.
- Not in scope but noted: `pytest` was not installed in this environment; I installed it with
  `python3 -m pip install --user pytest` (pytest 9.2.0) so the mandated checks could run. This
  touched only the runner's user site-packages, not the repository.

## Checks run and results
1. `python3 -m pytest tests/test_luhn.py -q` → `6 passed in 0.01s`
2. `python3 -m pytest tests/ -q` → `17 passed in 0.03s` (both pre-existing test files still pass)

Acceptance items verified by the test file: `79927398713` valid, `79927398710` invalid,
`4242424242424242` valid, `4242424242424241` invalid, `check_digit("7992739871") == 3`,
`check_digit("424242424242424") == 2`, `is_valid("12a3")` raises `ValueError`,
`check_digit("")` raises `ValueError`.

## What the validator must pay attention to
- Input validation is strict ASCII: `is_valid("12a3")` and `check_digit("")` raise `ValueError`,
  and so do `is_valid("１２３４")` (full-width digits) or `is_valid("12 3")`.
- `check_digit` and `is_valid` double complementary positions; a "regression" where they share
  the same parity would still pass the two `check_digit` examples only if consistent — the
  round-trip test (`check_digit` output passes `is_valid`) is the guard.
- No cross-module imports: `luhn.py` imports nothing from the project.
