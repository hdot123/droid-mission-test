# Handoff: braille (sub-issue #829, 并发 B 单之一)

## What was requested

Create `braille.py` and `tests/test_braille.py` only, for work order #813 第54轮并发B单 (flesch / braille / cssunits), process card `braille` (#829):

- Grade 1 letter-to-dot mapping pinned in the card (a–z → dots 1–6, codepoint = 0x2800 + Σ 2^(dot−1)).
- `to_braille(text) -> str`: non-str raises TypeError; only lowercase a–z and space accepted (space → U+2800 blank cell); any other character raises ValueError; empty string returns empty string.
- `from_braille(text) -> str`: non-str raises TypeError; only the 26 table braille characters plus U+2800 accepted (U+2800 → space); any other character (e.g. U+283F, plain Latin letters) raises ValueError; empty string returns empty string.
- Every acceptance item must have a corresponding test case. Standard library only; no import of flesch/cssunits; only these two files created; no pre-existing file modified.

## What I did

- Created `braille.py`: dot table, letter↔braille maps derived from the pinned dot formula, `to_braille`, `from_braille`. No imports of the other two modules; stdlib not even needed.
- Created `tests/test_braille.py` with one test per acceptance item:
  - `to_braille("a") == "⠁"`, `hello`, `braille`, `abc xyz` (with U+2800 blank cell), empty string.
  - `from_braille("⠓⠑⠇⠇⠕") == "hello"`, phrase roundtrip `from_braille(to_braille("the quick brown fox"))`.
  - All 26 letters: `from_braille(to_braille(ch)) == ch` and `ord(to_braille(ch)) == 0x2800 + Σ 2^(dot−1)` against an independently re-declared dot table in the test file.
  - ValueErrors: `to_braille("Hello")`, `to_braille("abc1")`, `from_braille("⠿")` (U+283F), `from_braille("ab")`.
  - TypeErrors: `to_braille(None)`, `from_braille(5)`.
  - Extras: empty-string `from_braille("")`, space roundtrip via U+2800.

## What I did NOT do

- Did not touch `flesch.py`, `cssunits.py`, or any pre-existing file (repo shows only the two new files plus pre-existing untracked `worker-prompt.txt` / `worker-stream.jsonl`, which are not mine).
- Did not commit or push.
- Did not import flesch or cssunits; braille.py has no module imports.

## Checks run and results

Environment note: `pytest` was not installed in the image; installed per `requirements-dev.txt` via `pip3 install --user -r requirements-dev.txt` (pytest 9.2.0, jsonschema 4.26.0) so the mandated checks could run.

- `python3 -m pytest tests/test_braille.py -q` → **13 passed**, exit 0.
- `python3 -m pytest tests/ -q` → **200 passed, 2 skipped**, exit 0 (full suite; skips pre-existing).
- No `verdict.json` / `verdict.md` by-products appeared in the repo root; cleanup `rm -f verdict.json verdict.md` ran anyway (no-op).

## What the validator must pay attention to

- Only `braille.py` and `tests/test_braille.py` are mine; both are new/untracked. Nothing else was modified.
- The acceptance examples use literal braille characters (e.g. `⠓⠑⠇⠇⠕`, `⠿`, `⠀`); they are pinned as Unicode in the test file and match the card exactly.
- `from_braille("⠿")` (U+283F) must raise ValueError — covered; U+283F is outside the 26-letter table.
- Blank cell is U+2800 (`"⠀"`), distinct from ASCII space, in both directions.
- Full-suite pass count depends on other cards' files landing; at handoff time the suite is green with only my files added.
