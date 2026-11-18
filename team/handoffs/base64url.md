# Handoff: base64url (sub-issue #301)

## What was requested

Process card #301 under work order #299 (第三十六轮 · 常规组：领班制 v2.6.5):

- Create `base64url.py`: RFC 4648 base64url codec, no padding.
  - `encode(data: bytes) -> str`: URL-safe alphabet (`-`/`_` instead of `+`/`/`), no `=` padding; empty input returns `""`.
  - `decode(s: str) -> bytes`: inverse; `=` in input raises ValueError; characters outside the alphabet raise ValueError; length mod 4 == 1 raises ValueError.
- Create `tests/test_base64url.py` covering every acceptance example.
- Constraints: only add the two files, touch no existing file, standard library only, no imports from other deliverable modules (isbn10, semvercmp).

## What I did

- `base64url.py` (new): `encode` strips `=` padding from `base64.urlsafe_b64encode`; `decode` rejects `=`, validates every character against the base64url alphabet, rejects length mod 4 == 1, then re-pads and decodes via `base64.b64decode` with a `-/` → `+/` translation. Uses only `base64` from the standard library.
- `tests/test_base64url.py` (new): 9 tests covering every acceptance example —
  `encode(b"") == ""`, `encode(b"hello") == "aGVsbG8"`, `encode(b"\xfb\xff") == "-_8"`,
  `decode("aGVsbG8") == b"hello"`, `decode("-_8") == b"\xfb\xff"`,
  `decode("aGVsbG8=")` raises ValueError, `decode("a")` raises ValueError,
  round-trip identity for `b""`, `b"\x00"`, `b"foobar"`,
  plus out-of-alphabet rejection (`+`, `/`, `*`, space).

## What I did NOT do

- Did not create `isbn10.py`, `semvercmp.py`, or their tests (other process cards own those).
- Did not modify any pre-existing file (`README.md`, `roman.py`, `legacy_stringkit.py`, `tests/test_roman.py`, `tests/test_legacy_stringkit.py`).
- Did not commit or push.

## Checks run and results

Environment note: pytest was not installed; I installed it with `python3 -m pip install --user pytest` (pytest 9.2.0) so the required checks could run.

1. `python3 -m pytest tests/test_base64url.py -q` → `9 passed`, exit 0.
2. `python3 -m pytest tests/ -q` → `20 passed`, exit 0 (11 pre-existing baseline tests + my 9).

Both checks pass.

## Notes for the validator

- Untracked `__pycache__/` directories are pytest bytecode caches; they are not deliverables and are not tracked in git.
- Untracked `worker-prompt.txt` / `worker-stream.jsonl` predate my work and were not touched.
- `git status` shows only the intended new files (`base64url.py`, `tests/test_base64url.py`) plus the two team files requested by the workflow; no existing file is modified.
- The full-suite count (20) assumes no other deliverables are present at check time; if isbn10/semvercmp land first, the total will grow accordingly — my 9 tests still pass either way.
