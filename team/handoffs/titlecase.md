# Handoff: titlecase (sub-issue #870, round 55 concurrent C card)

## What was requested

Implement `titlecase.py` exposing `title_case(text: str) -> str` with the rules pinned verbatim in the work order (#850) and process card #870 (r2 retry), plus a new test file `tests/test_titlecase.py` covering every acceptance example. Card rules (r2 revision):

- Only two deliverable code files may be created: `titlecase.py`, `tests/test_titlecase.py`. No existing file modified. Standard library only; no import of `speedconv` or `divisorsum`.
- Plus exactly two team files: this handoff and `team/status/titlecase.json`.
- The ONLY mandated check: `python3 -m pytest tests/test_titlecase.py -q`, must exit 0. The full-suite run `python3 -m pytest tests/ -q` is deliberately NOT a card check (see below).

## What I did

- Created `titlecase.py`:
  - `title_case` splits on whitespace (normalization: runs collapse, strips ends; empty string -> `""`).
  - Per word: first alphabetic char uppercased, remaining letters lowercased; non-letter characters (symbols, digits, apostrophes) preserved as-is.
  - Small-word list (a, an, the, and, but, or, nor, for, so, yet, at, by, in, into, of, off, on, onto, per, to, up, via, as) implemented as a module-level frozenset; lowercase only when the word is neither first nor last.
  - Hyphenated compounds: segments processed individually; first segment always capitalized, later segments lowercase when they are small words (so `jack-of-all-trades` -> `Jack-of-All-Trades`, `e-mail` -> `E-Mail`).
  - Abbreviations not preserved as all-caps (`NASA and ESA` -> `Nasa and Esa`).
  - Non-`str` input (incl. `None`) raises `TypeError`.
- Created `tests/test_titlecase.py` with one test per acceptance example — all 20 examples from the work order, each as its own named test.

## What I did NOT do

- Did not modify or delete any existing file. Only added the two code files and the two team files.
- Did not implement `speedconv.py` or `divisorsum.py` (other cards own those).
- Did not touch `tests/test_check_summary_focused_counts.py` — the full suite exits 1 from a pre-existing `FileNotFoundError` under `/tmp/r54-audit/`. Per the card this is known out-of-scope context: I did not fix, seed, skip, or run it as a card gate.

## Checks run

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_titlecase.py -q` | exit 0 — `20 passed in 0.02s` |

Known out-of-scope context (not a card check): `python3 -m pytest tests/ -q` exits 1 solely because of the pre-existing `/tmp/r54-audit/` FileNotFoundError in `tests/test_check_summary_focused_counts.py`, which belongs to no process on this plan.

## Validator attention points

- Small-word check uses the letters-only view of the word (leading symbols stripped) so `(the)` still matches `the` while preserving the parens — this is what makes `title_case("(the) end") == "(The) End"` pass (first word, capitalized).
- Single-word inputs are always capitalized regardless of being in the small-word list (`"the"` -> `"The"`, `"in the"` -> `"In The"`).
- First segment of any hyphenated compound is always capitalized even mid-sentence; later segments use the small-word rule (`of` in `jack-of-all-trades` stays lowercase).
- Verdict files (`verdict.json` / `verdict.md`) appearing in the repo root are pipeline by-products of the test suite, not deliverables; none were present/kept from my runs.
