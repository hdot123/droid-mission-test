# Handoff: roman-module (sub-issue #116)

## What was requested
Process card `roman-module` for work order #113 (第二十二轮 A 单 · 结业考双计划并发 · 领班制 v2.6.4):

- Create `roman.py` in the repository root with exactly:
  - `to_roman(n)`: integer 1–3999 → Roman numeral string, standard subtractive notation (4 → "IV", 9 → "IX", 1994 → "MCMXCIV").
  - `from_roman(s)`: valid Roman numeral string → integer.
  - Invalid input (out-of-range n, non-integer n, invalid Roman string) raises `ValueError`.
- Create `tests/test_roman.py` covering this module only: the worked examples, round-trips across 1–3999, and ValueError cases (0, 4000, non-integer, malformed strings such as "IIII"-style, empty string).
- Constraints: Python standard library only; `roman.py` must not import other modules; no package directory, no CLI; test file tests only this module.
- Run this card's two check commands verbatim from the repository root and record real output here and in `team/status/roman-module.json`.

## What I did
- Implemented `roman.py` with `to_roman(n)` and `from_roman(s)`:
  - `to_roman` rejects non-`int` (including `bool`) and values outside 1–3999 with `ValueError`; greedy subtraction with the standard table (M/CM/D/CD/C/XC/L/XL/X/IX/V/IV/I).
  - `from_roman` rejects empty/non-string input, bad characters, and non-canonical forms (e.g. "IIII", "VV", "IC", "XM") by validating that `to_roman(total)` round-trips to the input; results outside 1–3999 raise `ValueError`.
- Implemented `tests/test_roman.py` with 19 tests: worked examples, representative value cases, a full round-trip loop over `range(1, 4000)`, and parametrized `ValueError` cases for both functions.
- Installed `pytest` (9.2.0) into the environment, which did not have it; no repository files were changed for this.
- Ran both card checks verbatim from the repository root; results recorded below.

## What I did not do
- Did not create or modify `isbn.py`, `piglatin.py`, or their test files (owned by other cards).
- Did not edit any other repository file (README, workflow files, etc.).
- Did not commit or push; the workflow handles that.
- Did not run the full-suite gate `python -m pytest -q` (final gate belongs to 汇总收口); only this card's checks.

## Checks run and results
1. `python -m pytest -q tests/test_roman.py` → exit 0:
   ```
   ...................                                                      [100%]
   19 passed in 0.03s
   ```
2. Verbatim assertion script (`from roman import to_roman, from_roman ...`) → exit 0, printed:
   ```
   roman OK
   ```
   This confirms examples 4/9/1994, `from_roman('MCMXCIV')==1994`, full round-trip 1–3999, and `ValueError` for `(0, 4000, -1, 3.5, 'x', '', 'IIII')`.

## Notes for the validator
- `roman.py` imports nothing beyond the language itself; no cross-module imports exist.
- `from_roman` enforces canonical forms: both "IIII" and non-canonical subtractive forms (e.g. "IC") raise `ValueError`, matching the card's "malformed strings such as 'IIII'-style invalid forms if you enforce standard forms".
- `to_roman` treats `bool` as invalid (a `bool` is an `int` subclass in Python) so `True` raises `ValueError`.
- Test count is 19; all passed under pytest 9.2.0 on Python 3.14.4.
