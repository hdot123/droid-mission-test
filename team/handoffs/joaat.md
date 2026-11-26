# Handoff: joaat (sub-issue #944)

## What was requested

Process card `joaat` from work order #926 (round 58, concurrent order A):

- Implement `joaat.py` exposing `joaat_hash(data: bytes) -> int` — the Jenkins one-at-a-time 32-bit hash, algorithm verbatim:
  - `h = 0`; for each byte `b`: `h += b`, `h += h << 10`, `h ^= h >> 6`;
  - finalization: `h += h << 3`, `h ^= h >> 11`, `h += h << 15`;
  - every step wraps to 32 bits (`& 0xFFFFFFFF`) throughout; result in `[0, 2**32)`.
- Input contract: non-bytes input (including `str`, `int`, `list`, `bytearray`) raises `TypeError`.
- New files only: `joaat.py` and `tests/test_joaat.py`. No existing file modified; standard library only; no imports of `rectunion`/`eulerian`.
- Every acceptance item must have a corresponding test case.

## What I did

- Created `joaat.py` (new): `joaat_hash` implements the verbatim algorithm with step-by-step 32-bit wrapping; raises `TypeError` for any non-`bytes` input (checked via `isinstance(data, bytes)`, which also rejects `bytearray`, `str`, `int`, `list`).
- Created `tests/test_joaat.py` (new), covering every acceptance item:
  - `joaat_hash(b"") == 0`
  - all-zero fixed point: `joaat_hash(b"\x00" * k) == 0` for `k ∈ [1, 5]` (parametrized)
  - result always in `[0, 2**32)` over 200 random byte strings (len 0–40)
  - agreement with two independent reference implementations living in the test file — a reduce/decomposed-step implementation and a streaming chunked-update implementation — over 300 random byte strings of length 0–40, plus explicit coverage of every length 0..40 with chunk sizes 1 and full-length
  - `TypeError` for `"abc"`, `123`, `[1, 2]`, `bytearray(b"a")` (parametrized)

## What I did not do

- Did not touch `rectunion.py`, `eulerian.py`, or any other component (other processes own those).
- Did not modify any pre-existing file (including `roman.py`, `legacy_stringkit.py`, existing tests, docs, schemas, scripts).
- Did not add non-standard-library dependencies.
- Did not commit or push.
- No CONFLICT was noted in the work order; none found between body and acceptance section.

## Checks run and results

From the repository root:

1. `python3 -m pytest tests/test_joaat.py -q` → **13 passed** in 0.04s
2. `python3 -m pytest tests/ -q` → **355 passed, 2 skipped** in 21.72s

No `verdict.json` / `verdict.md` by-products appeared in the repo root during these runs (nothing to delete).

## Validator notes

- The wrapping in `joaat_hash` is done after **each** arithmetic step (`& 0xFFFFFFFF`), not just at return; truncating only before returning would yield different values — the streaming and reduce references in the test file also wrap step by step, so they pin the step-by-step semantics.
- The three finalization steps are present and cannot be omitted; the test references independently re-derive them.
- Input rejection relies on `isinstance(data, bytes)`: `bytearray` and `memoryview` are rejected (only exact `bytes` accepted), matching the contract "非 bytes（含 str、int、list、bytearray）抛 TypeError".
- Reference implementations are deliberately written differently (reduce with pre-masked shifts; streaming class with chunked `update`/`digest`) to provide independent evidence of agreement.
- Test randomness is seeded (`random.Random(...)`) for reproducibility.
