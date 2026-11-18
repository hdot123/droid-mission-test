# Handoff: crc16 (sub-issue #283)

## What was requested
Process card #283 for work order #279 (round 35): implement the CRC-16/CCITT-FALSE component.

- `crc16.py` with `compute(data: bytes) -> int` using exactly: polynomial 0x1021, initial value 0xFFFF, no reflection, output xor 0x0000 (CCITT-FALSE); empty input returns 0xFFFF.
- `tests/test_crc16.py` with a test case for every acceptance item:
  - `compute(b"123456789") == 0x29B1` (10673)
  - `compute(b"") == 0xFFFF`
  - `compute(b"\x00") == 0xE1F0` (57840)
- Standard library only; no imports of hamming74 or parity2d; only new files created, no existing files modified.
- Checks (verbatim): `python3 -m pytest tests/test_crc16.py -q`, `python3 -m pytest tests/ -q`.

## What I did
- Created `crc16.py`: bit-wise CRC-16/CCITT-FALSE implementation (`_POLY = 0x1021`, `_INIT = 0xFFFF`, 8 shifts per byte, final value returned directly since output xor is 0x0000). No imports at all, so no cross-component coupling.
- Created `tests/test_crc16.py`: unittest-style tests covering all three acceptance vectors, plus decimal literal variants (10673 and 57840) so the parenthetical values in the spec are asserted directly.
- Installed pytest into the environment (it was not present) in order to run the mandated checks. This only touched the Python environment, not repository files.

## What I did not do
- Did not create or touch `hamming74.py`, `parity2d.py`, `tests/test_hamming74.py`, `tests/test_parity2d.py`, or any other existing repository file.
- Did not modify any pre-existing file (git status at start showed only untracked worker files; my additions are new: `crc16.py`, `tests/test_crc16.py`, `team/handoffs/crc16.md`, `team/status/crc16.json`).
- Did not commit or push.
- Did not implement anything outside the crc16 scope.

## Checks run and results
1. `python3 -m pytest tests/test_crc16.py -q` → **5 passed** (exit 0)
2. `python3 -m pytest tests/ -q` → **16 passed** (exit 0) (includes other teams' existing/new tests; all green)

Note: the first attempt failed with `No module named pytest`; resolved by `python3 -m pip install pytest` (pytest 9.2.0). Re-ran both checks afterward, both green.

## What the validator must pay attention to
- `compute` returns the raw register (output xor is 0x0000, so no final inversion is applied — this is correct for CCITT-FALSE).
- Empty input short-circuits to the initial value 0xFFFF via the loop body never running.
- Spec acceptance vectors are asserted both as hex and as decimal literals in the test file; all match.
- Full-suite result (16 passed) is green as of this handoff; if other process cards land concurrently, rerun `python3 -m pytest tests/ -q` after merge for the authoritative combined result.
