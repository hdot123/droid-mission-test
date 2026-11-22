# Handoff: ipv4kit (sub-issue #329)

## What was requested
Process card #329 under work order #314 (第三十八轮 · 并发 C 单). Create only `ipv4kit.py` and `tests/test_ipv4kit.py`:

- `parse(text: str) -> int`: strict dotted-quad, exactly 4 segments, each a decimal integer 0–255. Reject leading zeros in every segment (the digit `"0"` itself is allowed). Raise `ValueError` for wrong segment count, non-digit characters, any space, out-of-range value, or a leading zero. Return a 32-bit integer with the first segment as the most significant byte.
- `format(value: int) -> str`: inverse of `parse`; raise `ValueError` if value is not in 0–4294967295 inclusive.
- Every acceptance criterion from the card must have a corresponding test.

## What I did
- Created `ipv4kit.py` (standard library only, no imports from other deliverables). Implementation notes:
  - `parse` splits on `.` and requires exactly 4 segments; each segment must be non-empty, contain only ASCII `0`–`9` (checked char by char, so spaces and any non-digit such as `a`, `+`, or Unicode digits are rejected), must not start with `0` unless it is exactly `"0"`, and must be ≤ 255. Segments are accumulated as `(value << 8) | number`, first segment as most significant byte.
  - `format` range-checks 0–4294967295 inclusive, then emits four octets extracted with shifts/masks.
  - Non-`str` input to `parse` also raises `ValueError`.
- Created `tests/test_ipv4kit.py` with a test for every acceptance criterion plus extra edge cases:
  - `parse("192.168.0.1") == 3232235521`; `parse("0.0.0.0") == 0`; `parse("255.255.255.255") == 4294967295`
  - `format(3232235521) == "192.168.0.1"`
  - `ValueError` for `"01.2.3.4"`, `"256.0.0.1"`, `"1.2.3"`, `"1.2.3.4 "` (trailing space)
  - round-trip identity for `"10.20.30.40"`
  - extras: leading zero in a middle segment, too many segments, empty string, non-digit, `+` sign, internal space, empty segment, `format(-1)`, `format(4294967296)`, `format(0)`, `format(4294967295)`, and sampled round-trips over boundary values.

## What I did NOT do
- Did not touch `duration.py`, `macaddr.py`, or their tests (owned by other processes).
- Did not modify any pre-existing file (`roman.py`, `legacy_stringkit.py`, `README.md`, `tests/test_roman.py`, `tests/test_legacy_stringkit.py`, `worker-prompt.txt`, `worker-stream.jsonl`).
- Did not commit or push.
- Did not add any imports beyond none at all in `ipv4kit.py` (the test file imports only `pytest` and `ipv4kit`).

## Checks run and results
- `python3 -m pytest tests/test_ipv4kit.py -q` → **29 passed** (exit 0)
- `python3 -m pytest tests/ -q` → **40 passed** (exit 0)

Note: `pytest` was not installed in the environment; I installed it with `python3 -m pip install pytest` (version 9.2.0) to run the required checks. No repository files were changed by that install.

## What the validator must pay attention to
- Spec fidelity: leading zeros are rejected only when a segment is longer than one character and starts with `"0"`; `"0"` alone is valid. Spaces anywhere (including trailing) are rejected because they are non-digit characters or produce wrong segment content.
- `"1.2.3.4 "` fails because the last segment `"4 "` contains a space (non-digit), matching the card's trailing-space rule.
- Non-ASCII digits (e.g. Arabic-Indic numerals) are rejected: the digit check is ASCII-only by design, stricter than `str.isdigit()`.
- `format` is inclusive of both bounds 0 and 4294967295.
- No cross-module imports exist; the module is self-contained.
