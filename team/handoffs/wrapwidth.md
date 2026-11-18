# Handoff: wrapwidth (sub-issue #229)

## What was requested
Implement the standalone module `wrapwidth.py` (Python standard library only; no imports of other project modules; no package directory; no CLI) exposing two functions, plus `tests/test_wrapwidth.py` that tests only this module's behavior:

1. `wrap(text, width)` — split text on any whitespace, rejoin words with single spaces, greedily pack words so no line exceeds `width` chars; a single word longer than `width` gets its own unbroken line (may exceed `width`); empty/all-whitespace text returns `[]`; non-positive-integer `width` raises `ValueError`.
2. `justify(line, width)` — pad a single-space-separated line to exactly `width` by distributing extra spaces evenly across gaps (base share first, remainder adds one space per gap left to right); line already at least `width` long, or a single-word line, returned unchanged; non-positive-integer `width` raises `ValueError`.

## What I did
- Created `wrapwidth.py` with `wrap` and `justify` (plus a private `_check_width` guard that rejects bools, non-ints, and non-positive ints with `ValueError`).
- Created `tests/test_wrapwidth.py` covering: both worked examples for each function; empty text; whitespace-only text; overlong single word unbroken; multi-whitespace splitting; exact-width words; greedy packing; long word mid-line; remainder distribution left-to-right; even split with no remainder; already-long and exactly-long lines; single-word lines; output length check; and invalid widths (0, negatives, floats, strings, None, True) for both functions.

## What I did not do
- Did not create or modify `duration_parse.py`, `bitflags.py`, any other test file, or anything under `team/` other than this handoff and `team/status/wrapwidth.json`.
- Did not create a package directory or CLI; did not import other project modules.
- Did not commit or push.

## Checks run and results
- `python -m pytest -q tests/test_wrapwidth.py` — all tests passed (see status JSON for the recorded result).

## Notes for the validator
- `wrap` uses `str.split()` (splits on any whitespace) and joins with single spaces, matching spec.
- `justify` treats the input as words separated by single spaces (`line.split(" ")`); it returns the input unchanged when there is only one word or the line is already `>= width`. It validates `width` before those early returns, so invalid width still raises `ValueError` even for single-word/long lines.
- `bool` is rejected as a width because `isinstance(True, int)` is `True` in Python; the spec requires a positive integer width.
- Tests import `wrapwidth` at module level; the check command is run from the repo root so `wrapwidth.py` is importable.
