# Handoff: base32hex-codec (sub-issue #317)

## What was requested
Process card `base32hex-codec` under work order #312 (第三十八轮 · 并发 A 单): create two new files only —
`base32hex.py` (RFC 4648 Base32hex encoder/decoder) and `tests/test_base32hex.py` — using only the
standard library, without touching any existing file, without importing `crc8` or `manchester` or any
non-stdlib module. Every acceptance point must have a corresponding test case.

## What I did
- Created `base32hex.py`:
  - `encode(data: bytes) -> str`: Base32hex alphabet `0123456789ABCDEFGHIJKLMNOPQRSTUV`, MSB-first
    bit packing, `=` padding to a multiple of 8 characters. `b""` encodes to `""`.
  - `decode(text: str) -> bytes`: inverse operation. Raises `ValueError` for non-str input,
    total length not a multiple of 8, `=` appearing inside the body (misplaced padding), more than 6
    pad chars, pad counts that don't match a legal body length (body % 8 in {1, 3, 6}), characters
    outside the alphabet, and non-zero trailing (unused) bits per RFC 4648 §6.
- Created `tests/test_base32hex.py` with 15 tests covering every acceptance point:
  all six RFC vectors (`f`, `fo`, `foo`, `foob`, `fooba`, `foobar`), `encode(b"") == ""`,
  `decode("CPNMUOJ1E8======") == b"foobar"`, round-trip identity on `b"\x00\xff\x10"`,
  round-trips at all lengths 0–7, plus ValueError cases for out-of-alphabet characters,
  non-conforming padding (misplaced pad, illegal pad counts), non-conforming length, and
  non-zero trailing bits.
- Installed `pytest` (9.2.0) into the environment — it was not present (`python3 -m pytest` reported
  "No module named pytest"). No repository files were changed by the install.

## What I did not do
- Did not create or modify `crc8.py`, `manchester.py`, or their tests (owned by other processes).
- Did not modify any pre-existing file (`roman.py`, `legacy_stringkit.py`, `README.md`,
  `tests/test_roman.py`, `tests/test_legacy_stringkit.py`, `.github/`, `team/` files of others).
- Did not touch `worker-prompt.txt` / `worker-stream.jsonl`.
- Did not commit or push.

## Checks run and results
1. `python3 -m pytest tests/test_base32hex.py -q` → **15 passed**
2. `python3 -m pytest tests/ -q` → **26 passed** (15 mine + 11 pre-existing)

## Notes for the validator
- The only environment change was `python3 -m pip install pytest` (pytest 9.2.0 on Python 3.14).
- Strict decode choices beyond the literal spec: total length must be a multiple of 8 (covered by
  acceptance "non-conforming length"), pad count > 6 and body % 8 ∈ {1,3,6} are rejected as
  non-conforming padding, and non-zero unused trailing bits are rejected (RFC 4648 §6). All raise
  `ValueError` as required.
- Test file imports are `from base32hex import decode, encode` — consistent with the existing
  `from roman import ...` style; no cross-module imports.
