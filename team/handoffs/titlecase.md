# Handoff: titlecase (sub-issue #863)

## What was requested

Work order #850 · concurrent card C · process card `titlecase`: create exactly two new files,
`titlecase.py` and `tests/test_titlecase.py`, implementing `title_case(text: str) -> str`
per the verbatim spec in #850/#863 (whitespace normalization, per-word capitalization with
leading symbols preserved, small-word list applied only to non-first/non-last words,
hyphenated compounds processed segment by segment, abbreviations lowercased NASA → Nasa,
non-str raises TypeError). No existing file may be modified; standard library only; no
imports from sibling modules (speedconv, divisorsum).

## What I did

- Created `titlecase.py` with `title_case(text)`:
  - `str.split()` tokenizes on any whitespace run and strips edges; empty/whitespace-only input returns `""`.
  - `_capitalize()` uppercases the first alphabetic character of a token, lowercases the rest,
    and passes non-alphabetic characters through unchanged (covers `"(the) end"`, `"123 go"`, `"don't look back"`).
  - `_alpha_core()` extracts the alphabetic core lowercased for small-word membership tests
    (so `"(the)"` counts as `the`).
  - Small words (the 24-word list from the spec) stay all-lowercase only when the word is
    neither first nor last; first/last are capitalized normally (`"in the"` → `"In The"`).
  - Hyphenated words are split on `-`: first segment always capitalized, later segments
    lowercased when they are small words, otherwise capitalized (`"jack-of-all-trades"` →
    `"Jack-of-All-Trades"`, `"mother-in-law"` → `"Mother-in-Law"`).
  - Whole-word small-word check happens after segment handling so a small word keeps its
    lowercase form in non-terminal positions.
  - Raises `TypeError` for any non-`str` input (including `None`).
- Created `tests/test_titlecase.py` with one test function per acceptance bullet: all 19
  string examples plus `title_case(None)` and a non-str (`42`) TypeError case (21 tests).

## What I did not do

- Did not touch any existing file (only the two new module/test files plus this handoff
  and `team/status/titlecase.json` were created).
- Did not implement `speedconv.py` or `divisorsum.py` (owned by concurrent cards).
- Did not import anything outside the standard library (module imports nothing at all).
- Did not commit or push.

## Checks run and results

- `python3 -m pytest tests/test_titlecase.py -q` → **21 passed** (all acceptance bullets).
- `python3 -m pytest tests/ -q` → **1 failed, 361 passed, 2 skipped**.

## What the validator must pay attention to

- The single full-suite failure is `tests/test_check_summary_focused_counts.py::
  test_summary_block_on_r54_pack_produces_real_focused_counts`, which fails with
  `FileNotFoundError: /tmp/r54-audit/a/evidence/packs/damm/checks-output.txt`. It reads
  external evidence files under `/tmp/r54-audit` that do not exist in this environment
  (verified: `/tmp/r54-audit` is absent). It fails identically when run in isolation and is
  entirely unrelated to this card (it exercises workflow summary-parsing code, not
  `titlecase`). It is a pre-existing environmental failure, not a regression from this change;
  it needs `/tmp/r54-audit` seeded or a skip guard, which is outside this card's scope.
- No `verdict.json` / `verdict.md` by-products were produced; repo root checked clean of them.
- A stray `42` non-str TypeError test was added alongside the required `None` case; both
  satisfy the "non str raises TypeError" contract.
