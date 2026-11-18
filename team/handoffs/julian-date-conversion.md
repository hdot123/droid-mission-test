# Handoff: julian-date-conversion (sub-issue #397)

## What was requested
Process card `julian-date-conversion` under work order #383 (round 42 · unit D): create exactly two new files, `julian.py` and `tests/test_julian.py`, implementing Gregorian-calendar Julian Day conversion:

- `to_jd(y: int, m: int, d: int) -> int` — Julian Day number at 12:00 UT; year >= 1, month 1–12, day valid for that month (February follows the Gregorian leap rule: divisible by 4 and not by 100, or divisible by 400); otherwise `ValueError`.
- `from_jd(jd: int) -> tuple[int, int, int]` — inverse, returning `(year, month, day)`.

Acceptance points (each with a corresponding test): `to_jd(2000,1,1)==2451545`, `to_jd(1970,1,1)==2440588`, `to_jd(1999,12,31)==2451544`, `to_jd(2026,11,19)==2461364`, `to_jd(2024,2,29)==2460370`, `to_jd(1582,10,15)==2299161`, `from_jd(2451545)==(2000,1,1)`, `from_jd(2461364)==(2026,11,19)`, `ValueError` for `to_jd(2026,2,29)`, `to_jd(2026,13,1)`, `to_jd(2026,1,0)`, and round-trip identity for 2026-11-19.

## What I did
- Created `julian.py` (standard library only, no imports from `angle`/`bcd` or any repo module):
  - Validation of year/month/day with `ValueError` (leap-year rule in `_is_gregorian_leap`, month lengths via `_days_in_month`).
  - `to_jd` uses the Fliegel–Van Flandern integer formula (Julian Day at 12:00 UT).
  - `from_jd` uses the inverse Fliegel–Van Flandern conversion, returning `(year, month, day)`.
- Created `tests/test_julian.py` with 4 test functions covering every acceptance item:
  - `test_to_jd_known_dates` (all six `to_jd` values),
  - `test_from_jd_known_values` (both `from_jd` values),
  - `test_to_jd_invalid_inputs` (three `ValueError` cases),
  - `test_roundtrip_2026_11_19` (round-trip identity).

## What I did not do
- Did not touch any existing file (no edits to `roman.py`, `legacy_stringkit.py`, `README.md`, `tests/test_roman.py`, `tests/test_legacy_stringkit.py`, or anything under `.github/`).
- Did not create `angle.py`, `bcd.py`, or their tests (owned by other process cards).
- Did not commit or push (workflow handles that).

## Checks run
1. `python3 -m pytest tests/test_julian.py -q` → **4 passed**
2. `python3 -m pytest tests/ -q` → **15 passed** (my 4 + 11 pre-existing baseline tests)

Note: `pytest` was not installed in this environment initially (`No module named pytest`); I installed it with `pip3 install --user pytest` (pytest 9.2.0) to run the required checks. This is an environment setup step, not a repository file change.

## What the validator must pay attention to
- `to_jd` returns the integer JD at 12:00 UT (not00:00), matching the spec's acceptance values; the Fliegel–Van Flandern formula is used directly, and all six known-value tests pass exactly (no floating-point tolerance needed).
- Validation order: year, then month, then day — `to_jd(2026, 1, 0)` raises `ValueError` for day 0, `to_jd(2026, 13, 1)` for month 13, `to_jd(2026, 2, 29)` for the non-leap February 2026.
- `from_jd` is the exact integer inverse of `to_jd` for the tested range; round-trip identity for 2026-11-19 passes.
- Only two new files were added by this card: `julian.py` and `tests/test_julian.py`, plus the two team files (`team/handoffs/julian-date-conversion.md`, `team/status/julian-date-conversion.json`) required by the workflow.
