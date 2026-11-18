# Handoff: vigenere-cipher (sub-issue #367)

## What was requested
Process card `vigenere-cipher` from work order #348 (第四十轮 · E · caesar／vigenere／euclid):
create **only** `vigenere.py` and `tests/test_vigenere.py` as new files, implementing:

- `encrypt(text: str, key: str) -> str`
- `decrypt(text: str, key: str) -> str`

Rules from the card, verbatim in effect:
- key must be non-empty and contain only ASCII letters (case-insensitive), otherwise raise `ValueError`;
- only ASCII letters are transformed and their case is preserved;
- non-letter characters are left unchanged and **do NOT advance the key position**;
- standard library only; must not import `caesar` or `euclid`;
- every acceptance item must have a corresponding test case in `tests/test_vigenere.py`.

## What I did
Created the two files (nothing else in the repo was touched).

- `vigenere.py`: key validation in a shared `_validate_key` (raises `ValueError` for empty/non-str/non-ASCII-letter keys, used by both `encrypt` and `decrypt`); ASCII-letter check; per-character shift with key cycling (`key[pos % len(key)]`) only on ASCII letters; non-letters copied verbatim without consuming a key slot; direction `+1` for encrypt, `-1` for decrypt (mod-26, so negative shifts wrap correctly).
- `tests/test_vigenere.py`: 13 tests covering all seven acceptance items plus key validation on `decrypt`, key case-insensitivity, non-ASCII letters, empty text, non-advancing key position, and a roundtrip suite.

## Conflict resolution (must be reviewed)
The card flagged a conflict for `encrypt("Hello, World!", "key")`:
- body rule (non-letters do not advance key) → `"Rijvs, Gspvh!"` per the card's note;
- acceptance criterion → `"Rijvs, Uyvjn!"` (provisional value, authoritative per the card).

**Important finding:** I implemented the stated rule (non-letters do not advance key) and the result matches the acceptance value exactly, not the card's "other" value. Manual derivation: key `key` cycles `k,e,y,k,e` over `Hello` → `Rijvs`; `,` and ` ` are skipped without consuming a slot, so `World` continues with `y,k,e,y` → `Uyvjn`, giving `"Rijvs, Uyvjn!"`. The card's `"Rijvs, Gspvh!"` would only arise from a different rule (e.g., punctuation counted as consuming a slot), which contradicts the stated body rule.

So: **the acceptance value and the body rule agree**; the recorded "alternative" appears to be miscalculated. The test `test_encrypt_hello_world_conflict_records_both_values` documents both candidate values in its comments/docstring and asserts the provisional value `"Rijvs, Uyvjn!"` (which is also what the implementation produces).

## What I did NOT do
- Did not create or touch `caesar.py`, `euclid.py`, `tests/test_caesar.py`, `tests/test_euclid.py` (owned by other cards).
- Did not modify any pre-existing file (`roman.py`, `legacy_stringkit.py`, existing tests, README, etc.).
- Did not commit or push.
- No cross-module imports; `vigenere.py` uses only the standard library (actually no imports at all).

## Checks run
From the repository root:

1. `python3 -m pytest tests/test_vigenere.py -q` → **13 passed** (exit 0)
2. `python3 -m pytest tests/ -q` → **24 passed** (exit 0)

Note: `pytest` was not installed in the environment; I installed it with `python3 -m pip install pytest` (pytest 9.2.0) to run the mandated checks. No repo files were changed by that install.

## Notes for the validator
- Verify the conflict item: run `python3 -c "from vigenere import encrypt; print(repr(encrypt('Hello, World!','key')))"` → expect `'Rijvs, Uyvjn!'`. If a future validator believes the body rule yields `'Rijvs, Gspvh!'`, the implementation is still correct per the acceptance criterion; reconcile the card's alternative value rather than the code.
- Key cycling is required: plaintext longer than the key must wrap the key (e.g. `encrypt("ATTACKATDAWN", "LEMON")`).
- The `test_non_ascii_letters_untouched` test uses a literal `é`; it asserts behavior, not a specific full-string constant, so NFC/NFD source normalization does not affect it.
