# Handoff: implement-anagram (sub-issue #46)

## What was requested
Process card `implement-anagram` under work order #42 (领班制 v2.6.1 稳定版复跑):

- Create `anagram.py` with exactly two public functions:
  - `are_anagrams(a, b)` — compare two strings as letter-only anagrams, ignoring case and all non-alphabetic characters. Examples: `are_anagrams("Dormitory", "dirty room")` is `True`, `are_anagrams("hello", "world")` is `False`.
  - `group(words)` — group a list of words into anagram groups, returning `list[list[str]]`; within each group words keep their original input order, and groups are ordered by the input position of each group's first word. Example: `group(["eat", "tea", "tan", "ate", "nat", "bat"])` → `[["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]`.
- Create `tests/test_anagram.py` covering: both `are_anagrams` examples, case and punctuation insensitivity, single-letter inputs, empty-string inputs, the `group` example, grouping of a single word, an empty word list returning `[]`, and preservation of input order within groups.
- Constraints: Python standard library only, no imports from other project modules, no CLI, no package directory. Owns only `anagram.py` and `tests/test_anagram.py`.

## What I did
- Implemented `anagram.py` using a shared private helper `_letters(text)` that filters to alphabetic characters and lowercases them.
  - `are_anagrams(a, b)` compares `sorted` lists of those filtered letters.
  - `group(words)` walks the input once, keying each word by `tuple(sorted(_letters(word)))`; new signatures start a new group appended at the end, existing signatures append the word to their group. This yields first-word input order for groups and input order within groups.
- Created `tests/test_anagram.py` with 8 tests covering every case the card listed.
- Installed `pytest` via `pip install --user pytest` (it was not present in the environment) so the process checks could run.

## What I did NOT do
- Did not create or modify `vigenere.py`, `chunk.py`, or their test files (owned by other process cards).
- Did not run the full `python -m pytest -q` suite (other processes' tests may not exist yet; only my own test file is in scope for this card).
- Did not commit, push, or edit any file outside `anagram.py`, `tests/test_anagram.py`, `team/handoffs/implement-anagram.md`, and `team/status/implement-anagram.json`.

## Checks I ran and results
1. `python -m pytest tests/test_anagram.py -q` → `8 passed in 0.02s` (exit 0).
2. `python -c "import anagram; assert anagram.are_anagrams('Dormitory','dirty room') is True; assert anagram.are_anagrams('hello','world') is False; assert anagram.group(['eat','tea','tan','ate','nat','bat'])==[['eat','tea','ate'],['tan','nat'],['bat']]"` → passed (exit 0).

## Notes for the validator
- Behavior details worth spot-checking: punctuation/whitespace are ignored entirely (`are_anagrams("A gentleman", "Elegant man!")` is `True`); `are_anagrams("", "")` is `True` while `are_anagrams("", "abc")` is `False`; an empty word list returns `[]`.
- `group` groups by the sorted letter signature of each word, so grouping is case- and punctuation-insensitive while the returned word strings are the untouched originals.
- `pytest` had to be installed into the environment; if the validator environment is fresh, run `pip install --user pytest` first or the pytest-based checks will fail with "No module named pytest".
- No cross-module imports exist in `anagram.py`; the three modules remain independent.
