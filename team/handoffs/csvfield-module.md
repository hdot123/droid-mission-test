# Handoff: csvfield-module (sub-issue #326)

## What was requested
Implement the RFC 4180 single-field codec as process card `csvfield-module` under work order #315 (round 38, concurrent batch D):
- `csvfield.py` with `encode(field: str) -> str` and `decode(text: str) -> str`.
- `tests/test_csvfield.py` covering every acceptance example plus the card's extra cases.
- Only these two new files; no existing file modified; standard library only; no imports of `wordwrap` or `slugify`.

Spec (verbatim from the card):
- `encode`: wrap in double quotes when the field contains a comma, a double quote, or a newline (`\n` or `\r`); internal double quotes become two; otherwise return as-is.
- `decode`: inverse; unquoted text returned as-is; quoted text must be paired with nothing after the closing quote; internal `""` decodes to `"`; unclosed quotes or trailing characters after the closing quote raise `ValueError`.

## What I did
- Created `csvfield.py` (new): `encode` checks for `,`, `"`, `\n`, `\r` and quotes/doubles as needed; `decode` parses a leading `"` manually — `""` collapses to `"`, a lone `"` ends the field (error if characters follow), and an unterminated field raises `ValueError`.
- Created `tests/test_csvfield.py` (new), 10 test functions covering all card acceptance points:
  - `encode("plain") == "plain"`, `encode("a,b") == '"a,b"'`, `encode('a"b') == '"a""b"'`
  - `decode('"a""b"') == 'a"b'`, `decode("plain") == "plain"`
  - round-trip identity for `x,"y"\nz`
  - `\n` and `\r` newlines both trigger quoting (card's extra requirement)
  - `decode` raises `ValueError` for unclosed quote (`"abc`) and trailing characters after closing quote (`"abc"def`)
  - an extra round-trip sweep over edge fields (`""`, bare `"`, `""` etc.)

## What I did not do
- Did not touch any pre-existing file (`roman.py`, `legacy_stringkit.py`, `README.md`, `tests/test_roman.py`, `tests/test_legacy_stringkit.py`, `worker-prompt.txt`, `worker-stream.jsonl`).
- Did not create or edit `wordwrap.py`, `slugify.py`, or their tests (owned by sibling processes).
- Did not import `wordwrap` or `slugify` anywhere.
- Did not commit or push.

## Checks run (from repository root)
- `python3 -m pytest tests/test_csvfield.py -q` → **10 passed**
- `python3 -m pytest tests/ -q` → **21 passed** (includes existing roman/legacy suites)

Note: the environment had no pytest initially; I installed `pytest 9.2.0` via `pip3 install --user pytest` so the mandated checks could run. No other environment changes.

## Validator attention points
- `decode` intentionally accepts only fields that either do not start with `"` (returned verbatim, including any stray quotes later in the text) or start with `"` (must be fully consumed). Trailing junk after a closing quote raises `ValueError`, per spec.
- `encode` quotes on `\r` as well as `\n` (spec: "换行（\n 或 \r）").
- Empty string round-trips: `encode("") == ""`, `decode("") == ""` (empty is not quoted since it contains no specials).
- Both files are new; the only files added by this process are `csvfield.py`, `tests/test_csvfield.py`, plus the two team files under `team/`.
