# Handoff: hexcolor (sub-issue #76)

## What was requested
Implement the `hexcolor` process card under work order #72 (领班制 v2.6.2, 第十五轮):
- `hexcolor.py` with three functions:
  - `parse(s)` — parses `"#RGB"` or `"#RRGGBB"` (case-insensitive) into an `(r, g, b)` int tuple, short form expanded by doubling each digit; raises `ValueError` on missing `#`, wrong length, or non-hex characters.
  - `to_hex(r, g, b)` — returns uppercase `"#RRGGBB"`; each component must be an `int` in 0–255, otherwise `ValueError`.
  - `is_valid(s)` — boolean version, never raises.
- `tests/test_hexcolor.py` covering only this module.
- Hard examples, written verbatim into the test file and check column:
  - `parse("#f80")` → `(255, 136, 0)`
  - `parse("#FF8800")` → `(255, 136, 0)`
  - `to_hex(255, 136, 0)` → `"#FF8800"`
- Constraints: standard library only; no imports between the three modules; no package directory; no CLI; only own files edited.

## What I did
- Created `hexcolor.py` implementing `parse`, `to_hex`, `is_valid` exactly per spec.
- Created `tests/test_hexcolor.py` with 12 tests, including the three hard examples verbatim, case-insensitivity, short-form doubling, invalid inputs (`ValueError`), out-of-range/non-int `to_hex` components, roundtrip, and `is_valid` boolean behavior (no raising).
- Wrote `team/handoffs/hexcolor.md` (this file) and `team/status/hexcolor.json`.

## What I did not do
- Did not create or edit `wordscore.py`, `caesar.py`, or their test files (owned by other processes).
- Did not edit any other repository file; no commits or pushes.
- Did not add CLI code, package directories, or non-standard-library dependencies.

## Checks run and results
1. `python -m pytest -q tests/test_hexcolor.py` → initially failed with `/usr/bin/python: No module named pytest` (pytest not installed in this environment). Installed pytest via `python3 -m pip install pytest`, then reran: **12 passed in 0.02s**.
2. `python -c "from hexcolor import parse, to_hex, is_valid; assert parse('#f80') == (255, 136, 0), 'example 1'; assert parse('#FF8800') == (255, 136, 0), 'example 2'; assert to_hex(255, 136, 0) == '#FF8800', 'example 3'; assert is_valid('#f80') is True and is_valid('f80') is False and is_valid('#gg0000') is False, 'is_valid boolean'; print('hexcolor examples all hold')"` → printed `hexcolor examples all hold` (exit 0).
3. `test -f hexcolor.py && test -f tests/test_hexcolor.py && echo files-present` → `files-present` (exit 0).

## Notes for the validator
- All three process checks pass after installing pytest; the `No module named pytest` failure was an environment gap, not a code defect. If the validating environment lacks pytest, install it before running check 1.
- The three hard examples are asserted both in the pytest file and in the standalone `python -c` check, matching the card's check column verbatim.
- `is_valid` is typed to return a real `bool` (`True`/`False`), satisfying the `is True` / `is False` assertions.
- `parse` rejects non-string input with `ValueError` (consistent with the "invalid format raises ValueError" rule).
- `to_hex` rejects `bool` components (e.g. `True`) as not being proper ints in 0–255 semantics; no spec example covers this, but it does not conflict with any stated requirement.
