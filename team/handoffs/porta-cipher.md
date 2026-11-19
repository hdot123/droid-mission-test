# Handoff: porta-cipher (sub-issue #473)

## What was requested

Process card `porta-cipher` under work order #458 (round 45, concurrent D card):
create exactly two new files, `porta.py` and `tests/test_porta.py`, implementing
the Porta cipher (reciprocal table cipher) with:

- `porta_encrypt(text: str, key: str) -> str`
- `porta_decrypt(text: str, key: str) -> str`

Spec (verbatim from the work order): 13 reciprocal tables; key letters select a
row in pairs (A/B -> row 0, C/D -> row 1, ... Y/Z -> row 12); each row maps the
first half A-M onto the second half N-Z (`A+i -> N+((i+n) mod 13)`) and the
second half back to the first (`N+i -> A+((i-n) mod 13)`). The key repeats and
advances only on letters (non-letters do not consume a key position). Output is
uppercased; non-letters preserved as-is. Key must be non-empty and all letters
otherwise `ValueError`; non-`str` inputs raise `TypeError`. Decryption equals
encryption (reciprocal). Every acceptance example needed a corresponding test.

## What I did

- Created `porta.py` (standard library only, no imports of `convexhull`,
  `primorial`, or anything outside the stdlib):
  - `_check_inputs` validates types (`TypeError` for non-`str` text/key) and
    key content (`ValueError` for empty or non-ASCII-alphabetic key).
  - `porta_encrypt` walks the plaintext, advances the key only over ASCII
    letters, computes row `(ord(k) - ord('A')) // 2`, and substitutes via
    `_substitute` implementing the two half-table formulas above.
  - `porta_decrypt` simply delegates to `porta_encrypt` (reciprocal cipher).
  - Non-ASCII letters in the plaintext are treated as non-letters (preserved)
    so substitution never indexes out of range.
- Created `tests/test_porta.py` with one test per acceptance bullet (21 tests):
  single-letter keys A/B/C/Z, full alphabet with key M, the three multi-letter
  examples (LEMON, ZEBRA, KEY), the decrypt example, three roundtrip pairs,
  empty text, `ABC123`, lowercase key `a`, `ValueError` cases (`""`, `"K3Y"`),
  `TypeError` cases (`123`, `5`), plus decrypt-side validation.

## What I did NOT do

- Did not create or touch `convexhull.py`, `primorial.py`,
  `tests/test_convexhull.py`, `tests/test_primorial.py` (owned by other cards).
- Did not modify any pre-existing file (`roman.py`, `legacy_stringkit.py`,
  `tests/test_roman.py`, `tests/test_legacy_stringkit.py`, `README.md`, CI
  config, etc.). Only additions: `porta.py`, `tests/test_porta.py`,
  `team/handoffs/porta-cipher.md`, `team/status/porta-cipher.json`.
- Did not commit or push.

## Checks run and results

- `python3 -m pytest tests/test_porta.py -q` -> `21 passed in 0.03s`
- `python3 -m pytest tests/ -q` -> `32 passed in 0.04s` (11 pre-existing +
  21 new)

Note: `pytest` was not installed in the environment; I installed it with
`pip3 install pytest` (pytest 9.2.0) to run the required checks. No project
files were affected.

## Notes for the validator

- The key-row derivation is integer division by 2 on the key letter's
  0-based index, which is exactly the specified A/B, C/D, ... pairing; do not
  "simplify" it to a letter-pair lookup with different indexing.
- Key advancement is per plaintext *letter* only; `porta_encrypt("HELLO WORLD",
  "KEY")` reuses `K` for the letter after the space (space does not consume a
  key position) — the expected `"ZTXQM KJCXV"` depends on this.
- `isalpha()` alone would accept non-ASCII letters and could index out of
  range, so the implementation requires `isascii() and isalpha()` for both key
  validation and plaintext letter detection; this is intentional hardening, not
  a spec change (all spec examples are ASCII).
- Non-letter characters in the ciphertext output are preserved verbatim and are
  not uppercased (e.g. `ABC123` -> `NOP123`).
