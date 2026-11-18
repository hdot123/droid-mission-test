# Handoff: hexcodec (sub-issue #323)

## What was requested
Work order #313, 第三十八轮 · 并发 B 单, process card `hexcodec`:

- Create `hexcodec.py` (repo root): hex encode/decode plus a spaced form.
  - `encode(data: bytes) -> str`: lowercase hex, no separator; empty bytes → empty string.
  - `decode(text: str) -> bytes`: accepts mixed case; raises `ValueError` on odd length or non-hex character; empty string → empty bytes.
  - `encode_spaced(data: bytes) -> str`: lowercase hex, each byte separated by a single space (e.g. `"00 ff"`); empty bytes → empty string.
- Create `tests/test_hexcodec.py` with a corresponding test case for every acceptance point:
  - `encode(b"\x00\xff") == "00ff"`
  - `decode("00FF") == b"\x00\xff"`
  - `encode_spaced(b"\x00\xff") == "00 ff"`
  - `decode("0")` and `decode("zz")` each raise `ValueError`
  - round-trip identity for `b"\xde\xad\xbe\xef"` (`decode(encode(x)) == x`)
- Only add these two files; never modify any existing file; standard library only; no imports of other project modules.

## What I did
- Added `hexcodec.py`: `encode` uses `bytes.hex()` (lowercase, no separator); `decode` validates even length via `len(text) % 2`, validates each character against `string.hexdigits`, then `bytes.fromhex(text)`; `encode_spaced` joins `"%02x" % b` per byte with a single space (empty input → `""`). Imports: `string` only (standard library).
- Added `tests/test_hexcodec.py` covering every acceptance point plus edge cases (empty inputs, mixed case, lowercase output, odd-length and non-hex `ValueError`s, round-trips over `b""`, single bytes, `b"\x00\xff"`, and `bytes(range(256))`).
- Wrote `team/handoffs/hexcodec.md` and `team/status/hexcodec.json` as instructed.

## What I did NOT do
- Did not touch `quotedprint.py`, `pctform.py`, or any pre-existing file (`roman.py`, `legacy_stringkit.py`, `README.md`, existing tests, git state). No commit or push.
- Did not add soft-wrapping, spacing in `decode`, or any behavior beyond the spec.
- Note: `pytest` was not present in this environment; I installed it with `python3 -m pip install pytest` (pytest 9.2.0) so the mandated checks could run. This only changed the Python environment, not repository files.

## Checks run and results
- `python3 -m pytest tests/test_hexcodec.py -q` → 9 passed.
- `python3 -m pytest tests/ -q` → 20 passed (my 9 plus the 11 pre-existing baseline tests).

## What the validator must pay attention to
- `decode` raises `ValueError` for odd length *and* for non-hex characters (including spaces, e.g. `"00 00"`); empty string decodes to `b""`.
- `encode` output is strictly lowercase with no separators; `encode_spaced` uses single spaces and is also lowercase.
- Both acceptance points for errors (`decode("0")`, `decode("zz")`) are covered by `test_decode_odd_length_raises` and `test_decode_non_hex_raises`.
- Only `hexcodec.py` and `tests/test_hexcodec.py` are mine from the code deliverables; the two `team/` files were explicitly mandated by my instructions.
