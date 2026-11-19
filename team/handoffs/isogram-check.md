# Handoff: isogram-check (sub-issue #470)

## What was requested

Create `isogram.py` with `is_isogram(word: str) -> bool` (case-insensitive, only a-z letters counted, non-letters ignored, empty string True, non-str raises TypeError) and `repeated_letters(word: str) -> list[str>` (letters occurring more than once, alphabetical order, empty list when no repeats, same rules), plus `tests/test_isogram.py` covering every acceptance item verbatim. Only these two deliverable files; standard library only; no imports of other deliverable modules; no existing files modified.

## What I did

- Created `isogram.py` implementing both functions via a shared `_letters` helper that validates the input is `str` (raising `TypeError` otherwise) and lowercases/keeps only a-z letters.
- Created `tests/test_isogram.py` with parametrized cases for all 14 `is_isogram` acceptance items, all 6 `repeated_letters` acceptance items, and `TypeError` cases for `is_isogram(123)` and `repeated_letters(None)`.

## What I did not do

- Did not touch `easter.py`, `deltaenc.py`, or any other existing file.
- Did not add, commit, or push anything.

## Checks run

- `python3 -m pytest tests/test_isogram.py -q` — passed.
- `python3 -m pytest tests/ -q` — passed.

## Notes for the validator

- Both acceptance check commands pass as specified.
- `is_isogram`/`repeated_letters` return fresh `bool`/`list` values (`is True`/`is False` comparisons in tests are safe).
- Non-letter characters (spaces, hyphens) and case are handled as specified; only ASCII a-z (case-insensitive) counts.
