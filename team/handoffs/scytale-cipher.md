# Handoff: scytale-cipher (sub-issue #436)

## What was requested

Implement the Spartan scytale transposition cipher per work order #430 (round 44 · item B), owning exactly two new files:

- `scytale.py` with `scytale_encrypt(text: str, circ: int) -> str` and `scytale_decrypt(cipher: str, circ: int) -> str`
- `tests/test_scytale.py` with a test case for every acceptance item

Constraints: only new files (no edits to existing files), standard library only, no imports of other deliverables (murmur3 / fiscal).

## What I did

- Created `scytale.py`:
  - `scytale_encrypt`: validates `text` is `str` (else `TypeError`) and `circ` is a positive `int` (else `ValueError`, covering 0 and negatives); empty string returns `""`. Otherwise pads the plaintext with `X` up to a multiple of `circ`, lays it out row by row into `circ` columns, and reads column by column to produce the ciphertext.
  - `scytale_decrypt`: same type/circ validation; empty string returns `""`; raises `ValueError` if `len(cipher)` is not a multiple of `circ`. Fills the ciphertext column by column and reads row by row, returning the padded plaintext with `X` padding left in (not stripped), per spec.
  - Non-`str` input raises `TypeError` before circ validation; a bool `circ` is treated as invalid (`ValueError`) since `bool` is an `int` subclass.
- Created `tests/test_scytale.py` with 18 tests covering every acceptance item: all three known ciphertext vectors, circ=1, exact-multiple case, empty string (both directions), all `ValueError` cases (circ 0 / -2 on encrypt; circ 0 / -2 and non-multiple length on decrypt), `TypeError` for `scytale_encrypt(123, 3)` and `scytale_decrypt(123, 3)`, plus a round-trip test asserting decrypt returns the *padded* plaintext.

## What I did not do

- Did not create or modify `murmur3.py`, `fiscal.py`, or their tests (other process cards own those).
- Did not modify any pre-existing file (`legacy_stringkit.py`, `roman.py`, existing tests, README, etc.).
- Did not commit or push (workflow handles that).

## Checks run

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_scytale.py -q` | 18 passed |
| `python3 -m pytest tests/ -q` | 29 passed |

Note: `pytest` was not initially installed in the environment; I installed it with `python3 -m pip install pytest` (no repo files changed).

## Validator attention points

- Spec detail: `scytale_decrypt` intentionally does **not** strip `X` padding — `scytale_decrypt("HLEOLX", 3) == "HELLOX"`, not `"HELLO"`. My round-trip test asserts the padded result.
- `circ` validation raises `ValueError` (not `TypeError`) for non-positive values; non-`str` text/cipher raises `TypeError`. Type check on the text argument runs before circ validation.
- `circ=1` and exact-multiple inputs produce output equal to input (no padding needed).
