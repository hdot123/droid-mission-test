# Handoff: vigenere-module (sub-issue #162)

## What was requested
Process card `vigenere-module` for work order #157 (round 26 A, foreman v2.6.5): create only `vigenere.py` and `tests/test_vigenere.py`.

Spec for `vigenere.py`:
- `encrypt(text, key)` / `decrypt(text, key)` implement the Vigenere cipher.
- Key must be a non-empty string of pure English letters (case-insensitive), otherwise raise `ValueError`.
- Only English letters are transformed; case is preserved individually.
- Key letters cycle and advance only when an English letter is encountered in the text; all other characters pass through unchanged.
- Required examples: `encrypt("ATTACKATDAWN", "LEMON") -> "LXFOPVEFRNHR"`, `encrypt("Attack", "LEMON") -> "Lxfopv"`, `decrypt("LXFOPVEFRNHR", "LEMON") -> "ATTACKATDAWN"`.

Constraints: Python standard library only; no imports from other modules (no ean13/temperature); no package directory; no CLI; the test file tests only this module.

## What I did
- Created `vigenere.py` with `encrypt(text, key)` and `decrypt(text, key)`:
  - Key validated once up front: must be a `str`, non-empty, `str.isalpha()` and `str.isascii()` true (so `None`, `42`, `""`, `"LE MON"`, `"LE1"`, `"123"`, `"LÉMON"` all raise `ValueError`).
  - For each character: if it is an ASCII letter, shift by the current key letter (mod 26) with `A`/`a` bases depending on the character's case, then advance the key index; otherwise append unchanged.
  - Key index is taken modulo key length, so the key cycles.
- Created `tests/test_vigenere.py` with 14 tests covering:
  - the three required examples verbatim,
  - a decrypt/encrypt roundtrip including punctuation, space, and digits,
  - non-alpha pass-through without key advance (`"A A"`/`"LE"` -> `"L E"`, `"A1A"`/`"LE"` -> `"L1E"`),
  - key cycling (`"AAAA"`/`"AB"` -> `"ABAB"`),
  - empty text,
  - `ValueError` for invalid keys for both functions (parametrized).

## What I did not do
- Did not create or touch `ean13.py`, `temperature.py`, or their tests (owned by other cards).
- Did not touch `team/**` files other than my own two (`team/handoffs/vigenere-module.md`, `team/status/vigenere-module.json`).
- Did not touch repo-level tooling, did not commit or push.

## Checks I ran
- Card check (verbatim): `python -m pytest -q tests/test_vigenere.py`
- Result: **14 passed in 0.01s**, exit code 0.
- Note: pytest was not preinstalled in the environment; I installed it with `python -m pip install pytest` (pip install into the runner's user environment only, no repo changes).

## What the validator must pay attention to
- The first run of the check failed with 1 failure: my own test expectation for `encrypt("A A", "LE")` was wrong (I had written `"L L"`; correct is `"L E"` because the key advances on the second letter `A` -> `E`). I fixed the test expectation, not the implementation; the implementation was correct throughout.
- Acceptance criterion (3) — full-repo `python -m pytest -q` — is the foreman/aggregate step; this card's check column only specifies `python -m pytest -q tests/test_vigenere.py`, which is what I ran and what is recorded in my status file. The other two cards own their own test files.
- The module has no cross-module imports, no package directory, and no CLI, per the constraints.
