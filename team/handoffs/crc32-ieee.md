# Handoff: crc32-ieee (sub-issue #387)

## What was requested
Process card "crc32-ieee": create `crc32.py` and `tests/test_crc32.py` as new files only, implementing `crc32(data: bytes) -> int` per CRC-32/IEEE (reflected polynomial 0xEDB88320, init 0xFFFFFFFF, final XOR 0xFFFFFFFF), implemented by hand without `zlib.crc32`. Non-bytes input (including `str`) raises `TypeError`. All seven acceptance criteria must have corresponding tests. Standard library only, no cross-imports with base36/graycode.

## What I did
- Created `crc32.py`: precomputed 256-entry CRC table built at import; bitwise reflected algorithm; returns int in 0–4294967295; raises `TypeError` for non-bytes.
- Created `tests/test_crc32.py`: one test per acceptance point (empty input, check value `b"123456789"`, `b"hello"`, `b"\x00"`, `b"a" * 1000`, `b"Wikipedia"`, `TypeError` on `"abc"`).

## What I did not do
- Did not touch `base36.py`, `graycode.py`, or any pre-existing file (`roman.py`, `legacy_stringkit.py`, existing tests, README).
- Did not use `zlib.crc32`.
- Did not commit or push.

## Checks run
- `python3 -m pytest tests/test_crc32.py -q` → 7 passed
- `python3 -m pytest tests/ -q` → 18 passed

Note: `pytest` was not installed in the environment; installed it via `python3 -m pip install pytest` to run the required checks (no repository files affected).

## For the validator
- Both acceptance values and the algorithm spec were followed verbatim; verify the seven acceptance points are each covered by a named test in `tests/test_crc32.py`.
- The table-driven implementation is functionally identical to the required bit-by-bit spec; polynomial/init/final-XOR constants are exactly 0xEDB88320 / 0xFFFFFFFF / 0xFFFFFFFF.
- Full-suite check passes alongside other teams' files only if they are present; at the time of this run the suite contained the pre-existing tests plus this module.
