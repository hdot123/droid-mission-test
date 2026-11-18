# Handoff: luhn-module (sub-issue #215)

## What was requested
Implement `luhn.py` in the repository root with two functions, plus `tests/test_luhn.py`:

- `check_digit(payload)`: input is a digits-only string WITHOUT the check digit; return the Luhn check digit as a single digit character. Algorithm: starting from the rightmost digit of `payload`, double every other digit counting from the right (rightmost is position 1, then positions 3, 5, ... are doubled); if a product is greater than 9, subtract 9; sum all digits; the check digit is `(10 - (sum % 10)) % 10`, returned as a character. Raise `ValueError` if `payload` is empty or contains any non-digit character.
- `is_valid(number)`: validate a full number INCLUDING its check digit. If `number` is not purely numeric (including the empty string) return `False` directly, never raise. Otherwise the last digit must equal the check digit computed from the remaining digits; return True/False accordingly.

Required examples: `check_digit("7992739871") -> "3"`; `check_digit("424242424242424") -> "2"`; `is_valid("79927398713") -> True`; `is_valid("79927398714") -> False`; `is_valid("7992739871a") -> False`.

Scope: owns only `luhn.py` and `tests/test_luhn.py`. Constraints: Python standard library only; `luhn.py` must not import `collatz`/`euclid`/any local module; no package directory; no CLI; `tests/test_luhn.py` tests only luhn behavior.

## What I did
- Created `luhn.py` with `check_digit` and `is_valid` per spec. Doubling parity: iterating `reversed(payload)` with 0-based index `i`, digits at even `i` (payload positions 1, 3, 5, ... from the right) are doubled; products > 9 get -9; check digit is `str((10 - (total % 10)) % 10)`. `check_digit` raises `ValueError` on empty or non-digit input (also on non-`str` input). `is_valid` returns `False` for non-`str`, empty, or non-digit input without raising, else compares the last digit against `check_digit(number[:-1])`.
- Created `tests/test_luhn.py` with 6 tests covering all five required examples, the `ValueError` cases for `check_digit` (empty, `"12a"`), and the False-not-raise behavior of `is_valid` on empty/non-numeric input.
- Installed `pytest` via `python -m pip install pytest -q` (it was not present in the environment; this was needed to run the mandated checks).

## What I did NOT do
- Did not create or modify `collatz.py`, `euclid.py`, or any other test file.
- Did not touch files owned by other processes.
- Did not create a package directory, CLI entry point, or any import of local modules.
- Did not commit or push.

## Checks run and results (commands verbatim from the process card check栏)
1. `python -c "import luhn; assert luhn.check_digit('7992739871') == '3'; ... assert ok"` (the full inline script from the card) — **passed** (exit 0).
2. `python -m pytest -q tests/test_luhn.py` — **passed**: `6 passed in 0.01s`.
3. `python -m pytest -q` — **passed**: `10 passed in 0.02s` (includes the other processes' tests; full suite green).

## Notes for the validator
- The first run of check 1 initially failed because I had the doubling parity inverted (doubled the wrong positions); I fixed `luhn.py` so the rightmost payload digit is doubled (position 1), which matches the spec and makes all five required examples pass. The final evidence above is from the corrected code.
- `pytest` was missing from the environment and was installed with `pip install pytest -q`; no other environment changes were made.
- `is_valid` never raises for any input type: non-`str` (e.g. `None`, `int`) also returns `False`.
