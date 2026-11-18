# Handoff: polybius-square (sub-issue #422)

## What was requested

Process card `polybius-square` under work order #408 (round 43 · batch B): implement the Polybius square component, owning only `polybius.py` and `tests/test_polybius.py`.

Spec (verbatim from the card):

- 5×5 square built by placing keyword `MONARCHY` first (J treated as I), then the remaining letters of A–Z (no J) in alphabetical order; coordinates are `(row, column)`, both 1-based.
- `encode(text: str) -> str`: process letters only (case-insensitive, `J` → `I`), output coordinate pairs as two digits `RC` separated by a single space; return `""` when there are no letters.
- `decode(text: str) -> str`: restore an uppercase letter string from the coordinate-pair sequence; raise `ValueError` on non-digit characters, odd-length input, or out-of-range coordinates.
- Standard library only; must not import `beaufort` or `affine`.
- A dedicated test case for every acceptance item: (1) `encode("hello") == "22 31 41 41 12"`; (2) `decode("22 31 41 41 12") == "HELLO"`; (3) `encode("Jupiter") == "34 51 42 34 45 31 15"`; (4) `encode("") == ""`; (5) `encode("123") == ""`; (6) `decode("99")` raises `ValueError`; (7) round-trip on `"POLYBIUS"` with encode output `"42 12 41 23 24 34 51 44"`.

## What I did

- Created `polybius.py` (new file): builds the square once at import (keyword `MONARCHY` deduped with J→I, then remaining letters A–Z without J), derives a position map, and implements `encode` / `decode` per spec. `decode` strips whitespace before validation, then checks odd length, non-digit characters, and 1-based row/col bounds (each raises `ValueError`).
- Created `tests/test_polybius.py` (new file): seven tests, one dedicated test per acceptance item, modeled on the existing test style in `tests/test_roman.py`.
- Installed `pytest` via `python3 -m pip install pytest` (it was not present in the environment; the checks could not run otherwise). No repository files were touched for this.

## What I did not do

- Did not create or modify `beaufort.py`, `affine.py`, or their tests (owned by other processes).
- Did not modify any existing file (`README.md`, `roman.py`, `legacy_stringkit.py`, existing tests).
- No cross-module imports; only the standard library plus `pytest` in tests.
- Did not commit or push.

## Checks run and results

| Command | Result |
|---|---|
| `python3 -m pytest tests/test_polybius.py -q` | PASS — 7 passed |
| `python3 -m pytest tests/ -q` | PASS — 18 passed (7 new + 11 pre-existing) |
| Extra acceptance script (all 7 items + error cases `99`, `9`, `1a`, `56`, `2`) | PASS — "acceptance OK" |

## Notes for the validator

- Decode input with internal whitespace (e.g. `"22 31 41 41 12"`) is accepted; whitespace is stripped before validation. Strict per-pair space formatting is only guaranteed on `encode` output.
- Error precedence in `decode`: odd length is checked before the digit check, so `"2"` (odd, and would be a single digit) raises on odd-length; `"99"` (even, digits, out of range) raises on range; `"1a"` raises on non-digit.
- J and I share a cell: both encode to the same coordinate, and decode maps that cell to `I` only (no way to distinguish, per spec).
- `pytest` was missing from the environment and installed with pip; if the validator runs in a fresh environment, it needs pytest available to run the checks.
