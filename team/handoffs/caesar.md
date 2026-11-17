# Handoff: caesar (sub-issue #75)

## What was requested
Process card #75 under work order #72 (three independent tool modules, 领班制 v2.6.2). Scope: implement `caesar.py` with `encode(text, shift)` / `decode(text, shift)` and `tests/test_caesar.py`, plus this handoff and status file. Caesar rules: shift only A–Z / a–z, preserve case, shift modulo 26 (negative shifts legal), all other characters unchanged; `decode` is the inverse of `encode`. Standard library only; no imports between modules; no package directory; no CLI.

Hard examples that must hold verbatim (written into the test file and the check column):
- `encode("Abc XyZ!", 2)` → `"Cde ZaB!"`
- `encode("abc", -1)` → `"zab"`
- `decode("Cde", 2)` → `"Abc"`

## What I did
- Created `caesar.py`: `encode` classifies each character (`A-Z`, `a-z`, or other), applies `(ord(ch) - base + shift) % 26` for letters, passes everything else through unchanged; `decode(text, shift)` delegates to `encode(text, -shift)`.
- Created `tests/test_caesar.py`: 8 tests covering the three hard examples verbatim, the decode-inverse example (`decode(encode("Hello, World! 123", 13), 13)`), case preservation/non-letter passthrough, modulo-26 behavior (shift 26, 27, −27), roundtrips at shifts 1/13/−5/26/−26, and empty strings. Tests import only `caesar`.
- Wrote this handoff and `team/status/caesar.json`.

## What I did NOT do
- Did not create or edit `wordscore.py`, `hexcolor.py`, their tests, or any other module's files.
- Did not touch other processes' team files; only `team/handoffs/caesar.md` and `team/status/caesar.json` were written.
- Did not commit or push (left to the workflow).

## Checks ran and results
1. `python -m pytest -q tests/test_caesar.py` → initially failed with "No module named pytest" (pytest was not installed in this environment). After installing pytest, re-ran: **8 passed in 0.02s, exit 0**.
2. `python -c "from caesar import encode, decode; assert encode('Abc XyZ!', 2) == 'Cde ZaB!', 'example 1'; assert encode('abc', -1) == 'zab', 'example 2'; assert decode('Cde', 2) == 'Abc', 'example 3'; assert decode(encode('Hello, World! 123', 13), 13) == 'Hello, World! 123', 'decode inverse'; print('caesar examples all hold')"` → **`caesar examples all hold`, exit 0**.
3. `test -f caesar.py && test -f tests/test_caesar.py && echo files-present` → **`files-present`, exit 0**.

## Notes for the validator
- All three process-card checks were run as written and now pass (check 1 required installing pytest first; the repository did not vendor it).
- I ran only my own test file (`tests/test_caesar.py`), per the card. The work-order-level `python -m pytest -q` (all three modules) is not something I can pass alone while other workers' modules are in flight; the validator should run it at integration time.
- No ambiguity or conflict was found in the caesar card; the deliverable and check-column examples are consistent (unlike the wordscore card's deliberate contradiction, which is not mine to resolve).
