# Handoff: fnv1a-32-bit-hash (sub-issue #416)

## What was requested

Work order #407, round 43 · A unit, process card `fnv1a-32-bit-hash`:

- Create `fnv1a.py` exposing `fnv1a32(data: bytes) -> int` — FNV-1a 32-bit hash (offset basis 2166136261, prime 16777619, no final xor), returning an int in 0–4294967295, raising `TypeError` for non-bytes input.
- Create `tests/test_fnv1a.py` with a test case for every acceptance item.
- Only these two files may be created; no existing file may be modified; standard library only; no import of `base58` or `verhoeff` (or anything outside the stdlib besides pytest in tests).

## What I did

- Created `fnv1a.py`: a single function `fnv1a32` implementing the classic FNV-1a 32-bit algorithm (xor byte, multiply by prime, mask to 32 bits, no final xor). Non-`bytes` input (including `str`, `bytearray`, `memoryview`) raises `TypeError` via an explicit `isinstance` check. Module constants `_OFFSET_BASIS`, `_PRIME`, `_MASK32` are private.
- Created `tests/test_fnv1a.py` with six test functions, one per acceptance item:
  - `fnv1a32(b"") == 2166136261`
  - `fnv1a32(b"hello") == 1335831723`
  - `fnv1a32(b"foobar") == 3214735720`
  - `fnv1a32(b"123456789") == 3146166556`
  - `fnv1a32(b"a" * 1000) == 500786573`
  - `fnv1a32("x")` raises `TypeError`

## What I did NOT do

- Did not touch `roman.py`, `legacy_stringkit.py`, `README.md`, `worker-prompt.txt`, `worker-stream.jsonl`, or anything under `tests/` other than adding `tests/test_fnv1a.py`.
- Did not create `base58.py`, `verhoeff.py`, or their tests (owned by sibling processes).
- Did not import `base58` or `verhoeff`; no third-party dependency in `fnv1a.py`.
- Did not commit or push.

## Checks run and results

Environment note: `pytest` was not preinstalled; I installed it via `python3 -m pip install pytest` (environment setup only, no repo file changed).

1. `python3 -m pytest tests/test_fnv1a.py -q` → **6 passed**
2. `python3 -m pytest tests/ -q` → **17 passed** (6 mine + 11 pre-existing baseline tests, all green)

## Notes for the validator

- The implementation has no final xor and no 64-bit variant, exactly as specified; the empty input returns the offset basis 2166136261, which is the expected behavior of the spec.
- `TypeError` is raised for any non-`bytes` type, not just `str`; the spec only mandates `str` raising, so this is a superset and should not conflict.
- The acceptance vectors are the canonical FNV-1a 32-bit values and were verified by the passing tests.
