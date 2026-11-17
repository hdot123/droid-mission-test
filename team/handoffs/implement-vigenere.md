# Handoff: implement-vigenere (sub-issue #44)

## What was requested
Process card `implement-vigenere` for work order #42 (领班制 v2.6.1 稳定版复跑轮): own only `vigenere.py` and `tests/test_vigenere.py`.

- `vigenere.py` with `encrypt(text, key)` and `decrypt(text, key)`:
  - key must be a non-empty string of letters only, else `ValueError`;
  - key is case-insensitive and cycles over its letters;
  - only alphabetic characters in `text` are shifted (encrypt adds, decrypt subtracts the key letter's shift), preserving each character's original case;
  - non-alphabetic characters pass through unchanged and do not consume a key letter;
  - examples: `encrypt("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR"`, `encrypt("Hello, World!", "key") == "Rijvs, Uyvjn!"`, `decrypt` reverses `encrypt`.
- `tests/test_vigenere.py` covering: both examples, decrypt round-trip, case preservation, non-letter passthrough without key consumption, key cycling when shorter than the text, and `ValueError` for empty/non-letter keys.
- Constraints: Python standard library only; no imports from other project modules; no package directory; no CLI; tests cover only this module.

## What I did
- Created `vigenere.py`: `_validate_key` raises `ValueError` for non-str, empty, or non-`isalpha()` keys; `_shift_char` shifts within `A-Z`/`a-z` preserving case (non-letters returned as-is); `encrypt`/`decrypt` walk the text once, consuming a cycling key letter per alphabetic character only.
- Created `tests/test_vigenere.py` with 13 tests: both spec examples, decrypt round-trip (both directions), case preservation, non-letter passthrough (`encrypt("A!A", "LE") == "L!E"`, which distinguishes non-consuming from consuming), key cycling (`encrypt("AAAA", "AB") == "ABAB"`), and a parametrized `ValueError` test over `["", "123", "ab1", "ab c", "ab!", None, 42]` for both functions.

## What I did not do
- Did not create or touch `chunk.py`, `anagram.py`, their tests, or any other process's files.
- Did not create package directories, CLI entry points, or non-standard-library imports.
- Did not commit or push (left to the workflow).
- Did not run the full suite `python -m pytest -q` (it includes other processes' in-flight files); my scope check is `python -m pytest tests/test_vigenere.py -q`.

## Checks ran and results
1. `python -m pytest tests/test_vigenere.py -q` → `13 passed in 0.01s` (exit 0).
2. `python -c "import vigenere; assert vigenere.encrypt('ATTACKATDAWN','LEMON')=='LXFOPVEFRNHR'; assert vigenere.encrypt('Hello, World!','key')=='Rijvs, Uyvjn!'; assert vigenere.decrypt(vigenere.encrypt('Hello, World!','key'),'key')=='Hello, World!'; print('checks OK')"` → `checks OK` (exit 0).

Environment note: `pytest` was not preinstalled; I installed it with `python3 -m pip install pytest` (pytest 9.2.0) to run the required checks.

## What the validator must pay attention to
- My first draft of the non-letter test had a wrong hand-computed expectation (`"R!R"`); I fixed the test to a verified discriminating case (`encrypt("A!A", "LE") == "L!E"` — if `!` consumed a key letter the second `A` would use `L` again giving `"L!L"`). The implementation was correct throughout; only test expectations were corrected.
- The non-letter test relies on a 2-letter key so the "consumed vs not consumed" outcome differs on the very next letter; keep it that way if editing.
- Invalid-key validation accepts only `str` where `str.isalpha()` is true and non-empty; `None`/ints raise `ValueError` as covered.
- Round-trip property holds for all inputs: `decrypt(encrypt(t, k), k) == t`.
