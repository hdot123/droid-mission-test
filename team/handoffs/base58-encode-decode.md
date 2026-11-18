# Handoff: base58-encode-decode (sub-issue #417)

## What was requested

Process card `base58-encode-decode` under work order #407 (round 43 · batch A):

- Create `base58.py` implementing `b58encode(data: bytes) -> str` and `b58decode(text: str) -> bytes` using the Bitcoin-style alphabet `123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz` (0/O/I/l removed), big-endian byte order, leading `0x00` bytes as leading `1` characters, empty in/out as empty strings, and `ValueError` on out-of-alphabet characters in decode.
- Create `tests/test_base58.py` with a test case for every acceptance item listed on the card.
- Only these two files; standard library only; no import of `fnv1a`/`verhoeff`; no modification of any pre-existing file.
- Checks (verbatim): `python3 -m pytest tests/test_base58.py -q` and `python3 -m pytest tests/ -q`.

## What I did

- Created `base58.py`:
  - `ALPHABET` constant plus an index map for decoding.
  - `b58encode`: rejects non-`bytes` with `TypeError`; strips leading zero bytes, converts the remainder with `int.from_bytes(..., "big")`, repeatedly `divmod(num, 58)` for the body, prepends one `1` per leading zero byte; empty input returns `""`.
  - `b58decode`: rejects non-`str` with `TypeError`; counts leading `1` characters, accumulates `num = num * 58 + digit`, raises `ValueError` (chained from `None`) on any character not in the alphabet, converts back with `to_bytes`, prepends one `0x00` byte per leading `1`; empty input returns `b""`.
- Created `tests/test_base58.py` with 15 tests:
  - Alphabet sanity (58 unique chars, no `0`/`O`/`I`/`l`).
  - One test per acceptance item (9 items): empty encode, `\x00` -> `"1"`, `"hello"` -> `"Cn8eVZg"`, `\x00\x00\x0f` -> `"11G"`, decode of `"Cn8eVZg"`, decode of `""`, decode of `"11G"`, `b58decode("0OIl!")` raises `ValueError`, and round-trip identity on `b"hello"` and `b"\x00\x00\x0f"`.
  - Extra coverage: round-trips over several byte strings (including all 256 single-byte values and `bytes(range(256))`), a few known encodings, and `TypeError` on wrong argument types.

## What I did not do

- Did not touch `fnv1a.py`, `verhoeff.py`, or any pre-existing file (`README.md`, `legacy_stringkit.py`, `roman.py`, `tests/test_legacy_stringkit.py`, `tests/test_roman.py`, etc.).
- Did not import anything outside the standard library (`os`, `sys` in the test file are only for `sys.path` setup; the module itself imports nothing).
- Did not commit or push (left to the workflow).

## Checks run and results

Environment note: the system Python had no `pytest`, so I installed it (`python3 -m pip install --user pytest`, pytest 9.2.0) to run the required checks. No project files were changed by that.

1. `python3 -m pytest tests/test_base58.py -q` -> **PASS**, `15 passed in 0.02s` (exit 0).
2. `python3 -m pytest tests/ -q` -> **PASS**, `26 passed in 0.03s` (exit 0). This is the merged full suite: my 15 plus the 11 pre-existing tests (`test_roman.py`, `test_legacy_stringkit.py`).

## What the validator must pay attention to

- The card's constraint says "only new files"; `base58.py` and `tests/test_base58.py` are the only files I created in the repo, both new. Please confirm no other repo file was modified (git status should show only these two plus this team file and my status file, alongside the pre-existing untracked `worker-prompt.txt` / `worker-stream.jsonl`).
- Decode raises `ValueError` for out-of-alphabet characters; `TypeError` is raised for wrong argument types (spec only mandates `ValueError` for bad characters).
- Encoding of all-zero input (`b"\x00\x00"`) yields `"11"` with no body, which matches Bitcoin-style behavior; decode of `"11"` yields `b"\x00\x00"` — round-trip is symmetric.
- Full-suite check depends on `pytest` being present in the environment (installed here via `--user`).
