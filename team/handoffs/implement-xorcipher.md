# Handoff: implement-xorcipher (sub-issue #493)

## What was requested

Process card `implement-xorcipher` from work order #480 (round 46 · C): implement `xorcipher.py`
(repeating-key XOR, hex in/out) plus `tests/test_xorcipher.py`, standard library only, covering every
acceptance item verbatim. Scope owned: `xorcipher.py` and `tests/test_xorcipher.py` only.

## What I did

- Created `xorcipher.py` with:
  - `xor_encrypt_hex(plaintext, key) -> str`: validates inputs (`TypeError` for non-str, `ValueError`
    for empty key), UTF-8 encodes both sides, cycles key bytes, XORs byte-by-byte, returns
    `bytes.hex()` (lowercase).
  - `xor_decrypt_hex(hexstr, key) -> str`: same key validation; rejects odd-length hex and invalid
    hex characters with `ValueError`, `bytes.fromhex` for decoding, XORs with the cycled key,
    UTF-8 decodes to the plaintext.
- Created `tests/test_xorcipher.py` with 14 test cases covering every acceptance item:
  hello/key encrypt+decrypt, empty plaintext/hex, single char `"A"`/`"k"`, Hello-World
  encrypt+decrypt, both round trips (unicode `café ☕` and single-byte key `x`), empty-key
  `ValueError` on encrypt and decrypt, invalid hex (`"zz"`, `"abc"`) `ValueError`, non-str
  `TypeError` for both plaintext and key on encrypt, and non-str `TypeError` on decrypt.

## What I did not do

- Did not touch `crt.py`, `volconv.py`, or any existing file (only the two owned new files plus the
  two required team files under `team/`).
- Did not commit or push.
- `xorcipher.py` imports nothing beyond the Python standard library (no import of crt/volconv).

## Checks run and results

From the repository root:

1. `python3 -m pytest tests/test_xorcipher.py -q` → `14 passed in 0.02s` (exit 0)
2. `python3 -m pytest tests/ -q` → `25 passed in 0.03s` (exit 0)

Note: the environment had no pytest installed; I installed it with
`python3 -m pip install --break-system-packages pytest` (pytest 9.2.0) so the required check
commands could run. This did not modify any repository file.

## What the validator must pay attention to

- Both required checks pass on the current working tree; the full suite (25 tests) includes the
  pre-existing `roman`/`legacy_stringkit` tests, all green.
- File ownership respected: only `xorcipher.py`, `tests/test_xorcipher.py`, and the two `team/`
  files were created; no existing file was modified (`git status` shows only new untracked files).
- Hex output is lowercase by construction (`bytes.hex()`); `bytes.fromhex` accepts both cases on
  decrypt, which is fine per spec (only invalid characters/odd length must raise).
