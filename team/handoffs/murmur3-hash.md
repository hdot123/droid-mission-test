# Handoff: murmur3-hash (sub-issue #435)

## What was requested

Process card #435 under work order #430 (Round 44 · Track A): implement `murmur3.py` with `murmur3_32(data: bytes, seed: int = 0) -> int` — the MurmurHash3 32-bit x86 variant — plus `tests/test_murmur3.py` covering every acceptance item. Scope was strictly limited to these two new files; no existing file could be modified, standard library only, no imports of the sibling deliverables (`scytale`, `fiscal`).

## What I did

- Created `murmur3.py`:
  - Constants `c1=0xcc9e2d51`, `c2=0x1b873593`; 4-byte little-endian chunking with the specified per-chunk mixing (`k *= c1; rotl(k,15); k *= c2; h ^= k; rotl(h,13); h = h*5 + 0xe6546b64`), all wrapped to 32 bits via mask `0xffffffff`.
  - Tail (1–3 bytes) assembled little-endian, then only `k *= c1; rotl(k,15); k *= c2; h ^= k` (no `h` update step).
  - Finalize with `h ^= len(data)` then `fmix32` (`h ^= h>>16; h *= 0x85ebca6b; h ^= h>>13; h *= 0xc2b2ae35; h ^= h>>16`), 32-bit wrapped; returns int in 0–4294967295.
  - Validation: non-`bytes` data → `TypeError`; non-`int` seed → `TypeError`; seed outside 0–4294967295 → `ValueError`. Seed masked into 32 bits after validation.
- Created `tests/test_murmur3.py` with a test case for each of the 16 acceptance items (all 11 value vectors, `TypeError` on str input, `ValueError` on seed `-1` and `2**32`), plus extra coverage: non-int seed `TypeError`, and a range/typicality check across payloads and seeds including `0xFFFFFFFF`.

## What I did not do

- Did not touch `scytale.py`, `fiscal.py`, their tests, or any pre-existing file (only the two owned files plus the two required team files were created).
- Did not modify, commit, or push anything.
- Did not import anything outside the standard library or the sibling deliverables.

## Checks run and results

From repo root (pytest was not preinstalled; installed it into the environment to run the mandated checks):

- `python3 -m pytest tests/test_murmur3.py -q` → **16 passed**
- `python3 -m pytest tests/ -q` → **27 passed**

Both exact checks from the work order pass.

## Notes for the validator

- All 13 named acceptance vectors are asserted individually in `tests/test_murmur3.py` (empty, hello default/seed 1/seed 42, foo, 123456789, a, ab, abc, abcd, abcde, str → TypeError, seed -1 and 2**32 → ValueError).
- The implementation follows the spec literally: the tail path performs no `h`-update step, and `len(data)` is mixed in before `fmix32`.
- Seed validation order is: `TypeError` for non-int before range `ValueError`, so a non-int seed never reaches the range check.
- `pytest` had to be installed to run the checks; no repository files were changed by that installation.
