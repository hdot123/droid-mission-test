# Handoff: ngrams (sub-issue #916, work order #904 第57轮 D 单)

## What was requested

Process card `ngrams`: implement an n-gram segmentation module from scratch under the
round-57 D unit (lfucache / asciitable / ngrams), creating exactly two new files:

- `ngrams.py` (repo root)
- `tests/test_ngrams.py`

Spec (verbatim from the card):

- `char_ngrams(text: str, n: int) -> list[str]`: character sliding-window segmentation,
  each element is the substring window of length n.
- `word_ngrams(text: str, n: int) -> list[tuple[str, ...]]`: split words with
  `str.split()` (absorbs runs of whitespace, including tabs), then sliding windows of n
  words; each element is a **tuple** — not a list, not a joined string.
- Pure segmentation only: NO counting/reporting (that would be the wordfreq direction).
- Validation applies identically to both functions:
  - text length (word count for `word_ngrams`) < n → return `[]`
  - `n < 1` → `ValueError`
  - non-str text or non-int n (including `bool`, an int subclass) → `TypeError`
- Standard library only; no imports from `lfucache` / `asciitable`; no modification of
  any existing repository file; no files under `team/` besides the two required by this
  workflow instruction; nothing under `.github/`.

## What I did

1. Created `ngrams.py` with a shared `_validate(text, n)` helper (checks `str`-ness of
   `text`, rejects `bool`/non-`int` `n` with `TypeError`, then `n < 1` with
   `ValueError`) and the two public functions:
   - `char_ngrams` → list-comprehension sliding window over `text`.
   - `word_ngrams` → `text.split()` then list-comprehension of `tuple(...)` windows.
   - Validation runs **before** any windowing, so illegal `n` raises even when the
     text is shorter than `n`.
2. Created `tests/test_ngrams.py` with 19 tests covering every acceptance item in the
   card, including:
   - `char_ngrams("abcde", 2) == ["ab", "bc", "cd", "de"]`
   - `char_ngrams("ab", 3) == []`, `char_ngrams("", 1) == []`,
     `char_ngrams("aaa", 1) == ["a", "a", "a"]`
   - `word_ngrams("the quick brown fox", 2) == [("the", "quick"), ("quick", "brown"), ("brown", "fox")]`
     plus an explicit `isinstance(g, tuple)` assertion (tuple, not list/str)
   - `word_ngrams("one", 2) == []`
   - `word_ngrams("a  b\tc", 3) == [("a", "b", "c")]` (split absorbs runs of
     whitespace and tabs)
   - `char_ngrams("abc", 0)` and `word_ngrams("a b", -1)` → `ValueError`
   - `char_ngrams("abc", 2.0)`, `char_ngrams(123, 2)`, `word_ngrams("a b", True)` →
     `TypeError`
   - extras: unigram tuples, empty-text word_ngrams, `bool` n rejection on the char
     side, non-str/float rejection on the word side, and validate-before-slice order.

## What I did NOT do

- Did not touch `lfucache.py` / `asciitable.py` or their tests (other cards own them).
- Did not modify any pre-existing repository file (only the two named new files were
  created; `team/handoffs/ngrams.md` and `team/status/ngrams.json` are required
  workflow artifacts of this card).
- Did not add counting/reporting behavior, did not import from other round-57 modules.
- Did not create anything under `.github/`.
- Did not commit or push (workflow owns that).

## Checks ran and results

- `python3 -m pytest tests/test_ngrams.py -q` → **19 passed** in 0.02s
- `python3 -m pytest tests/ -q` → **361 passed, 2 skipped** in 20.37s (full suite
  green; the 2 skips are pre-existing and unrelated to this module)

Both checks exited 0.

## Notes for the validator

- The only behavior deliberately subtle: validation order. `_validate` runs before the
  length check, so `char_ngrams("a", 0)` raises `ValueError` rather than returning
  `[]` — the spec lists "n < 1 raises ValueError" unconditionally. A test pins this.
- `bool` is rejected explicitly (`isinstance(n, bool)` first), since `True` passes a
  bare `isinstance(n, int)` check in Python.
- `word_ngrams` elements are guaranteed `tuple` (cast inside the comprehension).
- The test file imports `from ngrams import ...`, relying on pytest rootdir/repo-root
  importability; if the suite is ever run from a different cwd, that is an environment
  issue, not a spec deviation.
- The full-suite run produces `verdict.json` / `verdict.md` in the repo root as
  pipeline by-products; they were deleted after the checks ran and are not deliverables.
