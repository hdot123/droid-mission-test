# Handoff: isoweek-module (sub-issue #443)

## What was requested

Work order #432, process card `isoweek-module`: implement `isoweek.py` (Gregorian date <-> ISO week date conversion) and `tests/test_isoweek.py` in the repository root. Only these two files may be added; no existing files may be modified; standard library only; must not import `trie` or `bacon`. Every acceptance point in the work order must have a corresponding test case. Checks to run: `python3 -m pytest tests/test_isoweek.py -q` and `python3 -m pytest tests/ -q`.

## What I did

- Created `isoweek.py`:
  - `to_iso_week(y, m, d) -> (iso_year, iso_week, iso_weekday)` with weekday 1-7 (Monday = 1). Rejects non-int (and bool) inputs with `TypeError`, invalid dates (including `to_iso_week(2026, 2, 29)`) with `ValueError`. Built on `datetime.date.isocalendar()`.
  - `from_iso_week(iso_year, iso_week, iso_weekday) -> (year, month, day)`. ISO week 1 is anchored on the Monday of the week containing January 4; non-existent weeks (e.g. `2026/54`, `2021/53`) and out-of-range weekdays (0, 8) raise `ValueError`; non-int inputs raise `TypeError`.
- Created `tests/test_isoweek.py` with a test case for every acceptance point in the work order, plus type-error cases for both functions and a date-range roundtrip check against `datetime` (2015-01-01 through 2035-12-31).

## What I did not do

- Did not touch `trie.py`, `bacon.py`, or their tests (other process cards own those).
- Did not modify any pre-existing file (README, roman.py, legacy_stringkit.py, existing tests, etc.).
- Did not commit or push anything.
- Did not create `__init__.py` or any conftest; tests import `isoweek` from the repo root, matching the existing `test_roman.py` convention.

## Checks I ran and results

1. `python3 -m pytest tests/test_isoweek.py -q` -> `12 passed in 0.03s` (PASS)
2. `python3 -m pytest tests/ -q` -> `23 passed in 0.04s` (PASS)

Note: the base environment had no pytest (`No module named pytest`), so I installed it with `pip3 install --user pytest` (pytest 9.2.0) to run the required checks. This was the only environment change; no repository files were affected.

## What the validator must pay attention to

- All 8 `to_iso_week` acceptance vectors, all 5 `from_iso_week` success vectors, the 4 `from_iso_week` ValueError vectors, and the `to_iso_week(2026, 2, 29)` ValueError vector each have their own assertion in `tests/test_isoweek.py`.
- The error semantics are strict: `bool` counts as a non-int (`TypeError`), and year values outside 1..9999 raise `ValueError` in both functions.
- Roundtrip coverage goes beyond the mandated points: every date from 2015-01-01 to 2035-12-31 is checked against `datetime.date` semantics, so the ISO week-53 years (2020, 2026) and week-boundary years (2019/2020) are exercised in both directions.
- The full-suite check (`23 passed`) includes tests owned by other processes; if another card breaks its own tests, that is not attributable to this card.
