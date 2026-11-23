# Handoff: pluralize (sub-issue #827)

## What was requested

Work order #814, round-54 concurrent C card: implement `pluralize(word) -> str` in a new `pluralize.py`, plus `tests/test_pluralize.py` covering every acceptance item. New files only; no existing file may be modified. Standard library only; no import of `ellipse` or `issn`.

Pinned spec:
- Non-`str` input raises `TypeError`; empty string or any character outside lowercase `a-z` raises `ValueError`.
- Rules applied in pinned order, first match wins:
  1. uncountable `{sheep, fish, deer, species, series, aircraft}` returned unchanged;
  2. irregular table (`child`→`children`, `person`→`people`, `man`→`men`, `woman`→`women`, `mouse`→`mice`, `goose`→`geese`, `tooth`→`teeth`, `foot`→`feet`, `ox`→`oxen`, `die`→`dice`, `quiz`→`quizzes`);
  3. f/fe→ves list `{leaf, life, knife, wife, wolf, loaf, thief, shelf, half, calf}` (fe drops `fe`, f drops `f`, add `ves`);
  4. o→es list `{hero, potato, tomato, echo, torpedo, veto}`;
  5. consonant + y → drop `y`, add `ies` (vowel + y does not take this rule);
  6. ends in `s`, `x`, `z`, `ch`, `sh` → add `es`;
  7. otherwise add `s`.

## What I did

- Created `pluralize.py` implementing the above exactly, with the three rule sets and irregular table as module-level frozensets/dicts, and a single `pluralize()` function. Guard `len(word) >= 2` before the consonant+y rule so a bare `"y"` falls through to rule 7 (`"ys"`) instead of indexing `word[-2]` (which would raise `IndexError`); `"y"` is not in any acceptance list, and this is the only deviation needed to keep the function total over all validated inputs.
- Created `tests/test_pluralize.py` with one test function per acceptance item (35 tests): all 31 positive cases, plus `""` / `"Cat"` / `"cat!"` → `ValueError`, and `None` / `3` → `TypeError`.

## What I did not do

- Did not create or touch `ellipse.py`, `issn.py`, or their tests (other cards own those).
- Did not modify any pre-existing file (`roman.py`, `legacy_stringkit.py`, existing tests, docs, schemas, scripts, etc.).
- Did not commit or push.
- Did not implement or verify anything from the round-level acceptance list (a–j): this card owns only the pluralize implementation itself.

## Checks run and results

- `python3 -m pytest tests/test_pluralize.py -q` → `35 passed in 0.03s`
- `python3 -m pytest tests/ -q` → `222 passed, 2 skipped in 15.42s`

Note: `pytest` was not installed in the environment; I installed it via `pip3 install pytest` (pytest 9.2.0) to run the checks. No `verdict.json` / `verdict.md` by-products were produced; `git status` shows only `pluralize.py`, `tests/test_pluralize.py` (plus the pre-existing untracked `worker-prompt.txt` / `worker-stream.jsonl`, untouched) and the new `team/` files.

## What the validator must pay attention to

- Rule order is load-bearing: uncountable → irregular → f/fe → o→es → consonant+y → sibilant → default. In particular `fish` must stay `fish` (rule 1, not rule 6 `s`→`es`), `quiz`→`quizzes` (rule 2, not rule 6), `echo`→`echoes` (rule 4, not rule 6), and `day`/`boy`/`toy`/`key` keep `y` (vowel+y skips rule 5).
- `roof` → `roofs` (not in the f/fe list, rule 7), `photo` → `photos`, `piano` → `pianos` (not in the o→es list, rule 7).
- Validation raises before any rule runs: `Cat`, `cat!`, `""` all `ValueError`; `None`, `3` all `TypeError`. Non-ASCII letters (e.g. `"café"`) also raise `ValueError` per the a–z-only rule.
- The bare `"y"` case is not in the acceptance list; handled as rule 7 (`"ys"`) via a length guard rather than crashing.
