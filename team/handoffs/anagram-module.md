# Handoff: anagram-module (sub-issue #221)

## What was requested
Process card #221 under work order #205 (round 29, D card): implement `anagram.py` with
`is_anagram(a, b)` and `group_anagrams(words)`, plus `tests/test_anagram.py`.

Spec:
- `is_anagram(a, b)`: case-insensitive comparison that ignores spaces and punctuation
  (only letters and digits participate), judged by character-count equality.
- `group_anagrams(words)`: group words by the anagram relation into a list of lists;
  groups ordered by the first appearance of each group's first member in the original
  list; within a group, original list order is preserved.
- Required examples: `is_anagram("Listen","Silent") -> True`,
  `is_anagram("Dormitory","Dirty room") -> True`, `is_anagram("hello","world") -> False`,
  `group_anagrams(["eat","tea","tan","ate","nat","bat"]) -> [["eat","tea","ate"],["tan","nat"],["bat"]]`.
- Constraints: Python standard library only; no imports of piglatin/runlength/non-stdlib;
  no package directory, no CLI; tests must cover every example above and only anagram behavior.

## What I did
- Created `anagram.py`: `_normalize(s)` keeps only letters/digits lowercased;
  `is_anagram` compares `sorted` normalized character lists; `group_anagrams` keys each
  word by its sorted normalized characters and appends to the first matching group,
  creating groups on first appearance (preserves both required orderings).
- Created `tests/test_anagram.py` with 8 tests covering all four required examples plus
  punctuation/case insensitivity, character-count sensitivity, group ordering on a
  reordered input, and the empty list.

## What I did not do
- Did not create or modify `piglatin.py`, `runlength.py`, or any other test file.
- Did not modify any other repository file, did not commit or push.
- Did not add a package directory, CLI, or any non-stdlib import (removed an initially
  unused `import string` before running checks).

## Checks run and results (verbatim from card's checks column)
1. `python -m pytest -q tests/test_anagram.py` → **PASS** (`8 passed in 0.01s`).
2. `python -c "import anagram; assert anagram.is_anagram('Listen','Silent') is True; assert anagram.is_anagram('Dormitory','Dirty room') is True; assert anagram.is_anagram('hello','world') is False; assert anagram.group_anagrams(['eat','tea','tan','ate','nat','bat']) == [['eat','tea','ate'],['tan','nat'],['bat']]"` → **PASS** (exit 0, no output).

Note: the environment initially had no `pytest` module (`python -m pytest` failed with
"No module named pytest"). I installed pytest 9.2.0 via `pip install pytest` so the
card's check command could run as written; both checks above were then executed
successfully.

## What the validator must pay attention to
- Both card checks pass exactly as written; acceptance criteria (1) and (2) hold for this
  card's deliverables (full-repo `python -m pytest -q` also passes: all tests green).
- Spec interpretation: normalization strips non-alphanumeric characters and lowercases;
  empty-vs-empty and punctuation-only inputs are equal by this rule (consistent with
  "only letters and digits participate in the comparison").
- Scope: only `anagram.py`, `tests/test_anagram.py`, and these two team files were
  touched. No commits were made.
