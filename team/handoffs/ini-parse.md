# Handoff: ini-parse (sub-issue #68)

## What was requested
Implement `ini_parse.py` in the repository root plus `tests/test_ini_parse.py`, per process card #68 (work order #66, 领班制 v2.6.2 round 14).

Module requirements:
- `parse(text)` -> dict mapping section name -> dict of key -> value, with rules: line whitespace stripped; blank lines and full-line `;`/`#` comments ignored; `[name]` headers (name stripped, case-sensitive); `key = value` / `key: value` lines (key stripped + lowercased, value stripped); pre-section keys go into `"DEFAULT"`; repeated key overwrites; repeated section header merges; value wrapped in one matching pair of double quotes is unwrapped with no escape processing; a line with neither `=` nor `:` (not header/blank/comment) raises `ValueError` whose message contains the line number; empty text returns `{}`.
- `get(text, section, key, default=None)`: section names case-sensitive, keys case-insensitive, returns `default` when missing.
- Standard library only; no imports of `urlencode` or `glob_match`; no package directory; no CLI.

## What I did
- Created `ini_parse.py` with `parse()` and `get()` implementing every rule above.
- Created `tests/test_ini_parse.py` covering: empty text, whitespace/blank lines, full-line comments, header name stripping + case sensitivity, `=` and `:` separators, key lowercasing/value stripping, `DEFAULT` section, repeated-key overwrite, repeated-section merge, quote stripping (including unbalanced/escaped-quote no-processing cases), `ValueError` with line number (both mid-text and first line), all three required examples, and `get()` default/case behavior (18 tests total).

## What I did not do
- Did not create or modify `urlencode.py`, `glob_match.py`, or any other repository file.
- Did not create package directories or a CLI.
- Did not commit or push.
- (Note: `pytest` was not installed in the environment; I installed it via pip solely to run the required check.)

## Checks run and results
1. `python -m pytest -q tests/test_ini_parse.py`
   - Output: `..................                                                       [100%]` / `18 passed in 0.02s` (exit 0)
2. `python -c "import ini_parse; assert ini_parse.parse('[a]\nX = 1\n') == {'a': {'x': '1'}}; assert ini_parse.get('k = v', 'DEFAULT', 'K') == 'v'"`
   - Output: none (exit 0) — passes verbatim from repository root.

## Notes for the validator
- Quote rule is implemented as "starts and ends with a matching pair of double quotes" — only the outer pair is stripped, no escape processing (e.g. `q = "a\"b"` keeps the inner backslash and quotes as literal text after outer strip).
- Line numbers in `ValueError` messages are 1-based over `text.split("\n")`.
- `get()` returns `default` when either the section or the key is missing (section lookup is case-sensitive; key lookup is lowercased).
