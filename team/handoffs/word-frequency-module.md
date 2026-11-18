# Handoff: word-frequency-module (sub-issue #148)

## What was requested
Process card #148 under work order #146 (text-statistics toolkit, round 25 R2 raw/comparison unit, foreman v2.6.5): deliver exactly the word-frequency capability of the toolkit as one root-level Python module `word_freq.py` plus its dedicated test file `tests/test_word_freq.py`. Requirements: Python standard library only; no package directory; no CLI; tests must exist, test only `word_freq.py`'s behavior (no imports of other modules), and implementation, tests, and docstrings must be mutually consistent. The card intentionally pre-decomposes nothing: function names, signatures, and behavior design were my decisions to make and document.

## What I did
- Created `word_freq.py` at the repository root with five documented functions (stdlib only: `re`, `collections.Counter`, `typing`):
  - `tokenize(text: str) -> List[str]` — splits text into word tokens (letters/digits, internal `'`/`-` allowed), preserves case, drops punctuation/whitespace; raises `TypeError` on non-str input.
  - `count_words(text: str) -> dict` — case-insensitive occurrence counts; keys lowercased, ordered by first appearance.
  - `top_words(text: str, n: int = 10) -> List[Tuple[str, int]]` — top-n `(word, count)` pairs sorted by descending count, ties broken alphabetically; `n <= 0` returns `[]`; non-int `n` raises `TypeError`.
  - `word_count(text: str) -> int` — total token count, equals `len(tokenize(text))`.
  - `unique_word_count(text: str) -> int` — number of distinct words, case-insensitive, equals `len(count_words(text))`.
  - Module docstring and per-function docstrings document each behavior (including doctest examples matching actual behavior).
- Created `tests/test_word_freq.py` covering all five functions: basic splitting, case preservation, empty/punctuation-only input, apostrophes/hyphens, TypeError cases, case-insensitive counting, ordering and tie-breaking in `top_words`, edge values of `n`, and cross-consistency assertions (`word_count == len(tokenize)`, `unique_word_count == len(count_words)`). The test file imports only `word_freq` (plus `pytest`).

## What I did NOT do
- Did not implement text normalization (another process's card) or sentence statistics (another process's card).
- Did not create shared utilities, a package directory, or any CLI.
- Did not add, modify, or delete any files other than `word_freq.py`, `tests/test_word_freq.py`, and the two required team files under `team/`.
- Did not commit or push (per instructions).

## Checks run and results
Both checks come verbatim from this card's `checks` array:

1. `python -m pytest -q tests/test_word_freq.py` — PASSED: `23 passed in 0.02s`.
2. `python -m pytest -q` (from repository root) — PASSED: `23 passed in 0.01s`.

Note: `pytest` was not preinstalled in the environment; I installed it with `python3 -m pip install pytest` before running the checks. At the time the full suite ran, only my own tests existed in the repo, so the full-suite result covers 23 tests (all from `tests/test_word_freq.py`); other processes' tests may add to the suite later.

## What the validator must pay attention to
- Scope: exactly two code files were delivered — `word_freq.py` and `tests/test_word_freq.py`. No normalization/sentence modules were touched (no omission from my side of the three-capability split; each capability is owned by its own card).
- Self-consistency: each function's docstring matches its tested behavior, including the deterministic tie-break rule (alphabetical ascending on equal counts) and case-insensitive counting in `count_words`/`top_words`/`unique_word_count` vs. case-preserving `tokenize`.
- The test file imports only `word_freq`, satisfying the isolation requirement.
- Check commands reported here are verbatim from the card's checks array and both exited 0.
