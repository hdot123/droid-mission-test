# Handoff: geohash (sub-issue #957)

## What was requested
Work order #951 第59轮 A 单, process card `geohash`: create **only** `geohash.py` and `tests/test_geohash.py`, implementing standard geohash encoding/decoding per the card spec, with every acceptance point covered by a corresponding test. Standard library only, no cross-module imports, no modification of any existing file.

## What I did
- Created `geohash.py`:
  - `geohash_encode(lat, lon, precision=12) -> str` — alphabet exactly `0123456789bcdefghjkmnpqrstuvwxyz`; lat interval [-90, 90], lon interval [-180, 180]; bit-by-bit binary subdivision with **longitude bits first** interleaved; 5 bits per character; coordinate exactly at midpoint takes the upper half (`>= mid` records 1).
  - `geohash_decode(code: str) -> tuple[float, float]` — returns the **cell center** (lat, lon), not the original coordinates.
  - Input contract: lat/lon out of range or precision ∉ [1, 12] → ValueError; empty decode string or character outside alphabet → ValueError; non-numeric lat/lon, non-int precision (bool excluded), non-str code (bool excluded) → TypeError.
  - bool handling: `isinstance(v, (int, float)) and not isinstance(v, bool)` so `True`/`False` raise TypeError, not pass as numbers.
- Created `tests/test_geohash.py` (10 tests), covering every acceptance point:
  - Anchors: `(57.64911, 10.40744, 11) == "u4pruydqqvj"`, `(42.6, -5.6, 5) == "ezs42"` (with an explicit comment that the circulated `ezjmg` pairing is incorrect/deprecated), `(0.0, 0.0, 12) == "s00000000000"`, decode of `u4pruydqqvj` ≈ (57.64911063, 10.40743969) at tolerance 1e-6.
  - Property test: 36 random/boundary points × precision 1..12 — encode agrees one-by-one with an **independent integer-bitcode interleaved reference** (uses `fractions.Fraction`, does not import the module's logic), decode center re-encodes to the identical code, and the original coordinates fall inside the decoded cell.
  - ValueError cases: `geohash_encode(90.1, 0.0)`, `geohash_encode(0.0, -180.1)`, `geohash_encode(0.0, 0.0, 0)`, `geohash_encode(0.0, 0.0, 13)`, `geohash_decode("")`, `geohash_decode("a")`, `geohash_decode("ezjmg!")`.
  - TypeError cases: `geohash_encode("0", 0.0)`, `geohash_encode(0.0, True)`, `geohash_encode(0.0, 0.0, 5.0)`, `geohash_decode(123)`.

## What I did NOT do
- Did not create or touch `pell.py`, `ackermann.py`, or their tests (other cards).
- Did not modify any existing file. Only new files: `geohash.py`, `tests/test_geohash.py`, plus this handoff and `team/status/geohash.json`.
- Did not commit or push.
- Did not cite the deprecated `(42.6, -5.6) -> ezjmg` pairing anywhere.

## Checks run and results
- `python3 -m pytest tests/test_geohash.py -q` → **10 passed** in 0.05s.
- `python3 -m pytest tests/ -q` → **352 passed, 2 skipped** in 21.64s (suite-wide baseline intact; the 2 skips are pre-existing).
- `verdict.json` / `verdict.md` by-products: none were produced; `rm -f verdict.json verdict.md` run as precaution.

## What the validator must pay attention to
- Only two deliverable source files are mine: `geohash.py`, `tests/test_geohash.py`.
- `git status` shows two other untracked files (`worker-prompt.txt`, `worker-stream.jsonl`) that pre-existed my session — not mine, not touched.
- The property test's independent reference recomputes integer grid indices with exact `Fraction` arithmetic and a different bit layout path (integer index → bits), so agreement is not tautological with the module's float-bisection implementation.
- Decode of odd total bit counts assigns the extra bit to longitude (longitude-first interleave); covered by tests through precision 1..12 round-trips.
