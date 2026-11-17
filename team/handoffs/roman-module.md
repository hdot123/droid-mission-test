# Handoff: roman-module (sub-issue #127)

## What was requested
Work order #120 (第二十三轮 A 单, 领班制 v2.6.5). This process card covers only:
- `roman.py` in the repo root: `to_roman(n)` converts integers 1–3999 to Roman numeral strings (standard subtractive notation, e.g. 4→"IV", 9→"IX", 1994→"MCMXCIV"); `from_roman(s)` converts a valid Roman numeral string back to an integer. Invalid input (out of range, non-integer, invalid string) raises `ValueError`.
- `tests/test_roman.py`: tests covering the required examples (4/"IV", 9/"IX", 1994/"MCMXCIV"), boundaries (1, 3999), round-trips, and ValueError cases (out-of-range / non-integer / invalid string).
- Constraints: Python standard library only; `roman.py` must not import other project modules; no package directory; no CLI; test file only tests `roman.py`.

## What I did
- Created `roman.py` with `to_roman(n)` and `from_roman(s)`.
  - `to_roman`: rejects non-integers (including `bool`, `float`, `str`, `None`) and values outside 1–3999 with `ValueError`; builds the numeral greedily over the standard subtractive table (M, CM, D, CD, C, XC, L, XL, X, IX, V, IV, I).
  - `from_roman`: rejects non-strings, empty strings, and non-Roman characters with `ValueError`; parses greedily (subtractive pair when next value is larger), then validates canonical form by round-tripping through `to_roman` and range 1–3999, so non-canonical spellings ("IIII", "VV", "IC", "XM", "IXI") also raise `ValueError`.
- Created `tests/test_roman.py` with 25 test cases covering all required examples, boundaries, round-trips, and ValueError paths.

## What I did NOT do
- Did not create or modify `isbn.py`, `piglatin.py`, or any other test file (owned by other process cards).
- Did not touch `team/**` beyond this handoff and `team/status/roman-module.json`, and did not touch `.github/**`.
- Did not build a package directory, CLI, or import any other project module from `roman.py`.
- Did not commit or push.

## Checks run and results
Commands run verbatim from this card's checks column, from the repo root:

1. `python -m pytest -q tests/test_roman.py` → exit 0: `25 passed in 0.03s`
2. `python -m pytest -q` → exit 0: `25 passed in 0.02s`

Note: the base image had no pytest, so I ran `python -m pip install pytest` first (installed pytest 9.2.0). That was an environment setup step, not a process check; the two checks above are the card's own commands and both pass. At the time of this run the full suite contains only the roman tests (other modules are other cards' work), so check 2 currently equals check 1 in coverage.

## What the validator must pay attention to
- `to_roman` raises `ValueError` for non-integers as well as out-of-range values; `bool` inputs (`True`/`False`) are rejected as non-integers.
- `from_roman` accepts only canonical Roman numeral strings; anything that parses to a value whose canonical form differs (e.g. "IIII", "IC") raises `ValueError`, as does any non-Roman character, empty string, or non-string input.
- Required examples hold: `to_roman(4) == "IV"`, `to_roman(9) == "IX"`, `to_roman(1994) == "MCMXCIV"`, `to_roman(1) == "I"`, `to_roman(3999) == "MMMCMXCIX"`, and round-trips `from_roman(to_roman(n)) == n` for all n in 1–3999 by construction of the greedy table.
- Scope was strictly `roman.py` and `tests/test_roman.py`; no other files were modified.
