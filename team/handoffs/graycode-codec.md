# Handoff: graycode-codec (sub-issue #391)

## What was requested
Process card `graycode-codec` under work order #380 (round 42 · unit A). Owns exactly two new files:
- `graycode.py`
- `tests/test_graycode.py`

Scope: implement Gray code encode/decode.
- `encode(n: int) -> int`: `n ^ (n >> 1)`; raise `ValueError` for negative `n`.
- `decode(g: int) -> int`: inverse of encode; raise `ValueError` for negative `g`.
- Acceptance points, each with a corresponding test: encode(0)=0, encode(1)=1, encode(2)=3, encode(3)=2, encode(4)=6, encode(5)=7, encode(6)=5, encode(7)=4, encode(8)=12, encode(10)=15, encode(255)=128, decode(15)=10, decode(128)=255, decode(3)=2, encode(-1)/decode(-1) raise ValueError, round-trip identity for every integer 0..255 inclusive.
- Standard library only; no cross-module imports; only new files, no existing files modified.

## What I did
- Created `graycode.py` with `encode` and `decode` as specified (decode uses the standard shift-XOR accumulation loop).
- Created `tests/test_graycode.py` with parametrized tests covering every encode/decode acceptance point, both negative-value `ValueError` cases, and the 0..255 round-trip identity.
- Installed `pytest` (9.2.0) into the environment, which was not preinstalled, in order to run the checks.

## What I did not do
- Did not touch `crc32.py`, `base36.py`, or any other existing file (those belong to other process cards).
- Did not commit or push anything.
- Did not modify `tests/test_legacy_stringkit.py`, `tests/test_roman.py`, `README.md`, or any other pre-existing file.

## Checks run and results
1. `python3 -m pytest tests/test_graycode.py -q` → exit 0, **17 passed**
2. `python3 -m pytest tests/ -q` → exit 0, **28 passed** (all pre-existing tests plus mine)

## Notes for the validator
- `pytest` was missing from the environment (`No module named pytest`); I installed it via `python3 -m pip install pytest`. If the CI/validator environment lacks pytest, it must be installed there too.
- `graycode.py` performs no type coercion: only the specified `ValueError` checks are implemented (no extra `TypeError` behavior beyond what falls out naturally, e.g. non-int types are not part of the spec).
- Both checks pass from the repository root exactly as written in the process card.
