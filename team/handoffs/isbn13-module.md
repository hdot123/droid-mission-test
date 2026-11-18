# Handoff: isbn13-module (sub-issue #287)

## What was requested

Process card `isbn13-module` under work order #278 (第三十五轮 · 并发加压第四组 B 单: 领班制 v2.6.5): implement the ISBN-13 checksum component as two new files only.

Specification:
- `check_digit(first12: str) -> int`: input must be exactly 12 pure-digit characters; compute the ISBN-13 check digit using alternating weights 1/3 with the leftmost digit weighted 1; raise `ValueError` on wrong length or any non-digit.
- `is_valid(isbn: str) -> bool`: `True` only for exactly 13 pure digits whose check digit matches; everything else (including hyphenated forms) returns `False` without raising.

Mandatory acceptance items (each covered by a test):
- `check_digit("978030640615") == 7`
- `is_valid("9780306406157") is True`
- `is_valid("9780306406158") is False`
- `check_digit("97803064061")` raises `ValueError` (11 digits)
- `is_valid("978-0-306-40615-7") is False`

Constraints: only new files, never modify existing files, standard library only, no imports from `luhn` or `mod97`.

## What I did

Created exactly two files:
- `isbn13.py` — implements `check_digit` and `is_valid`. Digit validation uses an explicit ASCII-digit membership check (`_is_ascii_digits`) rather than `str.isdigit()`, so non-ASCII digit characters (e.g. Arabic-Indic digits, superscripts) are rejected as non-digits. `check_digit` raises `ValueError` for non-string input, wrong length, or non-digits. `is_valid` returns `False` (never raises) for non-string input, wrong length, non-digits, and hyphenated forms; for 13 pure digits it recomputes the check digit over the first 12 and compares.
- `tests/test_isbn13.py` — 14 test cases: all five mandatory acceptance items plus additional invalid inputs (empty string, 13-digit input to `check_digit`, non-digit/`None`/hyphen inputs to both functions, too-short and too-long `is_valid` inputs).

Algorithm note: weights alternate 1, 3, 1, 3, ... from the left (index 0 gets weight 1), check digit = `(10 - total % 10) % 10`.

## What I did not do

- Did not touch `luhn.py`, `mod97.py`, `tests/test_luhn.py`, `tests/test_mod97.py`, or any other existing file (those belong to other processes).
- Did not implement or test Luhn or mod-97 logic; no cross-imports between the three components.
- Did not commit or push anything (workflow handles that).

## Checks run and results

Environment lacked pytest; installed it with `python3 -m pip install pytest` (pytest 9.2.0, environment-only change, no repo files touched).

1. `python3 -m pytest tests/test_isbn13.py -q` → **14 passed in 0.02s**
2. `python3 -m pytest tests/ -q` → **25 passed in 0.04s** (includes pre-existing roman/legacy_stringkit tests; all green, no regressions)

## Notes for the validator

- The two files are the only repo changes from this process; `team/handoffs/isbn13-module.md` and `team/status/isbn13-module.json` are the required team artifacts.
- Tests are plain `unittest.TestCase` classes runnable by pytest and directly by `python3 -m unittest`, matching the style of existing tests.
- `is_valid` deliberately treats non-string input as invalid (`False`) rather than raising; `check_digit` deliberately raises `ValueError` for the same input class, per spec.
- Verification status: validated. Both mandated checks executed and passing.
