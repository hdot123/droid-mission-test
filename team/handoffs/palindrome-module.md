# Handoff: palindrome-module (sub-issue #10)

## What was requested
Implement `palindrome.py` with two functions and a dedicated test file:

- `clean_text(text)` returns a string keeping only alphanumeric characters, lowercased (letters and digits only, everything else removed).
- `is_palindrome(text)` judges palindromes based on `clean_text`; an empty string after cleaning counts as a palindrome.
- `tests/test_palindrome.py` covering: clean_text stripping punctuation/symbols/spaces and lowercasing; is_palindrome true cases with mixed case and separators; false cases; empty string as palindrome; single-character input.

Constraints: Python standard library only; do not import other project modules; no package directories; no CLI; the test file must only test palindrome behavior; only edit files owned by this process.

## What I did
- Created `palindrome.py` exposing `clean_text(text)` and `is_palindrome(text)`. `clean_text` uses `str.isalnum()` + `str.lower()` per character; `is_palindrome` compares the cleaned string against its reverse.
- Created `tests/test_palindrome.py` with 7 pytest tests covering all required behaviors, including digits kept by `clean_text` and the empty-after-clean case counting as a palindrome.
- Installed `pytest` (9.2.0) into the environment because no interpreter had it; this was an environment fix, not a repo change.

## What I did not do
- Did not create or modify `rot13.py`, `runlength.py`, or any test file other than `tests/test_palindrome.py`.
- Did not add package directories, CLI entry points, or any non-standard-library dependency in the delivered files.
- Did not run the full-repo acceptance check (`python -m pytest -q` at repo root) — that is the foreman/acceptance step, outside this card's scope.
- Did not commit or push.

## Checks I ran and results
- `python -m pytest -q tests/test_palindrome.py` → `7 passed in 0.01s` (run from the repository root). Ran twice; second run after removing an unused `import pytest` from the test file.

## What the validator must pay attention to
- Behavior definition: a string that cleans to empty (e.g. `"!!"`, `"   ,,, !!! "`) is a palindrome per spec; the tests assert this explicitly.
- `clean_text` keeps digits, not just letters (e.g. `"AbC123xYz"` → `"abc123xyz"`), matching the alphanumeric requirement.
- `is_palindrome` is case- and separator-insensitive because it delegates entirely to `clean_text`.
- The delivered code uses only the standard library; `pytest` was installed only as a test runner for the environment.
