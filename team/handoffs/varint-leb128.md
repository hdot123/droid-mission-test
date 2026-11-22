# Handoff: varint-leb128 (sub-issue #350)

## What was requested
Implement unsigned LEB128 varint encode/decode per work order #345, process card `varint-leb128`. Scope owned: only `varint.py` and `tests/test_varint.py` (new files). Standard library only; must not import zigzag or hamming; must not modify any existing file.

Spec:
- `encode(n: int) -> bytes` — unsigned LEB128 (little-endian, low 7 bits payload per byte, high bit continuation flag); negative `n` raises `ValueError`.
- `decode(data: bytes) -> int` — inverse; must consume exactly the entire input; raises `ValueError` on empty input, on unterminated input (last byte has continuation bit set), and on trailing bytes after a terminator.

## What I did
Created `varint.py` with `encode`/`decode` as specified, and `tests/test_varint.py` with one test case per acceptance criterion:

- `encode(0) == b"\x00"`, `encode(1) == b"\x01"`, `encode(127) == b"\x7f"`, `encode(128) == b"\x80\x01"`, `encode(300) == b"\xac\x02"`, `encode(624485) == b"\xe5\x8e\x26"`
- `decode(b"\xe5\x8e\x26") == 624485`, `decode(b"\xac\x02") == 300`
- `encode(-1)` raises `ValueError`
- `decode(b"")`, `decode(b"\x80")` (unterminated), `decode(b"\x01\x02")` (trailing byte) each raise `ValueError`
- round-trip identity: `decode(encode(123456789)) == 123456789`

## What I did NOT do
- Did not touch `zigzag.py`, `hamming.py`, or any existing file (roman.py, legacy_stringkit.py, existing tests, README, etc.).
- Did not add any imports beyond `pytest` in the test file; `varint.py` imports nothing.
- Did not commit or push.

## Checks run and results
1. `python3 -m pytest tests/test_varint.py -q` → **13 passed**
2. `python3 -m pytest tests/ -q` → **24 passed** (13 new varint + 11 pre-existing)

Note: pytest was not installed in the environment initially (`No module named pytest`); I installed it via `python3 -m pip install pytest` to run the checks. No repository files were changed by that install.

## For the validator
- Every acceptance criterion from the process card has a dedicated test function in `tests/test_varint.py`; verify each is present and passes.
- `decode` rejects trailing bytes by checking that the terminator byte is the last byte (`index != len(data) - 1`), and rejects unterminated input when the loop ends with the continuation bit still set on every byte.
- Only two new files should appear from this process: `varint.py`, `tests/test_varint.py`, plus the two team files `team/handoffs/varint-leb128.md` and `team/status/varint-leb128.json`.
