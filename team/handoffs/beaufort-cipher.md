# Handoff: beaufort-cipher (sub-issue #420)

## What was requested

Process card for work order #408 (round 43 · batch B): implement only the Beaufort component of three independent classical-cipher widgets.

- Create `beaufort.py` (new file only) exposing `beaufort(text: str, key: str) -> str`:
  - Beaufort rule `(key_letter - plain_letter) mod 26` on letters.
  - Key cycles over the letters of the text; key/plain comparison case-insensitive.
  - Preserve original letter case; non-letters pass through unchanged.
  - Raise `ValueError` when `key` is the empty string.
  - Standard library only; no imports from `affine` or `polybius`.
- Create `tests/test_beaufort.py` (new file only) with a dedicated test case per acceptance item, verbatim:
  1. `beaufort("Hello", "key") == "Danzq"`
  2. `beaufort("ATTACK AT DAWN", "lemon") == "LLTOLB ET LNPR"`
  3. `beaufort("", "k") == ""`
  4. `beaufort("123", "k") == "123"`
  5. `beaufort("Hello, World!", "key") == "Danzq, Cwnnh!"`
  6. round-trip identity on `"Hello, World!"` with key `"key"` (self-inverse)
  7. `beaufort("Hi", "")` raises `ValueError`

## What I did

- Implemented `beaufort(text, key)` in `beaufort.py`:
  - Empty key raises `ValueError` up front.
  - The key index advances only when a letter is consumed (non-letters do not consume key), so key cycling is over letters only, per the "key cycles over the text ... letters" spec.
  - Case of the input letter is preserved; non-letters pass through unchanged.
  - Standard library only (uses `ord`/`chr`/`isalpha`/`isupper`); imports nothing from other repo modules.
- Implemented `tests/test_beaufort.py` with exactly seven test functions, one per acceptance item above (round-trip test applies `beaufort` twice and asserts identity).

## What I did not do

- Did not touch `affine.py`, `polybius.py`, `tests/test_affine.py`, `tests/test_polybius.py`, or any other existing file (only the two owned files plus the two required team files were created).
- Did not import or depend on any other module in the repo.
- Did not commit or push.
- Did not implement the affine or polybius process cards (owned by other workers).

## Checks run and results

1. `python3 -m pytest tests/test_beaufort.py -q` → **7 passed** (exit 0).
2. `python3 -m pytest tests/ -q` → **18 passed** (exit 0), covering the whole suite (baseline roman/legacy tests + my 7).

Note: `pytest` was not installed in the environment initially; I installed it via `python3 -m pip install pytest` (pytest 9.2.0) before running checks. No repository files were changed by that install.

## What the validator must pay attention to

- Key-cycling semantics: the key advances only on letters. For `"ATTACK AT DAWN"` (11 letters) with `"lemon"` the key wraps as expected; spaces do not consume key. This matches the acceptance vector `LLTOLB ET LNPR`.
- Case preservation: only the letter's case from the input is preserved; the key's case is ignored (`ord(ch.lower())`).
- Self-inverse property: applying `beaufort` twice with the same key returns the original; the round-trip test asserts this.
- `ValueError` is raised only for an empty key; other falsy inputs are out of scope per spec.
- All seven acceptance items have dedicated, individually named test functions in `tests/test_beaufort.py`.
