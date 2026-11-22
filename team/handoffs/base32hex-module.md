# Handoff: base32hex-module (sub-issue #258)

## What was requested

Work order #245, process card `base32hex-module` (sub-issue #258), scope limited to exactly two files:

- `base32hex.py`: RFC 4648 Base32hex codec. Alphabet `0123456789ABCDEFGHIJKLMNOPQRSTUV`, `=` padding to a multiple of 8. `encode(data: bytes) -> str`, `decode(s: str) -> bytes`. `decode` accepts only uppercase alphabet chars with `=` padding at the end; raises `ValueError` when length is not a multiple of 8, any char is outside the alphabet (including lowercase), `=` appears in a non-final position, or pad count is invalid (valid pad counts: 0, 1, 3, 4, 6). All listed examples must hold (`encode(b"f") == "CO======"` … `decode("CPNMUOJ1") == b"fooba"`).
- `tests/test_base32hex.py`: tests covering only `base32hex.py`, including every example and every `ValueError` case.

Constraints: Python standard library only; the three modules must not import each other; no package directory; no CLI.

## What I did

- Implemented `base32hex.py` with a pure-stdlib implementation:
  - `encode`: chunks input into 5-byte groups, left-aligns each group to 40 bits, emits 8 five-bit characters, then replaces characters beyond `ceil(8n/5)` of each chunk with `=`.
  - `decode`: validates `str` type, length multiple of 8, `=` only in a trailing run, pad count in {0, 1, 3, 4, 6}, and every body char in the alphabet (uppercase only, via an exact lookup dict). Decodes via 5-bit accumulation and drops leftover bits (which are guaranteed zero since `encode` zero-fills them).
- Wrote `tests/test_base32hex.py` (9 tests): all 7 encode examples, all 7 matching decode examples, output length is a multiple of 8 for inputs 0–23 bytes, roundtrip for inputs 0–39 bytes, length-not-multiple-of-8, out-of-alphabet (lowercase `w`, `W`-equivalent edge via `W` which is past V in alphabet, `@`, space), `=` in non-final position, invalid pad counts (7, 5, 2, 8), and valid pad counts (6, 4, 3, 1, 0).

## What I did NOT do

- Did not touch `crc8.py`, `manchester.py`, or any other test file (owned by sibling processes).
- Did not create a package directory, no CLI, no third-party dependencies.
- Did not commit or push (workflow handles that).

## Checks run and results

| Command | Result |
| --- | --- |
| `python -m pytest -q tests/test_base32hex.py` | **9 passed in 0.02s** (exit 0) |

Note: the environment had no pytest preinstalled; I installed it with `python3 -m pip install --user pytest` (pytest 9.2.0) so the mandated check command could run. This is environment setup only, no repo files changed by it.

## What the validator must pay attention to

1. **Alphabet is hex-flavored Base32**, not the standard RFC 4648 Base32 (`A-Z2-7`): `encode(b"f")` is `CO======`, not `MY======`. Decode rejects lowercase — `decode("cpnmuoj1")` must raise `ValueError`.
2. **Valid pad counts are exactly {0, 1, 3, 4, 6}**: `decode("C=======")` (pad 7), `"CPN====="` (pad 5), `"CPNMUO=="` (pad 2), `"========"` (pad 8) all raise `ValueError`, per the spec's explicit rule. This differs from a naive "pad 1–6 allowed" reading; the work order says otherwise, so 5 and 2 are rejected.
3. **`=` in a non-final position** raises (`"=PNMUOJ1"`, `"CP=NMUO1"`), and a trailing run containing any non-`=` char after the first `=` also raises (`"CO======X"` is caught by the non-multiple-of-8 rule; `"CPN====X"`-style would be caught by the trailing-run rule).
4. Scope check: only `base32hex.py`, `tests/test_base32hex.py`, and these two team files were created. The other two modules/tests are owned by sibling processes of work order #245.
