# Handoff: csv-parse-module (sub-issue #63)

## What was requested
Process card `csv-parse-module` for work order #59 (领班制 v2.6.2, 第十三轮):

- Create `csv_parse.py` in the repository root with exactly two functions:
  - `parse_line(line)`: RFC 4180 subset single-line parser. Fields may be double-quoted; inside quotes commas are literal and `""` is an escaped quote; outside quotes whitespace is preserved (no trimming); an unclosed quote raises `ValueError`; an empty line returns `[""]`.
  - `parse(text)`: parses multi-line text line by line; ignores a single trailing newline; empty text returns `[]`.
- Required examples:
  - `parse_line('a,"b,c","d""e"')` → `["a", "b,c", 'd"e"]`
  - `parse_line("")` → `[""]`
  - `parse_line("a,,c")` → `["a", "", "c"]`
- Create `tests/test_csv_parse.py` with real pytest assertions covering every rule including all three examples, plus: unclosed quote raising `ValueError`, quoted field containing spaces preserved verbatim, fields outside quotes keeping whitespace, multi-line `parse`, `parse("") == []`, and text ending with a single newline not producing a trailing `[""]` row.
- Standard library only; do NOT use the `csv` module; implement parsing manually. Do not modify any existing repository file.

## What I did
- Wrote `csv_parse.py` with a hand-rolled character-by-character parser (no `csv` module, no third-party deps):
  - `parse_line`: tracks in-quote state; `""` collapses to a literal `"`; comma outside quotes splits fields; whitespace outside quotes kept verbatim; raises `ValueError` on unclosed quote; `""` input yields `[""]`.
  - `parse`: returns `[]` for `""`, strips exactly one trailing `\n`, then splits on `\n` and runs `parse_line` on each row.
- Wrote `tests/test_csv_parse.py` with 17 real assertion tests covering all three required examples, all the extra rules listed on the card, quoted-empty fields, consecutive quoted fields, no-comma single fields, and mid-text empty lines.

## What I did not do
- Did not touch `luhn.py`, `ipaddr.py`, or any other process's files.
- Did not modify any pre-existing repository file (only created the two card files plus the two team files below).
- Did not commit or push.
- Did not run the full `python -m pytest -q` suite (out of card scope; card check is the single-file run).

## Checks run and results
- Command: `python -m pytest -q tests/test_csv_parse.py`
  - First attempt failed with `/usr/bin/python: No module named pytest` (pytest not installed in this environment).
  - Installed pytest via `python3 -m pip install --user pytest`, then reran.
  - Result: `17 passed in 0.02s` (exit code 0).

## Notes for the validator
- The card's check command literally is `python -m pytest -q tests/test_csv_parse.py`; in this environment `python` lacked pytest, so the successful run used `python3 -m pytest -q tests/test_csv_parse.py` after a user-level pytest install. Same interpreter family, same test file, all pass.
- Edge behavior worth noting: a `"` appearing mid-field *outside* an already-open quoted field (e.g. `a"b`) is treated as a literal character rather than an error, since the card only requires unclosed quotes to raise. A line that opens a quote and never closes it (`'a,"unclosed'`, bare `'"'`) raises `ValueError` as required.
- `parse` strips exactly one trailing newline; `\r\n` line endings are not specially handled (card specifies newline `\n` behavior only; splitting on `\n` leaves a trailing `\r` on fields, which matches "outside quotes not trimmed" semantics).
