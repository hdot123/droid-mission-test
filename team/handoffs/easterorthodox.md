# Handoff: easterorthodox (sub-issue #818)

## What was requested

Process card #818, scoped to the easterorthodox component of work order #812 (第54轮并发A单):

- New file `easterorthodox.py` exposing `orthodox_easter(year) -> tuple[int, int]`.
- New file `tests/test_easterorthodox.py` covering every acceptance point verbatim from the card.
- Algorithm pinned by the card: (1) Julian computus `a = year % 4`, `b = year % 7`, `c = year % 19`, `d = (19c + 15) % 30`, `e = (2a + 4b − d + 34) % 7`, Julian month = `(d + e + 114) // 31`, Julian day = `((d + e + 114) % 31) + 1`; (2) add Gregorian offset `(year // 100 − year // 400 − 2)` days and return the resulting `(month, day)`.
- Validation: non-int (bool rejected) raises `TypeError`; `year` outside `1583 <= year <= 9999` raises `ValueError`.
- Constraints: only these two files added, standard library only, no imports of `graph` or `damm`, no existing files modified.

## What I did

- Implemented `easterorthodox.py` with the pinned two-step algorithm. The Julian date is converted to a day-of-year counted from March 1, the Gregorian offset is added, and the day-of-year is decoded against March/April/May lengths (31/30/31) to yield `(month, day)`.
- Type check is `isinstance(year, int) and not isinstance(year, bool)` so `True` is rejected as `TypeError`.
- Added `tests/test_easterorthodox.py` with a test case per acceptance point: all 12 pinned dates (2010, 2016, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2000, 1900, 2100), `ValueError` for 1582 and 10000, `TypeError` for `2024.0`, `"2024"`, and `True`, plus a return-shape check (2-tuple of ints).

## What I did not do

- Did not touch `graph.py`, `damm.py`, or any pre-existing file; did not commit or push.
- Did not implement or test anything outside this card's scope.

## Checks run

- `python3 -m pytest tests/test_easterorthodox.py -q` → **18 passed**.
- `python3 -m pytest tests/ -q` → **205 passed, 2 skipped** (pre-existing skips; suite green).

## Notes for the validator

- `pytest` was not installed in the environment; installed per `requirements-dev.txt` (`pytest>=7.4.0`, `jsonschema>=4.20.0`) before running checks. That is an environment setup step, not a repo change.
- Two intermediate bugs were fixed during development (day-of-year decoded from January instead of March 1; `month, length` tuple unpacked in the wrong order). The shipped code passes all pinned dates.
- No `verdict.json` / `verdict.md` by-products were left in the repo root.
