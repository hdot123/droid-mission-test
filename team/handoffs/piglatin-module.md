# Handoff: piglatin-module (sub-issue #118)

## What was requested
Process card `piglatin-module` under work order #113 (round 22 A-unit, foreman v2.6.4). Scope was strictly two files:
- `piglatin.py` in the repository root, exposing exactly `translate(word)`:
  - vowel start (a/e/i/o/u, case-insensitive) -> append `"way"`;
  - consonant start -> move the initial consecutive consonants to the end and add `"ay"`;
  - preserve capitalization shape (all-lowercase in -> all-lowercase out; initial-capital in -> initial-capital out);
  - worked examples that must hold exactly: `translate("apple") == "appleway"`, `translate("banana") == "ananabay"`, `translate("string") == "ingstray"`.
- `tests/test_piglatin.py` covering only this module: the three worked examples verbatim, vowel-start and consonant-start rules, multi-consonant clusters ("string", "chair"), case preservation for lowercase and initial-capital inputs, and empty-string/invalid input handling documented in the test.

Constraints: Python standard library only; `piglatin.py` must not import the other modules (roman/isbn); no package directory; no CLI; the test file tests only this module.

## What I did
- Created `piglatin.py` with `translate(word)` implemented as specified. Behavior details:
  - Vowel-start: `lower + "way"`, then case applied.
  - Consonant-start: split point is the first vowel in the lowered word; `lower[i:] + lower[:i] + "ay"`.
  - Case shape: if `word[0].isupper()`, the first output character is uppercased; otherwise the output is exactly the lowered pig-Latin form (all-lowercase input stays all-lowercase).
  - Invalid input raises `ValueError` (documented choice, consistent with the sibling modules' convention): non-string input (`123`, `None`), empty string `""`, and non-single-word input (`"hi!"`, `"two words"`). All other inputs are single alphabetic words.
  - Module imports only the Python standard library in spirit (no imports at all besides the docstring); it does not import `roman` or `isbn`.
- Created `tests/test_piglatin.py` with 9 tests covering exactly the card's required behaviors (see checks below).

## What I did NOT do
- Did not touch `roman.py`, `isbn.py`, `tests/test_roman.py`, `tests/test_isbn.py`, or any other repository file — those belong to other process cards.
- Did not create a package directory, `__init__.py`, or any CLI entry point.
- Did not commit or push (workflow handles that).
- Did not run the full-suite gate `python -m pytest -q` as a *card* requirement — the card marks the full-suite run as the final gate at 汇总收口; my card-level scope was only `python -m pytest -q tests/test_piglatin.py` plus the assertion snippet, both run verbatim below.

## Checks run (verbatim commands, from repository root) and results

1. `python -m pytest -q tests/test_piglatin.py`
   - First attempt failed because the environment had no pytest (`/usr/bin/python: No module named pytest`). I installed pytest via `python -m pip install` (environment-only; no repo files touched). Re-run of the verbatim command after install:
   - Result: `......... [100%]` / `9 passed in 0.02s`, exit code 0.

2. `python - <<'PY' ... PY` (the assertion snippet exactly as given in the card's `checks` array, verbatim):
   ```
   from piglatin import translate
   assert translate('apple') == 'appleway'
   assert translate('banana') == 'ananabay'
   assert translate('string') == 'ingstray'
   assert translate('Apple') == 'Appleway'
   assert translate('Banana') == 'Ananabay'
   assert translate('String') == 'Ingstray'
   print('piglatin OK')
   ```
   - Result: `piglatin OK`, exit code 0.

## What the validator must pay attention to
- The two commands above were run exactly as written in this card's `checks` array, from the repository root, and both passed. Outputs are recorded in `team/status/piglatin-module.json`.
- pytest was absent from the environment initially; it was installed to make the prescribed check runnable. The final gate `python -m pytest -q` at 汇总收口 should be run in an environment where pytest is present (it now is, in this workspace).
- `translate` deliberately raises `ValueError` for empty string, non-string, and non-alphabetic/multi-word input; the test file documents these choices explicitly (tests `test_empty_string_raises_value_error`, `test_non_string_input_raises_value_error`, `test_non_alphabetic_input_raises_value_error`).
- Files owned by this card: `piglatin.py`, `tests/test_piglatin.py`, plus `team/handoffs/piglatin-module.md` and `team/status/piglatin-module.json`. Nothing else was modified.
