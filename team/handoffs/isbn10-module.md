# Handoff: isbn10-module (sub-issue #207)

## What was requested
Process card #207 under work order #202 (round 29, group A): implement `isbn10.py` at the repository root with exactly two functions, plus `tests/test_isbn10.py`, honoring this card's scope (own only those two files; no hamming/caesar work, no other test files, no `team/**` paths other than the two handoff/status files required by the harness, no package directory, no CLI, standard library only, no imports of other project modules).

Specification implemented:
- `check_digit(first9)`: input must be a 9-character string of ASCII digits; position i (1-based, leftmost = 1) has weight i; weighted sum of the first 9 digits mod 11 is the check value; value 10 maps to `"X"`; otherwise returns `"0"`–`"9"` as a string. Non-conforming input (wrong length, non-digit, non-string, non-ASCII digits) raises `ValueError`.
- `is_valid(code)`: full 10-character ISBN-10; first 9 must be ASCII digits, last must be an ASCII digit or `"X"`; check character computed from the first 9 must equal the last; any format problem returns `False` directly (never raises).
- Required examples: `check_digit("030640615") -> "2"`, `check_digit("043942089") -> "X"`, `is_valid("0306406152") -> True`, `is_valid("043942089X") -> True`, `is_valid("0306406153") -> False`.

## What I did
- Created `isbn10.py` with `check_digit` and `is_valid` per the spec above.
- Created `tests/test_isbn10.py` covering both function signatures/return types, all five required examples, the `ValueError` path of `check_digit` (short, long, empty, non-digit, whitespace-padded, fullwidth digits, `None`, `int`), and `is_valid` returning `False` without raising on malformed input (wrong length, bad check character, lowercase `x`, non-digit in first 9, bad last character, fullwidth digits, `None`, `int`).
- Installed `pytest` 9.2.0 into the environment (`pip install pytest`); it was not present initially, so `python -m pytest` could not run at all.

## What I did not do
- Did not touch `hamming.py`, `caesar.py`, `tests/test_hamming.py`, `tests/test_caesar.py`, `legacy_stringkit.py`, `tests/test_legacy_stringkit.py`, README, or any `team/**` file other than this handoff and `team/status/isbn10-module.json`.
- Did not create a package directory, `__init__.py`, or any CLI.
- Did not add imports of other project modules; `isbn10.py` imports nothing.
- Did not commit or push.

## Checks run and results
Check transcribed verbatim from this card's check column:

1. `python -m pytest -q tests/test_isbn10.py` — PASSED: `28 passed in 0.03s` (exit code 0).

Additional evidence (not part of the card check column, run to confirm no repo-wide regression):

2. `python -m pytest -q` — PASSED: `32 passed in 0.03s` (28 isbn10 + 4 pre-existing `tests/test_legacy_stringkit.py`).

Note: the first attempt at check 1 failed with `/usr/bin/python: No module named pytest` because pytest was absent from the environment; after `pip install pytest` the same command passes. The check command itself was run verbatim as written.

## What the validator must pay attention to
- Digit checks are ASCII-only (`str.isascii() and str.isdigit()`), so fullwidth digits like `"１２３４５６７８９"` are rejected: `check_digit` raises `ValueError`, `is_valid` returns `False`. This is stricter than bare `isdigit()`, which accepts Unicode digits; the spec says "9 位纯数字"/ASCII digits.
- `is_valid` never raises: non-string inputs (`None`, `int`) and wrong-length codes return `False` rather than raising, matching "格式不对直接返回 False（不抛异常）".
- `check_digit` raises `ValueError` for `None`/`int` inputs as well as malformed strings, since they are "not 9 位纯数字".
- All five spec examples are asserted verbatim in `tests/test_isbn10.py`.
- Test file only exercises `isbn10`; no cross-module imports.
- `python -m pytest -q` for the whole repo passes (32 tests), so the acceptance criterion at the work-order level holds for this card's contribution.
