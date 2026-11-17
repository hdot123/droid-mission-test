# Handoff: anagram-module (sub-issue #135)

## What was requested
Process card `anagram-module` for work order #133 (第二十四轮 B 单, 领班制 v2.6.5):

- Own **only** `anagram.py` and `tests/test_anagram.py`.
- Implement `is_anagram(a, b)`: judge whether two strings are letter anagrams.
  - Compare only English letters; ignore case and all other characters.
  - Two empty strings (no letters at all) return `True`.
  - Examples: `is_anagram("Listen", "Silent")` → `True`, `is_anagram("hello", "world")` → `False`.
- Constraints: Python standard library only; must not import `gcdx`/`flatten`; no package directories; no CLI.
- Tests must cover only anagram behavior, including both worked examples, case/other-character ignoring, and the two-empty-strings `True` case.
- Check command (verbatim from the card's checks list): `python -m pytest -q tests/test_anagram.py`.

## What I did
- Created `anagram.py` with `def is_anagram(a: str, b: str) -> bool`. It extracts English letters only (`ch.isalpha() and ch.isascii()`), lowercases them, and compares sorted letter lists; two strings with no letters compare as equal → `True`.
- Created `tests/test_anagram.py` with 7 tests covering: both worked examples, case ignoring, other-character ignoring, empty-string `True`, no-letter strings `True`, and letter-count sensitivity (`"aa"` vs `"a"` → `False`).
- Ran the card's check command: `python -m pytest -q tests/test_anagram.py` → **7 passed in 0.01s** (exit 0). Note: the environment had no pytest module initially (`No module named pytest`); I installed pytest with `python -m pip install pytest -q`, then the check passed.

## What I did not do
- Did not touch `gcdx.py`, `flatten.py`, any other test file, `team/**` (other than my two assigned files), or `.github/**`.
- Did not import other modules, create package directories, add a CLI, or commit/push anything.

## Checks run and results
1. `python -m pytest -q tests/test_anagram.py` → initially failed only because pytest was missing (`No module named pytest`); after `python -m pip install pytest -q`, reran the exact check command → **7 passed, exit code 0**.

## For the validator
- The required check command comes verbatim from the card's checks list and now passes on this run.
- Acceptance item 1 (`python -m pytest -q` for everything) depends on the other processes' files (`gcdx.py`, `flatten.py`, etc.) existing in the shared tree; my card's own check is the per-module command above.
- Behavior note: non-ASCII letters (e.g. accented characters) are excluded as "not English letters", matching the "only English letters" spec.
