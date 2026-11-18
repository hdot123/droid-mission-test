# Handoff: monthshift-module (sub-issue #256)

## What was requested
Process card #256 for work order #247 (round 33, concurrency group C, foreman v2.6.5):
- Implement `monthshift.py` with two functions:
  - `add_months(year, month, delta)`: shift `(year, month)` by `delta` months (any integer, negative goes to the past), return the new `(year, month)` tuple; raise `ValueError` if `month` is outside 1-12 or the shifted year is `< 1`.
  - `add_months_to_date(year, month, day, delta)`: shift the full date; clamp `day` to the last day of the target month when it exceeds that month's length; raise `ValueError` if the input date itself is invalid.
- Required examples (all covered by tests):
  - `add_months(2026, 11, 3)` → `(2027, 2)`
  - `add_months(2026, 1, -2)` → `(2025, 11)`
  - `add_months(2026, 12, 1)` → `(2027, 1)`
  - `add_months_to_date(2026, 1, 31, 1)` → `(2026, 2, 28)`
  - `add_months_to_date(2024, 1, 31, 1)` → `(2024, 2, 29)`
  - `add_months_to_date(2026, 3, 31, -1)` → `(2026, 2, 28)`
- Also test `ValueError` cases (invalid month, shifted year < 1, invalid input date).
- Constraints: standard library only; no import of the other two modules; no package layout; no CLI.

## What I did
- Created `monthshift.py` in the repository root:
  - `add_months(year, month, delta)` validates `month` in 1-12 and `year >= 1`, converts to a 0-based absolute month index, adds `delta`, converts back, and raises `ValueError` if the resulting year is `< 1`.
  - `add_months_to_date(year, month, day, delta)` validates the input date (month range, day within the actual month length under proleptic Gregorian leap rules), shifts via `add_months`, then clamps `day` to the target month's last day (`min(day, days_in_month)`).
  - Leap-year rule used for February: divisible by 4 and not by 100, or divisible by 400.
  - Validation rejects non-int / bool values for `month`, `day`, `year`, and `delta` with `ValueError`.
- Created `tests/test_monthshift.py` with 24 tests covering all required examples, zero/large deltas, year rollovers, clamping in leap and common years, and every specified `ValueError` case. Tests import only `monthshift`.

## What I did NOT do
- Did not touch `intervals.py`, `weekday.py`, their tests, `roman.py`, `legacy_stringkit.py`, or any other pre-existing file.
- No package directory, no CLI, no cross-module imports.
- Did not commit or push (left to the workflow).
- Note: the bare `python` in this environment initially lacked pytest; I installed `pytest` 9.2.0 via `python3 -m pip install pytest` so the mandated check command could run. This changes only the environment, not the repository.

## Checks run
- `python -m pytest -q tests/test_monthshift.py` → **24 passed in 0.02s** (exit code 0).

## Notes for the validator
- The check command is the one from the process card, run verbatim from the repository root.
- Behavior matches the spec exactly: tuples are returned (not lists), clamping uses `min(day, days_in_month)`, and shifted-year `< 1` raises `ValueError` from `add_months` (and therefore also from `add_months_to_date` when the shift crosses below year 1).
- `add_months_to_date` validates the input date before shifting, so an invalid input day (e.g. 2026-02-30) raises even when `delta == 0`.
