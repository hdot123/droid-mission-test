# Handoff: iban-module (sub-issue #168)

## What was requested
Process card `iban-module` under work order #160 (round 26, group D):
- Implement `iban.py` with `is_valid(iban)` performing IBAN mod-97 validation:
  strip spaces, upper-case, move first 4 characters to end, expand letters
  A=10..Z=35 to digits, valid iff the resulting number mod 97 == 1.
- Characters other than letters/digits (after space stripping) → return `False`,
  never raise. Do not validate length or country code.
- Worked examples that must hold:
  - `is_valid("GB29 NWBK 6016 1331 9268 19")` → `True`
  - `is_valid("GB29 NWBK 6016 1331 9268 18")` → `False`
- Attach `tests/test_iban.py` covering only this module.
- Constraints: Python stdlib only; no package directories; no CLI.

## What I did
- Created `iban.py` with `is_valid(iban)` exactly per spec (stdlib only,
  no imports of other project modules). Non-`str` input also returns `False`
  defensively instead of raising.
- Created `tests/test_iban.py` with 5 tests covering only `iban.py`:
  the two worked GB examples, space/case insensitivity, invalid characters /
  empty string returning `False` (no exception), and an extra valid/invalid
  DE IBAN pair.

## What I did not do
- Did not touch `transpose.py`, `versioncmp.py`, or any other process's files.
- No package directories, no CLI, no non-stdlib dependencies.
- Did not commit or push (left to the workflow).

## Checks run and results
- `python -m pytest -q tests/test_iban.py` → **5 passed in 0.01s** (exit 0).
  This is the card's check, run verbatim.
- Note: pytest was not preinstalled in the environment; I installed it via
  `python -m pip install pytest` (pytest 9.2.0) so the check could run. This
  is environment setup only, not a repo change.

## For the validator
- Both required files exist at repo root: `iban.py`, `tests/test_iban.py`.
- The worked GB examples are covered directly by
  `test_valid_gb_iban` / `test_invalid_gb_iban_checksum`.
- Full-suite command `python -m pytest -q` also passes (this process only
  owns its own check; the full suite is validated by the foreman).
