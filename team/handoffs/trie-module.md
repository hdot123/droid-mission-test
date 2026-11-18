# Handoff: trie-module (sub-issue #444)

## What was requested
Process card "trie-module" under work order #432 (round 44 · C): add only `trie.py` and `tests/test_trie.py` implementing `class Trie` with `insert`, `search`, `starts_with`, `count_prefix`, `words_with_prefix`. Duplicate inserts must be idempotent. All methods raise `ValueError` on empty string and `TypeError` on non-str input. Standard library only; no imports of `isoweek` or `bacon`; no modification of any existing file.

## What I did
- Created `trie.py`: a node-based trie (`_Node` with `children` dict and `is_word` flag). `count_prefix` walks to the prefix node and counts distinct word-ending descendants; `words_with_prefix` collects those words, prepends the prefix back to each (collection starts at the prefix node), and returns them sorted lexicographically. Duplicate `insert` only re-sets `is_word`, so counts never change. Input validation is centralized in a static `_check` (type check first → `TypeError`, then empty check → `ValueError`).
- Created `tests/test_trie.py` covering every acceptance bullet from the work order:
  - hits: `app`, `banana`, `cat`; misses: `appl`, `ban`, `dog`
  - `starts_with`: `app`/`ban` true, `dog` false
  - `count_prefix`: 3, 3, 2, 1, 0 for `app`/`ban`/`band`/`c`/`z`
  - `words_with_prefix`: exact list equality for `app` and `ban`, `[]` for `z`
  - idempotent re-insert of `"app"` keeps `count_prefix("app") == 3`
  - `ValueError` on empty string and `TypeError` on `123` for **all five** methods (parametrized)

## What I did not do
- Did not touch `isoweek.py`, `bacon.py`, their tests, or any other existing file (including `roman.py`, `legacy_stringkit.py`, `tests/test_roman.py`, `tests/test_legacy_stringkit.py`).
- Did not commit or push.
- Did not import anything outside the standard library (trie.py imports nothing).

## Checks run
- `python3 -m pytest tests/test_trie.py -q` → **16 passed**
- `python3 -m pytest tests/ -q` → **27 passed** (includes pre-existing roman/legacy tests)

Note: `pytest` was not installed in the environment; I installed it via `python3 -m pip install pytest` (pytest 9.2.0) to run the required checks. No repository files were changed by this.

## Notes for the validator
- One bug was found and fixed during testing: `words_with_prefix` initially returned suffixes relative to the prefix node (e.g. `['', 'le', 'lication']`); fixed by prepending the prefix to each collected word. Final code passes.
- `words_with_prefix` returns full words including the prefix itself, sorted lexicographically — matches the spec's `["app", "apple", "application"]`.
- `count_prefix` counts distinct words (idempotent by construction), not insertion count.
- Validation order is `TypeError` for non-str before `ValueError` for empty; an input like `""` (str) raises `ValueError`, and `123` raises `TypeError`, as specified.
