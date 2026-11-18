# Handoff: ean13-module (sub-issue #163)

## What was requested
Implement `ean13.py` with `check_digit(first12)` and `is_valid(code)`, plus `tests/test_ean13.py`, per process card #163 (work order #157, round 26A):

- `check_digit(first12)`: input is a 12-digit numeric string; odd positions (1-based, from the left) weight 1, even positions weight 3; weighted sum mod 10, subtracted from 10, result 10 becomes 0; returns the check digit as an `int`. Non-12-digit / non-digit / non-string input raises `ValueError`.
- `is_valid(code)`: judges a 13-digit numeric string; wrong format returns `False` directly (never raises).
- Required examples as tests: `check_digit("400638133393") -> 1`, `is_valid("4006381333931") -> True`, `is_valid("4006381333932") -> False`.
- Constraints: Python standard library only; no imports of other modules; no package directory; no CLI; tests cover only this module.

## What I did
- Created `ean13.py` implementing `check_digit(first12)` and `is_valid(code)` exactly per spec (mod-10 mapping `(10 - remainder) % 10`, so 10 maps to 0).
- Created `tests/test_ean13.py` with 8 tests:
  - the three required examples,
  - all-zero input (`check_digit("000000000000") == 0`),
  - explicit weighting check (`"123456789012"` → 8),
  - the 10→0 mapping (`"000000000013"` → 0),
  - `check_digit` `ValueError` on wrong length, non-digit, non-string,
  - `is_valid` returning `False` (no raise) on wrong length, non-digit, empty, `None`.
- No imports beyond `pytest` in the test file and nothing at all in `ean13.py` (no cross-module imports).

## What I did NOT do
- Did not touch `vigenere.py`, `temperature.py`, their tests, repo-level tooling, or any other process's files.
- Did not modify any `team/**` files other than the two assigned to me (`team/handoffs/ean13-module.md`, `team/status/ean13-module.json`).
- Did not commit or push (workflow-owned).

## Checks run and results
Check command (verbatim from the process card's check column):

```
python -m pytest -q tests/test_ean13.py
```

Result: **passed** — `........ [100%] 8 passed in 0.02s` (exit code 0).

Environment note: `pytest` was not preinstalled in this runner (`python -m pytest` initially failed with `No module named pytest`); I installed it via `python3 -m pip install pytest` (pytest 9.2.0) so the prescribed check command could run verbatim. The check itself was then executed exactly as written.

## What the validator must pay attention to
- The required check command runs at the repository root against only `tests/test_ean13.py`; the full-suite check (`python -m pytest -q`) is owned by the work-order level, and this card's tests are independent of the other two modules.
- Spec examples are covered verbatim as tests; weighting and the 10→0 edge case are covered by dedicated tests.
- `is_valid` never raises on malformed input (verified including `None`), while `check_digit` raises `ValueError` for anything that is not a 12-char pure-digit string.
