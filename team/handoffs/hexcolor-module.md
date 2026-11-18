# Handoff: hexcolor-module (sub-issue #211)

## What was requested
Process card #211 under work order #204 (round 29, unit C). Scope limited to:

- `hexcolor.py` at repo root:
  - `parse(color)` accepting `"#RGB"` and `"#RRGGBB"` (hex letters case-insensitive); the 3-digit form repeats each digit once to expand to 6 digits; returns `(r, g, b)` int tuple. Raises `ValueError` for missing `#`, wrong length (not 3 or 6 hex digits), or non-hex characters.
  - `to_hex(r, g, b)` returns lowercase `"#rrggbb"`; raises `ValueError` if any component is not an int in 0–255.
  - Spec examples: `parse("#FF8000") -> (255, 128, 0)`, `parse("#f80") -> (255, 136, 0)`, `parse("#0a1B2c") -> (10, 27, 44)`, `to_hex(255, 128, 0) -> "#ff8000"`, `to_hex(0, 0, 0) -> "#000000"`.
- `tests/test_hexcolor.py`: tests this module only; must cover all spec examples plus boundaries (missing `#`, lengths 1/2/4/5/7, non-hex chars, mixed case, components 256/-1, non-int components raising `ValueError`).
- Constraints: Python stdlib only; no import of `ipv4` or `morse`; no package directory; no CLI.

## What I did
- Created `hexcolor.py` with `parse` and `to_hex` exactly per spec. Validation is strict: non-string input, missing `#`, length not in {3, 6} after `#`, any non-hex char, and for `to_hex` any non-int (bools excluded) or out-of-range component all raise `ValueError`. No sibling-module imports; stdlib only (no imports at all).
- Created `tests/test_hexcolor.py` with 44 tests covering: all five spec examples, black/white/shorthand-uppercase, int-tuple return type, missing `#` (4 cases), bad lengths `#`, `#F`, `#FF`, `#FFFF`, `#FFFFF`, `#FFFFFFF` (covers required lengths 1/2/4/5/7), non-hex characters (6 cases), mixed case, `to_hex` output/bounds, components 256/300 and -1, non-int components (str, float, None), and parse→to_hex round trips (shorthand `#f80` correctly round-trips to `#ff8800`, since expansion is lossy).

## What I did not do
- Did not create or modify `ipv4.py`, `morse.py`, their tests, or any other repo file.
- Did not create a package directory, CLI, or add any cross-module import.
- Did not commit or push.

## Checks ran and results (commands verbatim from the card's check list)
1. `python -m pytest -q tests/test_hexcolor.py` → initially FAILED once due to an error in my own round-trip test (asserted `#f80` round-trips to `#ff8000`; correct expansion is `#ff8800`). Fixed the test expectation (module code was already correct per spec). Rerun → `44 passed in 0.04s` (exit 0).
2. `python -m pytest -q` → `48 passed in 0.05s` (exit 0).

Environment note: the base image had no `pytest` module; I installed it via `python -m pip install pytest` (pytest 9.2.0) so the mandated check commands could run. This is an environment setup step, not a repo change.

## What the validator must pay attention to
- The required expansion semantics: `parse("#f80") == (255, 136, 0)` and therefore `to_hex(*parse("#f80")) == "#ff8800"`. A round-trip test asserting `#f80 -> #f80` would be wrong.
- `to_hex` rejects bools as non-int components (`isinstance(True, int)` is True in Python, so an explicit bool guard is present); this is stricter than the literal wording but consistent with "must be an integer in 0–255".
- Both card checks pass as written: `python -m pytest -q tests/test_hexcolor.py` (44 passed) and `python -m pytest -q` (48 passed, includes other processes' tests already in the repo).
