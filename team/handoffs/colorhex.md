# Handoff: colorhex (sub-issue #362)

## What was requested
Process card #362 under work order #346 (round 40 · concurrency C): implement `colorhex.py` — a hex color parser/formatter — plus `tests/test_colorhex.py`, new files only, standard library only, no imports from other project modules (`bytesize`/`rangemerge` are out of scope).

Spec (verbatim from the work order):
- `parse(text: str) -> tuple[int, int, int]`: accepts `"#RGB"` and `"#RRGGBB"` (hex digits case-insensitive); the short form expands each digit to two (e.g. `#f80`'s f becomes FF); missing `#`, wrong length, or non-hex characters raise `ValueError`.
- `format(r: int, g: int, b: int) -> str`: inverse operation, outputs uppercase `"#RRGGBB"`; any channel outside 0–255 raises `ValueError`.

Every acceptance item has a corresponding test:
- `parse("#FF8000") == (255, 128, 0)`; `parse("#f80") == (255, 136, 0)`; `parse("#000000") == (0, 0, 0)`; `parse("#fff") == (255, 255, 255)`; `parse("#123456") == (18, 52, 86)`
- `format(255, 128, 0) == "#FF8000"`; `format(0, 0, 0) == "#000000"`; `format(18, 52, 86) == "#123456"`
- `parse("FF8000")` and `parse("#FF80")` raise `ValueError`
- `format(256, 0, 0)` raises `ValueError`
- round trip: `parse(format(18, 52, 86)) == (18, 52, 86)`

## What I did
- Created `colorhex.py` with `parse` and `format` as specified. `parse` validates the leading `#`, expands the 3-digit form, enforces exactly 6 hex digits, and double-checks every character is a hex digit (since `int(body, 16)` alone would accept whitespace/signs). `format` validates each channel is an `int` in 0–255 (rejecting `bool`) and emits uppercase `#RRGGBB`.
- Created `tests/test_colorhex.py` with 6 tests covering all acceptance items above plus extra negative cases (empty string, bare `#`, non-hex letters, spaces, out-of-range/negative channels, and round trips for several triples).

## What I did not do
- Did not create or touch `bytesize.py`, `rangemerge.py`, or their tests (owned by other processes).
- Did not modify any pre-existing file (only the two owned source/test files were added).
- Did not commit or push.

## Checks run
From the repository root:
- `python3 -m pytest tests/test_colorhex.py -q` → `6 passed in 0.02s`
- `python3 -m pytest tests/ -q` → `17 passed in 0.03s` (full suite at time of writing: colorhex 6 + roman 6 + legacy_stringkit 5)

Note: `pytest` was not installed in the environment, so I installed it with `python3 -m pip install pytest` (pytest 9.2.0) before running the checks. That is an environment change, not a repository change.

## For the validator
- The two acceptance `ValueError` parses are `parse("FF8000")` (missing `#`) and `parse("#FF80")` (wrong length); both are covered.
- `parse` intentionally rejects anything that is not exactly `#` + 3 or 6 hex digits; `format` rejects non-int channels (e.g. `256.0` or `True`) as well as out-of-range ints.
- After the other two processes land, re-run `python3 -m pytest tests/ -q` for the merged-suite acceptance; nothing in this module depends on their files.
