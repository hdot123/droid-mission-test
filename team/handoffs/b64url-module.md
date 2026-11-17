# Handoff: b64url-module (sub-issue #38)

## What was requested
Implement `b64url.py` (process card for work order #36, sub-issue #38) with:

- `encode(data: bytes) -> str`: URL-safe Base64 per RFC 4648 (`-`/`_` instead of `+`/`/`), all trailing `=` padding removed. Examples: `encode(b"\xfb\xff") == "-_8"`, `encode(b"") == ""`.
- `decode(s: str) -> bytes`: reverse operation; auto-restores missing padding, returns `b""` for `""`, raises `ValueError` on illegal characters or invalid length.
- `tests/test_b64url.py` covering the spec examples, round-trips, padding removal/restoration, empty input, and ValueError cases.
- Only Python stdlib (`base64` allowed); no package directory, no CLI; tests must only test this module.
- Ownership: only `b64url.py` and `tests/test_b64url.py` (plus these team/ files).

## What I did
- Created `b64url.py`:
  - `encode`: accepts bytes-like input, delegates to `base64.urlsafe_b64encode`, then `.rstrip("=")`.
  - `decode`: rejects non-`str` input with `TypeError`; returns `b""` for `""`; tolerates but does not require up to 2 trailing `=` chars (rejects padding that does not make the length a multiple of 4, and more than 2 padding chars); validates every remaining char against the URL-safe alphabet; rejects lengths congruent to 1 mod 4 (one leftover char is never valid); then pads back to a multiple of 4 and decodes, converting any underlying error to `ValueError`.
- Created `tests/test_b64url.py` with 8 tests: spec examples, padding stripping, empty input, padding restoration, round-trips (6 payloads), URL-safe alphabet decode, illegal-character ValueErrors (`+`, `/`, space, mid-string `=`, `==` mid-string, 3 padding chars), and bad-length ValueErrors (len % 4 == 1).

## What I did NOT do
- Did not touch `piglatin.py`, `collatz.py`, their tests, or any other repository file.
- Did not create package directories, `__init__.py`, or a CLI.
- Did not commit or push.

## Checks I ran and results
1. `python -m pytest -q tests/test_b64url.py` → **8 passed** (exit 0).
2. Full suite `python -m pytest -q` (repo root, at time of writing only my tests exist) → **8 passed** (exit 0).
3. Inline check (heredoc equivalent of the process-card command, since the one-liner quoting was mangled by the shell): `encode(b'\xfb\xff')=='-_8'`, `encode(b')==''`, `decode('')==b''`, `decode(encode(b'\xfb\xff'))==b'\xfb\xff'` → **OK**.

Note: pytest was not preinstalled in this environment; I installed it with `pip install pytest` (pytest 9.2.0) to run the required checks.

## What the validator must pay attention to
- The decode contract accepts **optional** trailing `=` padding (e.g. `"Zg=="` and `"Zg"` both decode to `b"f"`); padding is stripped only by `encode`, but `decode` tolerates it. Padding anywhere else, or >2 padding chars, raises `ValueError`.
- Illegal characters are checked explicitly against the RFC 4648 URL-safe alphabet, so `+`, `/`, whitespace, and interior `=` all raise `ValueError` (not `binascii.Error`).
- Bad lengths: any string whose core length is ≡ 1 (mod 4) raises `ValueError`, regardless of padding.
- `decode` raises `TypeError` (not `ValueError`) for non-`str` input; `encode` raises `TypeError` for non-bytes-like input. The spec only constrains `ValueError` for bad chars/lengths.
- Expected example values were verified against `base64.urlsafe_b64encode` directly: `encode(b"\xfb\xff\xfe\xff") == "-__-_w"` and `decode("-_-_") == b"\xfb\xff\xbf"`.
