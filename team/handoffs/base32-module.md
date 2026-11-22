# Handoff: base32-module (sub-issue #51)

## What was requested
- Process card for work order #47 (第十一轮 · v2.6.2): implement `base32.py` plus `tests/test_base32.py`, owning only those two files.
- `encode(data: bytes)` — RFC 4648 standard Base32 (uppercase A-Z plus 2-7, `=` padding); `encode(b"foo") == "MZXW6==="`, `encode(b"") == ""`.
- `decode(s)` — strict inverse: must be canonical uppercase with padding; `ValueError` on illegal characters or bad padding; `decode("") == b""`, `decode("MZXW6===") == b"foo"`.
- Standard library only; no imports of other project modules; no package directory; no CLI.
- Test coverage: spec examples, RFC 4648 vectors, round trips for remainder lengths 0-7 (tested 0-11), lowercase/unpadded/illegal-char rejections, empty input/output.

## What I did
- Created `base32.py` implementing `encode` (delegates to stdlib `base64.b32encode`) and `decode` (validates a strict regex `\A[A-Z2-7]+={0,6}\Z`, rejects non-string input, verifies total length is a multiple of 8 and that the trailing `=` count matches the canonical pad length for the final group, then decodes with `base64.b32decode`). `ValueError` is raised for all invalid inputs; `binascii.Error` (a `ValueError` subclass) is re-raised as `ValueError`.
- Created `tests/test_base32.py` (29 tests): spec examples, full RFC 4648 test-vector table, round trips for byte lengths 0-11 (covers all 8 remainders), and rejection cases for lowercase, unpadded, wrong-length padding, illegal characters (`8`, `!`), padding in the middle, plus `TypeError` for non-bytes `encode`.

## What I did NOT do
- Did not touch `levenshtein.py`, `semver.py`, their tests, or any other process's files.
- Did not create a package directory, CLI, or any inter-module imports.
- Did not commit or push (per workflow).

## Checks run
- `python -m pytest -q tests/test_base32.py` → **29 passed in 0.02s** (exit 0).
- Note: pytest was not present in the environment; it was installed with `pip install pytest` (pytest 9.2.0) to run the process check.

## Notes for the validator
- `decode` intentionally accepts only strict canonical form: uppercase only, no lowercase, no missing padding, no extra padding, alphabet exactly `[A-Z2-7]`. Non-string input also raises `ValueError` (not `TypeError`) so callers see a uniform error type for invalid input.
- Padding validation is structural (multiple of 8; pad count matches the remainder class), so e.g. `"MZXW6"` (unpadded), `"MZXW6=="` (too short), and `"MZXW68=="` (`8` not in alphabet) all raise `ValueError`.
- `base32.py` imports only `base64` and `re` from the standard library; it does not import `levenshtein` or `semver`.
