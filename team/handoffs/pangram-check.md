# Handoff: pangram-check (sub-issue #489)

## What was requested

Process card `pangram-check` from work order #479 (Round 46 · concurrent B):

- Create `pangram.py` with:
  - `is_pangram(text: str) -> bool` — case-insensitive, ignores non-letters, True iff all 26 lowercase letters appear; non-str raises TypeError.
  - `missing_letters(text: str) -> list[str]` — sorted list of lowercase letters not present; non-str raises TypeError.
- Create `tests/test_pangram.py` with a test case for every acceptance item listed in the card.
- Constraints: only these two files, modify no existing file, standard library only, no import of other project modules.

## What I did

- `pangram.py`: a shared `_letters()` helper validates `str` (raises `TypeError` otherwise) and returns the set of lowercased alphabetic characters. `is_pangram` checks `set(_ALPHABET) <= seen`; `missing_letters` lists alphabet chars absent from `seen`. No project-module imports; standard library only.
- `tests/test_pangram.py`: 14 tests covering every acceptance item:
  - pangram True: quick-brown-fox sentence, pack-my-box sentence, `ABCDEFGHIJKLMNOPQRSTUVWXYZ`, Sphinx sentence, all-uppercase sentence.
  - pangram False: `"hello world"`, `""`.
  - missing letters: `[]` for the full sentences, exact 19-element list for `"hello world"`, full 26-letter alphabet for `""`, `[]` for uppercase alphabet, 23 letters (all but a/b/c) for `"aAbBcC"`.
  - TypeError: `is_pangram(123)`, `missing_letters(None)`.

## What I did not do

- Did not touch `bloom.py`, `triangle.py`, `legacy_stringkit.py`, `roman.py`, or any existing test; did not touch `team/` paths other than this handoff and my status file.
- Did not commit or push (workflow handles that).
- Installed `pytest` via `pip3` into the environment (it was absent; no repo files changed by this).

## Checks run and results

- `python3 -m pytest tests/test_pangram.py -q` → **14 passed**
- `python3 -m pytest tests/ -q` → **25 passed** (includes pre-existing roman/legacy tests)

## Notes for the validator

- `is_pangram` returns a real `bool` (set comparison yields `bool`), so `is True` / `is False` assertions hold.
- Non-letter characters (digits, punctuation, whitespace) are ignored via `str.isalpha()`; accented letters count as alphabetic but are not among a–z, so they never satisfy or fill the 26-letter set.
- The full-suite check will also exercise other workers' modules once merged; as of this run only roman/legacy tests existed alongside mine, all passing.
