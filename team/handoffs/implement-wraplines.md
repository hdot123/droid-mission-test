# Handoff: implement-wraplines (sub-issue #171)

## What was requested
Process card `implement-wraplines` for work order #159 (第二十六轮 C 单 · 并发加压组): implement `wraplines.py` with `wrap(text, width)` and `tests/test_wraplines.py`. Scope owned: `wraplines.py` and `tests/test_wraplines.py` only.

## What I did
- Created `wraplines.py` with a single function `wrap(text, width)`:
  - Splits on any whitespace (`text.split()`).
  - Greedy placement: adds each word to the current line with a single space between words; if appending would exceed `width`, starts a new line (`len(current) + 1 + len(word) <= width`).
  - A word longer than `width` stands alone on its own line (over-length allowed).
  - Empty or whitespace-only text returns `[]`.
  - No imports of `stack` or `duration`; standard library only; no CLI, no package directory.
- Created `tests/test_wraplines.py` with 8 tests covering both body examples (`wrap("the quick brown fox", 10)` → `["the quick", "brown fox"]`, `wrap("aaa bb", 3)` → `["aaa", "bb"]`), the greedy rule, the over-length single-word case, empty input, whitespace-only input, exact-width fit, and multi-whitespace normalization. The test file imports only `wraplines`.

## What I did not do
- Did not touch `stack.py`, `duration.py`, or any other test files.
- Did not touch `team/` paths other than my own two files, nor `.github/`.
- Did not commit or push.

## Checks run
- `python -m pytest -q tests/test_wraplines.py` (from repository root) — **passed**: `8 passed in 0.02s` (exit code 0).
- Note: the environment initially lacked pytest; I installed it with `python3 -m pip install --quiet pytest` (pytest 9.2.0) so the mandated check command could run. No other environment changes.

## What the validator must pay attention to
- The check command `python -m pytest -q tests/test_wraplines.py` was run verbatim from the repository root; its real output is the `8 passed` line above.
- `wrap` semantics: over-length words are allowed to exceed `width` when they stand alone; lines with only one word are exempt from the width check.
- Full-suite acceptance (`python -m pytest -q` from the repo root) depends on the other processes' modules/tests; this card only guarantees its own check passes.
