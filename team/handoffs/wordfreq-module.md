# Handoff: wordfreq-module (sub-issue #16)

## What was requested
Implement the word frequency module for work order #12 (foreman v2.6.1 test round), scoped to process card `wordfreq-module`:

- `wordfreq.py` in the repository root: `top_words(text, n)` counts words where a word is a maximal run of ASCII letters or digits, lowercased for counting; returns `list[tuple[str, int]]` sorted by descending frequency, ties broken by word in ascending alphabetical order, truncated to the first `n` entries; `n <= 0` returns `[]`; `n` larger than the number of distinct words returns all of them.
- `tests/test_wordfreq.py` covering: case-insensitive + digit mixing, punctuation splitting, descending frequency order, alphabetical tie-breaking, `n` boundaries (0, negative, exceeding total), and empty text.
- Python standard library only; no package directory; no CLI; no import of `morse` or `brackets`.

## What I did
- Created `wordfreq.py` using `re` from the standard library: `[A-Za-z0-9]+` tokenization, `str.lower()` normalization, `sorted(..., key=lambda item: (-count, word))` for ranking, slice to `n`.
- Created `tests/test_wordfreq.py` with 8 tests, importing only `wordfreq`.
- Created `team/handoffs/wordfreq-module.md` (this file) and `team/status/wordfreq-module.json`.

## What I did not do
- Did not create or edit `morse.py`, `brackets.py`, or their tests (owned by other processes).
- Did not create a package directory, `__init__.py`, or any CLI entry point.
- Did not import either sibling module.
- Did not edit `README.md`, `.github/`, or any workflow files.
- Did not commit or push.

## Checks run and results
- `python -m pytest -q tests/test_wordfreq.py` → **8 passed** (exit code 0).

Note: pytest was not preinstalled in this environment; I installed it via `python -m pip install pytest` (the repo's prep step normally does this deterministically). If the prep step has already run, this install is a no-op.

## What the validator must pay attention to
- Tokenization is ASCII-only (`[A-Za-z0-9]+`), matching the spec's "letters or digits" wording; non-ASCII letters (e.g. `é`) are treated as delimiters, not word characters.
- Punctuation-only or empty text returns `[]` for any `n > 0`.
- The tie-break is on the lowercased word, so sorting is stable regardless of input case.
- Tests in `tests/test_wordfreq.py` reference only `wordfreq`; running the full suite (`python -m pytest -q` at the repo root) should pass once the other two modules and their tests land.
