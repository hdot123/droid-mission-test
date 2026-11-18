# Handoff: affine-cipher (sub-issue #421)

## What was requested

Process card `affine-cipher` under work order #408 (round 43 · concurrent B). Owns exactly two new files:

- `affine.py` — affine cipher mod 26:
  - `encode(text: str, a: int, b: int) -> str` applies `E(x) = (a*x + b) mod 26` to letters only.
  - `decode(text: str, a: int, b: int) -> str` is the inverse operation.
  - Preserve original case; non-letters pass through unchanged.
  - When `a` is not coprime with 26, both `encode` and `decode` must raise `ValueError`.
  - Standard library only; must not import `beaufort` or `polybius`.
- `tests/test_affine.py` — one dedicated test case per acceptance item, verbatim:
  1. `encode("Affine", 5, 8) == "Ihhwvc"`
  2. `decode("Ihhwvc", 5, 8) == "Affine"`
  3. `encode("abc", 1, 0) == "abc"`
  4. `encode("Hello", 25, 3) == "Wzssp"`
  5. `decode("Wzssp", 25, 3) == "Hello"`
  6. `encode("Hi", 2, 0)` raises `ValueError`
  7. `decode("Hi", 2, 0)` raises `ValueError`
  8. round-trip identity on `"Secret message"` with `a=7`, `b=11`

## What I did

- Created `affine.py` (new file): `encode`/`decode` implemented via a shared `_transform` helper. `gcd(a, 26) != 1` is checked first in both entry points so both raise `ValueError` for non-coprime `a`. `decode` inverts with `pow(a, -1, 26)` and `(-a_inv * b) % 26`. Case is preserved by working from `A`/`a` bases; only ASCII letters are transformed, everything else passes through untouched.
- Created `tests/test_affine.py` (new file): 8 tests, one per acceptance item above (both ValueError cases use `pytest.raises(ValueError)`).
- Installed `pytest` into the environment (`python3 -m pip install pytest`) because it was missing; this did not touch repository files.

## What I did not do

- Did not touch `beaufort.py`, `polybius.py`, or any other process's files.
- Did not modify any existing file (no changes to `roman.py`, `legacy_stringkit.py`, existing tests, or repo config).
- Did not add cross-module imports; `affine.py` imports only `math.gcd` from the standard library.
- Did not commit or push.

## Checks run and results

- `python3 -m pytest tests/test_affine.py -q` → **8 passed** (exit 0).
- `python3 -m pytest tests/ -q` → **19 passed** (exit 0), covering the pre-existing `test_roman.py` and `test_legacy_stringkit.py` suites alongside the 8 new affine tests.

## Notes for the validator

- The only pre-existing test-file count is 11 tests (19 total − 8 new); all pre-existing tests still pass, confirming no existing file was broken or modified.
- Expected validator output: `tests/test_affine.py` shows 8 passed; full suite shows 19 passed. Counts will rise as `beaufort` and `polybius` processes land their own tests; that is expected and not a regression.
- `decode` re-validates `a` before computing the inverse, so the ValueError guarantee holds even though the failure could otherwise be masked.
