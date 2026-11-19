# Handoff: implement-crt (sub-issue #491)

## What was requested
Implement `crt.py` with `crt(remainders, moduli) -> int` (Chinese Remainder Theorem, pairwise-coprime moduli, smallest non-negative solution) plus `tests/test_crt.py`, per process card #491 under work order #480 (round 46 · C). Owns only `crt.py` and `tests/test_crt.py`.

## What I did
- Created `crt.py` (standard library only: `math.gcd`; `pow(x, -1, m)` for modular inverse). Validation order per spec:
  1. Non-list/tuple input → `TypeError`
  2. Length mismatch or empty → `ValueError`
  3. Non-int elements (bool rejected as non-int per strict `isinstance` intent) → `TypeError`
  4. Modulus < 2, remainder outside `0 <= r < m`, non-coprime moduli pair → `ValueError`
- Solution computed via product of moduli, Garner-style accumulation, reduced mod product.
- Created `tests/test_crt.py` with 16 tests covering every acceptance bullet plus tuple-input and container-type cases.

## What I did not do
- Did not touch `volconv.py`, `xorcipher.py`, `roman.py`, `legacy_stringkit.py`, any existing test, or any other file.
- Did not commit or push.
- No cross-imports; `crt.py` imports nothing from the other round-46 modules.

## Checks run (results)
- `python3 -m pytest tests/test_crt.py -q` → **16 passed**
- `python3 -m pytest tests/ -q` → **27 passed** (includes pre-existing 11 tests)

Note: pytest was not present in the environment; installed with `python3 -m pip install --user --break-system-packages pytest` (pytest 9.2.0) to run the checks. No repository files were changed by this.

## What the validator must pay attention to
- `bool` elements are rejected as `TypeError` (e.g. `crt([True], [3])`) — the spec says "元素须为 int"; I treated bool as invalid. If a hidden test expects `True` to be accepted as `1`, that is the one behavior that could differ.
- Validation order: length/empty checks run before element-type checks, so `crt([], [])` raises `ValueError` (empty), not TypeError, and mismatched lengths raise `ValueError` before any element inspection.
- All spec'd acceptance values verified: `23, 7, 0, 19, 30, 5, 2188` and all error cases.
