# Handoff — hill-cipher (sub-issue #483)

## What was requested

Process card `hill-cipher` for work order #478 (round 46 · unit A): implement the Hill 2×2 cipher (mod 26) component.

- Create `hill.py` with `hill_encrypt(text: str, key) -> str` and `hill_decrypt(cipher: str, key) -> str`.
- Key is a 2×2 matrix of tuples-of-tuples; elements must be ints in 0–25, determinant coprime with 26, else errors as specified.
- Plaintext preprocessed to uppercase with non-letters stripped (all 26 letters kept, J not folded into I), grouped into digraphs, odd length padded with trailing X. Decrypt returns the padded plaintext including the padding X (not stripped). Empty string in, empty string out. Odd-length ciphertext raises ValueError.
- Create `tests/test_hill.py` with a test case for every one of the 21 acceptance items.
- New files only; do not modify any existing file; standard library only; no imports of `yearday` or `base45`.

## What I did

- Created `hill.py`: key validation distinguishes TypeError (key not a matrix, non-int element, non-str input) from ValueError (wrong shape, element outside 0–25, determinant not coprime with 26); encryption left-multiplies digraph vectors by the key mod 26; decryption multiplies by the adjugate times `pow(det % 26, -1, 26)` mod 26. Padding X is added before encryption and preserved through decryption.
- Created `tests/test_hill.py`: 28 tests covering all 21 acceptance items plus decrypt-side key/input errors and a J-not-folded-into-I check.

## What I did not do

- Did not touch `yearday.py`, `base45.py`, or any existing file (roman.py, legacy_stringkit.py, existing tests, README, etc.).
- Did not modify any file owned by another process.
- Did not commit or push.
- Did not add any dependency; only the standard library (`math.gcd`, `pow`).

## Checks run

From the repository root:

1. `python3 -m pytest tests/test_hill.py -q` → **28 passed** (exit 0)
2. `python3 -m pytest tests/ -q` → **39 passed** (exit 0)

Note: pytest was not installed in the environment initially; I installed it with `python3 -m pip install pytest` (environment tooling, not a repo file).

## For the validator

- Decrypt deliberately returns the padded plaintext: `hill_decrypt("HIOZHN", K1) == "HELLOX"`, `hill_decrypt(hill_encrypt("ZEBRA", K2), K2) == "ZEBRAX"`. Padding X is not stripped.
- `hill_decrypt` rejects odd-length ciphertext with ValueError before any other cipher validation, but still validates the key first (key rules are identical to encrypt).
- All 26 letters are kept; `hill_encrypt("J", K1) == "SD"` and `hill_encrypt("I", K1) == "PB"` (J is not folded into I).
- Key validation order: TypeError for non-matrix/non-int, then ValueError for shape, range, and determinant — matching the spec's error types.
- Both process checks pass as specified; full-suite count 39 includes the 28 hill tests plus the 11 pre-existing baseline tests.
