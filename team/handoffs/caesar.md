# Handoff: caesar (sub-issue #98)

## What was requested
Process card #98 under work order #95 (领班制 v2.6.4): implement `caesar.py` exposing
`encode(text, shift)` and `decode(text, shift)` plus `tests/test_caesar.py`.

Spec:
- Shift only A–Z and a–z, preserving case; shift taken mod 26; negative shifts legal.
- All other characters unchanged.
- `decode` is the inverse of `encode`.
- Hard examples (verbatim in tests): `encode("Abc XyZ!", 2) -> "Cde ZaB!"`,
  `encode("abc", -1) -> "zab"`, `decode("Cde", 2) -> "Abc"`.
- Constraints: Python standard library only; no imports of wordscore/hexcolor; no
  package directory; no CLI.

## What I did
- Created `caesar.py` with `encode(text, shift)` (mod-26 shift, case-preserving,
  non-letters untouched) and `decode(text, shift)` implemented as `encode(text, -shift)`.
- Created `tests/test_caesar.py` covering only the caesar module: the three required
  examples verbatim, case/non-letter preservation, mod-26 wraparound, and
  decode/encode round-trip over several positive and negative shifts.

## What I did not do
- Did not touch `wordscore.py`, `hexcolor.py`, or any other process's files/tests.
- Did not create a package directory or CLI; did not add non-stdlib dependencies to
  the code (pytest was installed into the environment only to run the required checks).
- Did not commit or push.

## Checks run and results
All four card check commands were executed verbatim from the repo root:

1. `python -m pytest -q tests/test_caesar.py` → `7 passed`
2. `python -m pytest -q` → `7 passed` (repo currently contains only the caesar tests)
3. `python -c "from caesar import encode, decode; assert encode('Abc XyZ!', 2) == 'Cde ZaB!'; assert encode('abc', -1) == 'zab'; assert decode('Cde', 2) == 'Abc'; print('caesar examples ok')"` → `caesar examples ok`
4. `python -c "import caesar, inspect; print(inspect.signature(caesar.encode)); print(inspect.signature(caesar.decode))"` → `(text, shift)` / `(text, shift)`

Note: pytest was not present in the environment initially; I installed it with
`python3 -m pip install pytest` (pytest 9.2.0) so the required checks could run.

## Notes for the validator
- One intermediate test failure occurred during development: my own assertion for
  `decode("123 ab-cd_", 4)` was wrong (I expected a forward shift). The module was
  correct; I fixed the test expectation to `"123 wx-yz_"`. Final state passes all checks.
- `decode` is defined as `encode(text, -shift)`, so it is the exact inverse by construction.
- Required examples are written verbatim in `tests/test_caesar.py`
  (`test_encode_basic_example`, `test_encode_negative_shift`, `test_decode_example`).
