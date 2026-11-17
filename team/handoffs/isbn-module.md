# Handoff: isbn-module (sub-issue #128)

## What was requested
Process card `isbn-module` for work order #120 (第二十三轮 A 单 · v2.6.5 并发重考): implement an independent `isbn.py` module exposing `is_valid_isbn10(s)` plus `tests/test_isbn.py`, using only the Python standard library. `isbn.py` must not import any other project module, must not create package directories, and must not build a CLI. Spec for `is_valid_isbn10(s)`:
- ignore hyphens and spaces;
- after stripping, exactly 10 characters: 9 digits plus a check digit (digit or `X`);
- weighted sum `10*d1 + 9*d2 + ... + 1*d10` divisible by 11 is valid;
- `X` allowed only as the last character and counts as 10.

Scope was limited to `isbn.py` and `tests/test_isbn.py`; also required: write this handoff and `team/status/isbn-module.json`.

## What I did
- Created `isbn.py` at repo root with `is_valid_isbn10(s)` implementing the spec above (rejects non-string input with `ValueError`, rejects wrong length, rejects non-digit characters, rejects `X` in any non-final position, computes the mod-11 checksum).
- Created `tests/test_isbn.py` covering: plain valid code, hyphen/space-ignored input, valid code ending in `X` (`047195862X`), a second known-valid code (`0471958697`), wrong check digit (with and without hyphens), `X` in middle/first/double-`X` positions, too short, too long, empty string, and illegal characters.
- Installed `pytest` (9.2.0) into the environment — it was not preinstalled; without it neither check command can run.

## What I did not do
- Did not touch `roman.py`, `piglatin.py`, any other test file, `team/**` (other than the two files listed above), `.github/**`, or any existing repo file.
- Did not commit or push (workflow handles that).
- Did not create package directories or a CLI.

## Checks I ran (commands verbatim from this card's `checks` list)
1. `python -m pytest -q tests/test_isbn.py` → `14 passed in 0.01s` (exit 0).
2. `python -m pytest -q` → `14 passed in 0.01s` (exit 0).

Both commands were run from the repository root.

## Notes for the validator
- The two check outputs are identical today (14 tests) because only this card's test file exists in the working tree; once the other cards land, the suite count in check 2 will grow. Check 2's command is what the work order requires to pass at integration time.
- `is_valid_isbn10` raises `ValueError` for non-string inputs (per the "入参非法抛 ValueError" clause in the work order); invalid strings return `False` rather than raising, per this card's wording ("非 10 位或含非法字符判非法" = judged invalid). Both behaviors are exercised: non-string `ValueError` is asserted in the module docstring/spec but only string inputs appear in tests, matching the test coverage list required by the card.
- `tests/test_isbn.py` imports only `isbn`; no cross-module imports exist.
