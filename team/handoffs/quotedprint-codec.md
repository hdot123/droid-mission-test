# Handoff: quotedprint-codec (sub-issue #321)

## What was requested
Process card `quotedprint-codec` for work order #313 (第三十八轮 · 并发 B 单): implement a simplified Quoted-Printable codec as `quotedprint.py` plus `tests/test_quotedprint.py`. Scope is strictly those two new files; no edits to any existing file, standard library only, no imports of other project modules.

Spec (verbatim from the work order):
- `encode(data: bytes) -> str`: bytes in range 33-60, 62-126 (printable ASCII except `=`) output as-is; all other bytes (including `=`, space, tab, non-ASCII) encoded as `=XX` with uppercase hex; no soft line breaking (line-length handling explicitly excluded this round).
- `decode(text: str) -> bytes`: the inverse; if `=` is not followed by exactly two hex digits, raise `ValueError`.

## What I did
- Created `quotedprint.py` at the repo root with `encode` and `decode`.
  - `encode` emits a character as-is when `33 <= b <= 60 or 62 <= b <= 126`, otherwise `=XX` with uppercase hex from a fixed `0123456789ABCDEF` table.
  - `decode` scans left to right: `=` consumes exactly two following characters via `int(pair, 16)` (raises `ValueError` for `=ZZ`, trailing `=`, and incomplete escapes like `a=3`); non-escape characters with `ord > 127` also raise `ValueError` since only ASCII text is a valid decode input under this spec.
  - Accepts `bytes`/`bytearray`/`memoryview` in `encode` (spec type is `bytes`; extras are harmless) and requires `str` in `decode`.
- Created `tests/test_quotedprint.py` covering every acceptance point plus the required `ValueError` cases:
  - `encode(b"a=b") == "a=3Db"`, `encode("café".encode("utf-8")) == "caf=C3=A9"`, `encode(b"a b") == "a=20b"`, `encode(b"plain") == "plain"`, `decode("a=3Db") == b"a=b"`, round-trip identity for `b"\x00\xff abc="`.
  - Extra: tab/control byte encoding (`a\tb` -> `a=09b`, `\x00` -> `=00`), plain decode, and `ValueError` on `"=ZZ"`, trailing `"="`, and incomplete `"a=3"`.

## What I did not do
- Did not touch `pctform.py`, `hexcodec.py`, or their tests (other processes own those).
- Did not modify any pre-existing file (`README.md`, `roman.py`, `legacy_stringkit.py`, existing tests, CI config, etc.).
- Did not add soft line breaking / line-length handling (explicitly out of scope this round).
- Did not commit or push.
- Did not add tests for pctform/hexcodec.

## Checks run and results
1. `python3 -m pytest tests/test_quotedprint.py -q` -> `11 passed in 0.02s`
2. `python3 -m pytest tests/ -q` -> `22 passed in 0.03s` (full suite, includes pre-existing roman/stringkit tests; no regressions)

Note: the environment had no `pytest` module initially (`No module named pytest`); I installed it with `pip3 install pytest` (pytest 9.2.0) so the mandated checks could run. This is an environment setup step only, no repo files changed by it.

## What the validator must pay attention to
- Only two repo files were added by this process: `quotedprint.py` and `tests/test_quotedprint.py`. Verify `git status` shows no modifications to existing files from this card.
- The handoff/status files `team/handoffs/quotedprint-codec.md` and `team/status/quotedprint-codec.json` are also written per instructions (team files, not part of the six deliverable files).
- Spec edge: `decode` rejects non-ASCII input characters with `ValueError`; the spec only defines `=XX` escapes and ASCII passthrough, so raw non-ASCII in decode input is treated as invalid. Round-trip tests pass because `encode` always escapes non-ASCII.
- Spec edge: no line-length/soft-break handling in either direction, per the round's explicit exclusion.
- All six acceptance points for quotedprint have corresponding test cases; `decode` `ValueError` behavior is covered by three cases.
