# Handoff: isbn13-check-digit (sub-issue #360)

## What was requested
Implement the ISBN-13 check-digit component of work order #347 (round 40 · unit D):
- `isbn13.py` with `check_digit(first12: str) -> int` and `is_valid(isbn: str) -> bool`
- `tests/test_isbn13.py` with a test case for every acceptance item, verbatim
- New files only; do not touch tempconv, baseconv, or any existing file; standard library only; no imports from other project modules.

## What I did
Created exactly two new files:
- `isbn13.py` — `check_digit` validates the argument is exactly 12 digit characters (else `ValueError`), applies ISBN-13 weights 1,3 alternating from the left, and returns `(10 - total % 10) % 10`. `is_valid` strips all hyphens, requires exactly 13 digits afterwards (else `ValueError`), and compares the 13th digit against `check_digit` of the first 12.
- `tests/test_isbn13.py` — 8 tests covering every acceptance item verbatim: `check_digit("978030640615") == 7`; `is_valid("9780306406157") is True`; `is_valid("978-0-306-40615-7") is True`; `is_valid("9780306406158") is False`; `check_digit("978013468599") == 1`; `is_valid("9780134685991") is True`; `check_digit("97803064061")` raises `ValueError`; `is_valid("978030640615")` raises `ValueError`.

## What I did not do
- Did not create `tempconv.py`, `baseconv.py`, or their tests (other process cards own those).
- Did not modify any pre-existing file (`roman.py`, `legacy_stringkit.py`, existing tests, README, workflow files).
- Did not commit or push.
- Did not add non-stdlib dependencies to the project (pytest was installed into the runner environment only, so the mandated check commands could execute; no project file was changed for this).

## Checks run and results
- `python3 -m pytest tests/test_isbn13.py -q` → `8 passed` (exit 0)
- `python3 -m pytest tests/ -q` → `19 passed` (exit 0) — includes pre-existing roman/legacy_stringkit tests.

Note: the environment had no pytest module initially (`No module named pytest`); I installed it with `python3 -m pip install pytest` to run the checks. This does not affect any repository file.

## What the validator must pay attention to
- `check_digit` raises `ValueError` for wrong length *or* non-digit characters (spec requires a 12-digit numeric string).
- `is_valid` raises `ValueError` for anything that is not exactly 13 digits after removing all hyphens — including non-digit characters, wrong length, and empty string.
- Hyphens are removed anywhere in the string (`replace("-", "")`), per spec ("先全部去除").
- All acceptance values are asserted exactly; tests use `pytest.raises(ValueError)` for the two error cases.
- Only `isbn13.py` and `tests/test_isbn13.py` were added by this process.
