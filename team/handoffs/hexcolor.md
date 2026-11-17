# Handoff — hexcolor (sub-issue #99, retry r2)

## What was requested
Implement `hexcolor.py` exposing `parse(s)`, `to_hex(r, g, b)`, `is_valid(s)` per work order #95 / process card "hexcolor":

- `parse(s)`: accepts `"#RGB"` or `"#RRGGBB"` (case-insensitive), returns `(r, g, b)` int tuple, short form expanded by doubling each digit. Invalid format (missing `#`, wrong length, non-hex characters) raises `ValueError`.
- `to_hex(r, g, b)`: returns uppercase `"#RRGGBB"`; components must be int in 0–255 else `ValueError`.
- `is_valid(s)`: boolean version, never raises.
- Hard examples (verbatim): `parse("#f80") -> (255, 136, 0)`, `parse("#FF8800") -> (255, 136, 0)`, `to_hex(255, 136, 0) -> "#FF8800"`.
- Constraints: Python stdlib only; no imports of wordscore/caesar; no package directory; no CLI; tests cover only this module.

## What I did
- Created `hexcolor.py` with the three functions. `parse` validates the leading `#`, requires exactly 3 or 6 hex digits, doubles each digit of the short form, and explicitly rejects any character outside `0-9a-fA-F` (avoids `int(..., 16)` silently accepting whitespace). `to_hex` rejects non-int (including `bool` and `float`) and out-of-range components with `ValueError`, and formats uppercase with zero padding. `is_valid` wraps `parse` and returns False on `ValueError`.
- Created `tests/test_hexcolor.py` (15 tests) covering the three required verbatim examples, short-form expansion, case-insensitivity, missing `#`, wrong lengths, non-hex characters (including `"#8 8000"`), empty/`#`-only input, roundtrip, uppercase zero-padded output, out-of-range and non-int components, and `is_valid` true/false cases including `None`.
- Installed pytest 9.2.0 into the environment (`python3 -m pip install pytest`) — it was absent; the mandated checks use `python -m pytest`.

## What I did NOT do
- Did not touch `wordscore.py`, `caesar.py`, or any other process's tests.
- Did not create a package directory, CLI, or any imports between the three modules.
- Did not commit or push (workflow does that).

## Checks run (verbatim from card, actual results)
1. `python -m pytest -q tests/test_hexcolor.py` → **exit 0**, output: `............... [100%]` / `15 passed in 0.01s`
2. `python -m pytest -q` → **exit 0**, output: `............... [100%]` / `15 passed in 0.01s`
3. `python -c "from hexcolor import parse, to_hex, is_valid; ..."` → **exit 0**, output: `hexcolor examples ok`
4. `python -c "import hexcolor, inspect; print(inspect.signature(...))"` → **exit 0**, output:
   ```
   (s)
   (r, g, b)
   (s)
   ```

## What the validator must pay attention to
- **Check 2 evidence:** `python -m pytest -q` collects **only** `tests/test_hexcolor.py` (15 tests) in this checkout — no wordscore/caesar test files exist yet, so the full-suite count is 15, not the 14 previously recorded. Exit code 0 is real and matches the output above; both `handoff.md` (this file) and `status.json` report exit 0 / `15 passed` for check 2, consistent with the recorded output.
- The prior retry flagged a mismatch (claimed exit 0 "14 passed" while recorded exit was 1). This revision re-ran all four checks verbatim after the fix; every reported exit code and output string above is the actual captured result.
- One interim run failed (`parse("#8 8000")` did not raise because `int` strips whitespace); the explicit hex-character check in `parse` fixed it before the final runs.
- Note for the wordscore reconciliation: the work order's contradictory `score("abc") == 7` requirement is wordscore's card, not this one; this module has no such conflict.
