# Handoff: yearday-convert (sub-issue #484)

## What was requested

Work order #478 (第四十六轮 · A 单). This process card owns only `yearday.py` and
`tests/test_yearday.py`:

- `to_yearday(year, month, day) -> int`: 1-based day-of-year (Jan 1 = 1). Gregorian
  leap rule (divisible by 4, not by 100 unless also by 400). year >= 1, month 1–12,
  day valid for that month, else ValueError; non-int (bool included) raises TypeError.
- `from_yearday(year, n) -> (month, day)`: n in 1–365 (common) / 1–366 (leap), else
  ValueError; same year/type rules as `to_yearday`.
- Every acceptance item from the card must have a test case.
- New files only; standard library only; no imports of hill/base45; do not modify
  any existing file.

## What I did

- Created `yearday.py`: helper `_is_leap`, shared type/range validators, month-length
  tables for common and leap years, `to_yearday` (cumulative sum of prior months +
  day), `from_yearday` (walk month lengths). Errors: TypeError for non-int args
  (bool rejected explicitly), ValueError for year < 1, month outside 1–12, invalid
  day, n outside 1–365/366.
- Created `tests/test_yearday.py` with a test for each acceptance item: items 1–8
  (to_yearday values), 9–14 (from_yearday values), 15 (round-trip parametrized over
  the 5 given triples), 16 (to_yearday ValueErrors: 2023-02-29, month 13, 2024-04-31,
  month 0), 17 (from_yearday ValueErrors: 2023/366, 2024/0, 2024/367), 18
  (TypeError: year "2024", 2024.0, True), plus extra type-error cases for month/day/n
  and year < 1 cases per spec.

## What I did NOT do

- Did not touch `hill.py`, `base45.py`, `roman.py`, `legacy_stringkit.py`, or any
  existing test file (owned by other process cards).
- Did not add or modify anything under `team/` other than this card's two files.
- Did not commit or push.
- Did not import hill or base45; module uses only the standard library (no imports
  at all).

## Checks run

From the repository root:

1. `python3 -m pytest tests/test_yearday.py -q` → **41 passed**
2. `python3 -m pytest tests/ -q` → **52 passed** (includes pre-existing
   test_roman.py and test_legacy_stringkit.py, unmodified)

Note: pytest was not installed in the environment initially; I installed it with
`python3 -m pip install pytest` (pytest 9.2.0) so the required checks could run. No
repository files were affected by that install.

## What the validator must pay attention to

- `to_yearday` and `from_yearday` reject `bool` explicitly before the `isinstance(int)`
  check, so `to_yearday(True, 1, 1)` raises TypeError (True is an int subclass in
  Python).
- Non-int `month`/`day`/`n` arguments also raise TypeError (spec: "非 int 输入抛
  TypeError" applies to the input parameters generally; `from_yearday` type rules
  "identical to to_yearday").
- `from_yearday` returns the padded/valid date only; bounds are enforced against the
  correct year length (365 vs 366) before the month walk.
- All 41 tests in tests/test_yearday.py map to the card's acceptance items; nothing
  in the spec's acceptance list is untested.
