# Handoff: weekday-module (sub-issue #254)

## What was requested
Implement `weekday.py` and `tests/test_weekday.py` for work order #247 (round 33, group C), scoped to this process card only:
- `is_leap_year(year)`: Gregorian rule (divisible by 4 and not by 100, or divisible by 400).
- `weekday(year, month, day) -> int` in 0–6, 0 = Monday, 6 = Sunday, proleptic Gregorian; year must be >= 1; invalid dates (month outside 1–12, day beyond month length, e.g. Feb 29 in a non-leap year) raise `ValueError`.
- Must derive the weekday in-module: no `datetime.weekday`/`isoweekday`, no `calendar` module functions for the weekday result; standard library only; no imports of `intervals`/`monthshift`; no package directory; no CLI.
- Required examples must be covered by tests: `is_leap_year(2000) -> True`, `is_leap_year(1900) -> False`, `is_leap_year(2024) -> True`, `is_leap_year(2026) -> False`, `weekday(1, 1, 1) -> 0`, `weekday(2000, 1, 1) -> 5`, `weekday(2024, 2, 29) -> 3`, `weekday(2026, 11, 18) -> 2`. Also test `ValueError` for invalid month/day and year < 1.

## What I did
- Created `weekday.py` with a pure-arithmetic day count: days elapsed before year `y` = `(y-1)*365 + (y-1)//4 - (y-1)//100 + (y-1)//400`, plus day-of-year offset (with +1 for leap days after February), modulo 7, anchored so 0001-01-01 = Monday (0). `is_leap_year` implements the Gregorian rule directly. Validation raises `ValueError` for year < 1, month outside 1–12, and day out of range (Feb 29 in non-leap years included).
- Created `tests/test_weekday.py` covering all eight required examples, additional known dates (1970-01-01 Thursday, 1899-12-31 Sunday), leap-year rule edge cases (4/100/400/2100/2400), and `ValueError` cases for year, month, and day.

## What I did not do
- Did not touch `intervals.py`, `monthshift.py`, their tests, or any other repository file.
- No package directory, no CLI, no cross-module imports.
- Did not commit or push (left to the workflow).

## Checks ran and results
- `python -m pytest -q tests/test_weekday.py` — initially failed only because pytest was not installed in the environment (`No module named pytest`). Installed pytest via `python3 -m pip install pytest`, then the check passed: **7 passed in 0.02s**.

## Notes for the validator
- The only deviation from a clean run was the missing pytest dependency in this environment; installing it was required to execute the card's mandated check verbatim. The check itself ran exactly as specified in the card: `python -m pytest -q tests/test_weekday.py`.
- Weekday derivation is self-contained in `weekday.py` (no `datetime`/`calendar` weekday usage).
