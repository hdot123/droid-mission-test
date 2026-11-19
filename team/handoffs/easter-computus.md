# Handoff: easter-computus (sub-issue #468)

## What was requested

Process card `easter-computus` for work order #457 (round 45, concurrent card C):

- Create `easter.py` implementing `easter_date(year: int) -> datetime.date` using the Anonymous Gregorian computus (Meeus/Jones/Butcher algorithm).
- Validation: `year` must be an `int` in 1583–4099; out of range raises `ValueError`; non-`int` raises `TypeError` (including `bool`, so `easter_date(True)` raises `TypeError`).
- Create `tests/test_easter.py` covering every acceptance item verbatim from the work order.
- Standard library only; do not import other deliverable modules; only add the two owned files; modify no existing files.
- Checks: `python3 -m pytest tests/test_easter.py -q` and `python3 -m pytest tests/ -q`.

## What I did

- Added `easter.py`: `easter_date` rejects `bool`/non-`int` with `TypeError` (checked before range, so `True` raises `TypeError` not `ValueError`), rejects years outside 1583–4099 with `ValueError`, and computes Easter via the Meeus/Jones/Butcher computus, returning a `datetime.date`.
- Added `tests/test_easter.py` with three test functions covering all 12 known-year assertions (2024, 2025, 2026, 2023, 2000, 1900, 1999, 2019, 2030, 2100, 1583, 4099), the two `ValueError` cases (1582, 4100), and the three `TypeError` cases (2026.0, "2026", True).

## What I did not do

- Did not create or touch `deltaenc.py`, `isogram.py`, or their tests (owned by other processes).
- Did not modify any existing file (`roman.py`, `legacy_stringkit.py`, existing tests, README, etc.).
- Did not import any deliverable module; only `datetime` and `pytest` (tests) are used.
- Did not commit or push.

## Checks run and results

Environment note: `pytest` was not installed in this environment; I installed it with `python3 -m pip install pytest` (user site-packages) before running the checks. No repository files were affected.

- `python3 -m pytest tests/test_easter.py -q` → `3 passed in 0.02s` (exit 0)
- `python3 -m pytest tests/ -q` → `14 passed in 0.03s` (exit 0)

## What the validator must pay attention to

- Type check runs before range check: `easter_date(True)` raises `TypeError` (spec requires this), not `ValueError`.
- Boundary years 1583 and 4099 are valid and asserted; 1582 and 4100 are out of range.
- All 12 known Easter dates from the work order are asserted verbatim in `test_known_years`.
- Only `easter.py` and `tests/test_easter.py` were added; `git status` should show only those two as my changes (plus any team/ files the workflow expects).
