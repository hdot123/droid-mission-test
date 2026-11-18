# Handoff: crc8-module (sub-issue #259)

## What was requested
Process card `crc8-module` under work order #245 (round 33, group A):
- Implement `crc8.py`: CRC-8/SMBUS checksum, polynomial `0x07`, init `0x00`, no input/output reflection, no final XOR. `crc8(data)` returns an `int` in 0–255; `crc8_hex(data)` returns the same value as a two-character uppercase hex string.
- Required examples: `crc8(b"")` -> `0`, `crc8(b"123456789")` -> `0xF4` (244), `crc8(b"\x01")` -> `0x07`, `crc8(b"A")` -> `0xC0`, `crc8_hex(b"123456789")` -> `"F4"`.
- Write `tests/test_crc8.py` covering only `crc8.py` behavior, including all examples above.
- Python standard only; no imports of the other modules; no package directory; no CLI.

## What I did
- Created `crc8.py` with `crc8(data)` and `crc8_hex(data)`. Bitwise MSB-first implementation over each byte, xor with `0x07` on the top bit, masked to 8 bits; `crc8_hex` is `"%02X" % crc8(data)`.
- Created `tests/test_crc8.py` with 10 tests: empty input, the `0xF4` check value, the `0x07` / `0xC0` single-byte examples, int-range/determinism checks, `crc8_hex` uppercase two-char formatting and equality with `crc8`, plus `TypeError` cases for `str` input (a `str` iterates to characters, so it must not be silently accepted).
- Verified the spec's expected values against an independent reference computation before writing the tests (all five examples matched).

## What I did not do
- Did not touch `base32hex.py`, `manchester.py`, `roman.py`, `legacy_stringkit.py`, or any other test file (my tests exercise only `crc8.py`).
- Did not add a package directory, CLI, or any third-party dependency.
- Did not commit or push (workflow handles that).
- Note: `pytest` was missing from this environment, so I ran `python3 -m pip install pytest` (installed pytest 9.2.0) to be able to run the required check. No repository files were changed by that.

## Checks run
- `python -m pytest -q tests/test_crc8.py` -> `10 passed in 0.02s` (exit 0). This is the card's only check command, run verbatim.
- Attempted first without pytest installed (`No module named pytest`), then after installing pytest the command passed as shown above.

## For the validator
- The card's single check command passes; all five required example values are asserted in `tests/test_crc8.py`.
- `crc8_hex` always returns exactly two uppercase hex characters (zero-padded), e.g. `crc8_hex(b"")` -> `"00"`.
- Passing a `str` to either function raises `TypeError` rather than producing a checksum; the spec only defines behavior for `bytes` input, so this is the conservative choice.
- Files owned by this process: `crc8.py`, `tests/test_crc8.py`, `team/handoffs/crc8-module.md`, `team/status/crc8-module.json`.
