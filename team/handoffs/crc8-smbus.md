# Handoff: crc8-smbus (sub-issue #318)

## What was requested
Process card for work order #312 (round 38, concurrency batch A): implement CRC-8/SMBUS.

- Own **only** `crc8.py` and `tests/test_crc8.py` (two new files).
- `crc8(data: bytes) -> int`: polynomial 0x07, initial value 0x00, no reflection, no final XOR (CRC-8/SMBUS); return an integer in 0-255.
- Every acceptance point must have a corresponding test:
  - `crc8(b"123456789") == 0xF4`
  - `crc8(b"") == 0`
  - `crc8(b"\x00") == 0`
  - return value always within 0-255 (including varied inputs)
- Standard library only; must not import `base32hex`, `manchester`, or any non-stdlib module.
- No existing file may be changed; no `team/` or `.github/` paths owned by others touched.

## What I did
Created exactly two new files:

- `crc8.py` — MSB-first bit-at-a-time CRC-8: `crc = 0`; for each byte `crc ^= byte`, then 8 shifts with XOR by 0x07 when the high bit is set, masked to 0xFF each step. Standard library only, no intra-repo imports.
- `tests/test_crc8.py` — 5 test cases covering every acceptance point:
  1. `test_check_value_123456789` — `crc8(b"123456789") == 0xF4`
  2. `test_empty_input_returns_zero` — `crc8(b"") == 0`
  3. `test_single_zero_byte_returns_zero` — `crc8(b"\x00") == 0`
  4. `test_return_value_always_in_range` — asserts `isinstance(result, int)` and `0 <= result <= 255` over 9 varied inputs (empty, `0x00`, `0x01`, `0xFF`, `"123456789"`, `"foobar"`, `bytes(range(256))`, 64×`0x00`, 64×`0xFF`)
  5. `test_known_values` — `crc8(b"\x00\x00\x00\x00") == 0x00`, `crc8(b"\x01") == 0x07`, `crc8(b"123456789") == 0xF4`

Also wrote this handoff and `team/status/crc8-smbus.json`.

## What I did NOT do
- Did not create or touch `base32hex.py`, `manchester.py`, or their tests (owned by other process cards).
- Did not modify any pre-existing repository file (verified: only new files added).
- Did not commit or push (left to the workflow).
- Did not touch `team/` files owned by other processes.

## Checks run and results
Both process checks, run verbatim:

- `python3 -m pytest tests/test_crc8.py -q` → `5 passed in 0.01s` (exit 0)
- `python3 -m pytest tests/ -q` → `16 passed in 0.03s` (exit 0)

Note: `pytest` was not installed in the environment; installed it via `python3 -m pip install pytest` before running checks.

## Notes for the validator
- An earlier draft of `test_known_values` asserted `crc8(b"\x01\x02\x03") == 0x4B`, which was my own mis-recollection and failed (actual: 0x48 = 72). I removed that assertion; the shipped tests use only values verifiable from the spec (`0xF4`, `0`, `0`) plus directly derivable ones (`b"\x00" * 4 → 0x00`, `b"\x01" → 0x07`).
- The implementation is a straightforward MSB-first CRC; `crc8(b"123456789") == 0xF4` is the canonical CRC-8/SMBUS check value and passes.
- Full suite is 16 tests: 5 mine + 11 pre-existing (`test_roman.py`, `test_legacy_stringkit.py`), all green.
