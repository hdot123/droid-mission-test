# Handoff: roman-module (sub-issue #20)

## What was requested
Process card `roman-module` (sub-issue #20) under work order #18: implement `roman.py` at the repository root with two functions using only the Python standard library, plus `tests/test_roman.py`:

- `to_roman(n)`: convert an integer in 1–3999 inclusive to a Roman numeral string (e.g. `to_roman(4) == "IV"`, `to_roman(1994) == "MCMXCIV"`). Raise `ValueError` for any `n` outside 1–3999 (including 0, negatives, >3999; bools rejected too).
- `from_roman(s)`: convert a Roman numeral string back to an integer, raising `ValueError` for invalid forms: empty string, illegal characters, improper subtraction (`IC`, `VX`, `IIV`, `VIV`, ...), illegal repetition (`IIII`, `VV`, `MMMM`, ...), and any other non-canonical form.
- Scope: only `roman.py` and `tests/test_roman.py`; no package directories, no CLI, no imports of `csv` or any other project module.

## What I did
- Created `roman.py`:
  - `to_roman(n)` uses a greedy table walk (M, CM, D, CD, C, XC, L, XL, X, IX, V, IV, I) and validates input (`1 <= n <= 3999`, int, not bool) else `ValueError`.
  - `from_roman(s)` validates non-empty string and legal characters (`IVXLCDM`), rejects illegal consecutive runs (I/X/C/M max 3, V/L/D max 1), parses left-to-right rejecting any descending pair that is not one of the six canonical subtractive pairs (IV, IX, XL, XC, CD, CM), then rejects any result whose canonical re-encoding does not equal the input (final safety net).
- Created `tests/test_roman.py` covering: the given examples, round-trips for 1, 3, 4, 9, 40, 44, 90, 400, 999, 3999, `ValueError` on `to_roman` with 0, -1, 4000, `ValueError` from `from_roman` on empty string, illegal characters, illegal repetition, and improper subtraction.

## What I did NOT do
- Did not touch `csvline.py`, `median.py`, or their test files.
- Did not create package directories or a CLI; no `csv` import.
- Did not commit or push anything (per instructions).

## Checks run
1. `python -m pytest -q tests/test_roman.py` — first run failed (2 failures): a bug where V/L/D had max-run limit 0 instead of 1, rejecting valid single occurrences like `"IV"`. Fixed `_MAX_REPEAT` to `{"V":1,"L":1,"D":1}` and removed the redundant `limit == 0` check.
2. `python -m pytest -q tests/test_roman.py` after fix — **8 passed in 0.01s**.
3. Extra sanity script: all of `['IC','VX','IIII','VV','MMMM','XXL','IIV','VIV','IIX','XCM','CMM','','ABC','i']` raise `ValueError`; full round-trip `from_roman(to_roman(n)) == n` for every `n` in 1..3999 — OK.

## Notes for the validator
- Even-length canonical numerals like `XLII` and subtractive forms round-trip correctly; the final re-encode check in `from_roman` is what guarantees canonicity.
- Tests use only `pytest` and `roman`; no cross-module imports.
- The file `worker-prompt.txt` / `worker-stream.jsonl` in the repo root are pre-existing untracked session artifacts, not part of this deliverable.
