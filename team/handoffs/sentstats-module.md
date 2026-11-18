# Handoff: sentstats-module (sub-issue #155)

## What was requested
Implement `sentstats.py` (the sentence statistics module) for work order #144, process card `sentstats-module`, owning exactly two files:
- `sentstats.py`
- `tests/test_sentstats.py`

Spec (from the work order, verbatim behavior):
- `count_sentences(text)` — split on terminal punctuation `.` `!` `?`; a run of consecutive terminal punctuation counts as one separator; empty fragments are not counted. Examples: `count_sentences("Hello world. How are you? Fine!")` → `3`; `count_sentences("Wait... really?! Yes.")` → `3`.
- `average_sentence_length(text)` — average words per sentence (whitespace split), returned as a float; `0.0` when there are no sentences. Example: `average_sentence_length("One two. Three.")` → `1.5`.

Hard constraints (from the card, verbatim): Python standard library only; the three modules must not import each other (`sentstats` must not import `wordfreq` or `textnorm`); no package directory; no CLI; `tests/test_sentstats.py` tests only `sentstats`.

## What I did
- Implemented `sentstats.py` using `re.split` on the pattern `[.!?]+`:
  - `count_sentences(text)` counts non-blank fragments after the split.
  - `average_sentence_length(text)` returns `0.0` when no sentences, otherwise `total_words / sentence_count` (always a float via `/` division).
- Implemented `tests/test_sentstats.py` with 11 tests covering:
  - both worked examples from the spec,
  - consecutive terminal punctuation (`...`, `?!`) as a single separator,
  - empty fragments not counted (leading/trailing/whitespace-only separators),
  - no-terminal-punctuation text counts as one sentence,
  - no sentences → `0.0` (and it is a `float`),
  - average word-per-sentence math, float return type on integral results.

## What I did not do
- Did not create or modify `wordfreq.py`, `textnorm.py`, or their tests (owned by other processes).
- Did not touch any `team/` system-management files other than my own two required files (`team/handoffs/sentstats-module.md`, `team/status/sentstats-module.json`).
- Did not create a package directory, CLI, or any non-stdlib import.
- Did not commit or push.
- No cross-module imports: `sentstats.py` imports only `re` from the stdlib.

## Checks I ran and results
Checks were run verbatim from the card's check column, in order, from the repository root:

1. `python -m pytest -q tests/test_sentstats.py` → **PASS** — `11 passed in 0.02s`
2. `python -m pytest -q` → **PASS** — `11 passed in 0.01s`

Note: the environment initially had no `pytest` module (`No module named pytest`). I installed `pytest` (test runner only; it is not imported by any deliverable module — modules use the standard library only) so the required commands could execute. The 11 tests that run are exactly the ones in `tests/test_sentstats.py`; no other test files exist yet in this pre-split round.

## What the validator must pay attention to
- Both card checks pass as written; results above are the actual outputs.
- `average_sentence_length` returns a float in all cases (`0.0` for no sentences; true division elsewhere), satisfying the "返回值为浮点数" requirement.
- Sentence splitting treats any maximal run of `.`/`!`/`?` as one separator, so `Wait... really?! Yes.` yields 3 sentences (fragments `Wait`, ` really`, ` Yes`).
- Fragments that are empty or whitespace-only after the split are discarded (`part.strip()` truthiness), so text like `"...?!."` has 0 sentences and average `0.0`.
- Only `sentstats.py` and `tests/test_sentstats.py` were created by this process, plus the two required team files.
