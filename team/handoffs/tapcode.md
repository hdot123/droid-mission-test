# Handoff: tapcode (sub-issue #772)

## What was requested

Work order #763, process card "tapcode": implement the Tap code component (5x5 grid, C/K merged) in exactly two new files — `tapcode.py` and `tests/test_tapcode.py` — to the verbatim spec in the card. No other files were to be created or modified as part of the deliverable (the two team files below were additionally required by the workflow instructions).

## What I did

- Created `tapcode.py`:
  - Fixed 5x5 table as the string `ABCDEFGHIJLMNOPQRSTUVWXYZ` (row-major, rows/columns 1-based, no K).
  - `tapcode_encode(text: str) -> list[tuple[int, int]]`: raises TypeError on non-str; uppercases, keeps only A–Z; K is mapped to C (coordinate (1, 3)); empty string returns `[]`.
  - `tapcode_decode(pairs) -> str`: pairs must be list/tuple (str rejected → TypeError); each item must be a 2-element list/tuple else TypeError; coordinates must be int with bool rejected (TypeError) and within 1–5 (else ValueError); empty input returns `""`; (1, 3) decodes to "C".
  - Standard library only; no imports of `bell`, `decimaltime`, or anything else.
- Created `tests/test_tapcode.py` with a test case for every acceptance example in the card (7 encode value cases, 3 decode value cases, 2 round-trips, 3 ValueError cases, 4 TypeError cases), using `pytest.raises` for the error cases.

## What I did not do

- Did not touch `bell.py`, `decimaltime.py`, or any other existing file.
- Did not import from the other two modules.
- Did not commit or push.
- Did not create or modify `tests/test_bell.py` (owned by the parallel bell worker).

## Checks run and results

1. `python3 -m pytest tests/test_tapcode.py -q` → **13 passed** (my module's own tests).
2. `python3 -m pytest tests/test_bell.py -q` → **ERROR: file or directory not found: tests/test_bell.py**. This check is listed verbatim in my card, but `tests/test_bell.py` is owned by the parallel bell worker and does not exist yet in the working tree. I did not create it (out of my scope). Re-run this check after the bell worker's files land.
3. `python3 -m pytest tests/ -q` → **150 passed, 1 skipped in 15.63s** (includes my 13 tapcode tests; pre-existing suite green).

Note: `pytest` was not installed in the environment; I installed it via `python3 -m pip install -r requirements-dev.txt` (pytest>=7.4.0, jsonschema>=4.20.0), which does not modify any tracked file.

## What the validator must pay attention to

- C/K merge direction: encoding `K` yields `(1, 3)` and decoding `(1, 3)` yields `"C"` — the table itself never produces `K`.
- Truncation/range semantics do not apply here; the only range rule is coordinates 1–5 → ValueError, everything malformed → TypeError, and `bool` is rejected as a coordinate (`isinstance(x, int)` alone would accept `True`, so an explicit `isinstance(x, bool)` guard is in place).
- `tapcode_decode("13")` must be TypeError because `str` is not a list/tuple, even though it is iterable.
- The check `python3 -m pytest tests/test_bell.py -q` will fail until the bell worker delivers `tests/test_bell.py`; that is a cross-worker ordering artifact, not a tapcode defect.
