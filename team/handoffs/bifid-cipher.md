# Handoff — bifid-cipher (sub-issue #741)

## What was requested

Process card `bifid-cipher` under work order #729 (fifty-first round C, concurrent card C):
implement `bifid.py` and `tests/test_bifid.py` only, adding exactly those two repository
files, never modifying any pre-existing file. Scope:

- 5x5 Polybius square pinned to `ABCDEFGHIKLMNOPQRSTUVWXYZ` (25 letters, no J; J folds
  into I), row-major fill: cell (r, c) with r, c in 1..5 is alphabet index
  `(r-1)*5 + (c-1)` (0-based).
- `bifid_encrypt(text: str, period: int = 5) -> str`: preprocess (uppercase, J -> I, keep
  only alphabet characters), group by `period` (last group may be shorter), per group write
  all row coordinates then all column coordinates into one digit string, split into
  (row, column) pairs, map back to characters. Empty string -> empty string.
- `bifid_decrypt(cipher: str, period: int = 5) -> str`: inverse — per group write each
  character's two coordinates as a digit string, first half is the row-coordinate column,
  second half the column-coordinate column, paired digit-by-digit; returns the preprocessed
  plaintext (folded I included). Empty string -> empty string.
- Validation: `period` non-int raises TypeError (bools rejected as non-integers), `<= 0`
  raises ValueError; `text` non-str raises TypeError.
- Standard library only; no imports from other project modules (partitions, rotate2d,
  legacy_stringkit, roman, etc.).
- One test case per acceptance item (14 items), none dropped.

## What I did

1. `bifid.py` (new): `ALPHABET` constant, `_SQUARE` letter -> (row, col) lookup built at
   import, `_validate_period` (TypeError on non-int/bool, ValueError on <= 0),
   `_prepare` (uppercase, J -> I, filter to alphabet, TypeError on non-str), then
   `bifid_encrypt` and `bifid_decrypt` exactly as specified. Empty prepared input returns
   `""` in both. No project-module imports.
2. `tests/test_bifid.py` (new): 14 tests, one per acceptance item —
   `test_encrypt_hello`, `test_decrypt_fnnvd`, `test_encrypt_single_letter`,
   `test_encrypt_empty`, `test_encrypt_j_folds_into_i`, `test_encrypt_jump`,
   `test_encrypt_cryptography_period_6`, `test_encrypt_helloworld_period_3`,
   `test_roundtrip_thequickbrownfox`, `test_roundtrip_attackatdawn`,
   `test_period_changes_result`, `test_period_zero_raises_value_error`,
   `test_period_non_int_raises_type_error`, `test_text_non_str_raises_type_error`.
3. Also wrote this handoff and `team/status/bifid-cipher.json` as required by the worker
   instructions.

## What I did NOT do

- Did not create or touch `partitions.py`, `rotate2d.py`, `tests/test_partitions.py`,
  `tests/test_rotate2d.py` (owned by sibling processes C-partitions / C-rotate2d).
- Did not modify any pre-existing repository file (no edits to `roman.py`,
  `legacy_stringkit.py`, existing tests, config, or docs).
- Did not commit or push.
- No scope beyond the two deliverables + the two team files above.

## Checks run and results

Environment note: system `python3` had no pytest and there was no project venv, so I ran
`python3 -m pip install "pytest>=7.4.0"` (satisfies `requirements-dev.txt`) to execute the
mandated checks.

- `python3 -m pytest tests/test_bifid.py -q` -> **14 passed in 0.02s** (exit 0)
- `python3 -m pytest tests/ -q` -> **117 passed in 3.12s** (exit 0)

Both mandated checks pass; the full suite (existing 103 tests + my 14) is green.

## What the validator must pay attention to

- The 14 acceptance vectors are each covered by exactly one test; roundtrip cases use
  (t, p) = ("THEQUICKBROWNFOX", 5) and ("ATTACKATDAWN", 4) as specified.
- `bifid_encrypt(42, 5)` raises TypeError via the text check; `bifid_encrypt("ABC", "5")`
  raises TypeError via the period check (bools such as `True` are also rejected as
  non-int period, consistent with "positive int").
- The decrypt returns the *preprocessed* plaintext: inputs containing J or lowercase
  letters come back uppercase with J folded to I, per spec ("返回制备后的明文").
- Only these files were added: `bifid.py`, `tests/test_bifid.py`,
  `team/handoffs/bifid-cipher.md`, `team/status/bifid-cipher.json`. Nothing pre-existing
  was modified.
