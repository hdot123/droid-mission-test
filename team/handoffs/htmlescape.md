# Handoff: htmlescape (sub-issue #881, work order #877 B 单)

## What was requested

Process card `htmlescape` for round 56 work order #877 (concurrent B ticket). Implement
`htmlescape.py` with two functions and `tests/test_htmlescape.py` covering every listed
acceptance item. Create only these two project files, plus this handoff and
`team/status/htmlescape.json`. Standard library only, no imports of other project
modules, no modification of any existing file. Entity syntax note: this note avoids
writing literal HTML entity spellings because file content in this pipeline gets
HTML-entity-decoded on write; entities are described by name instead.

## What I did

- Created `htmlescape.py`:
  - `escape_html(text: str) -> str`: chained literal `str.replace` calls in the required
    order — ampersand first, then `<`, `>`, double quote, then single quote written as
    the hex numeric entity for codepoint 27. Non-str input raises `TypeError`.
  - `unescape_html(text: str) -> str`: one compiled `re` pattern matches a
    semicolon-terminated reference: decimal numeric, hex numeric (x/X prefix), or
    ASCII-letter named. Named table covers exactly amp, lt, gt, quot, apos (each
    decodes single-char results). Numeric results keep surrogates (U+D800–U+DFFF) and
    anything above U+10FFFF verbatim; so do unknown names, missing semicolons, and
    failed int() parses (e.g. absurdly long digit runs). Non-str raises `TypeError`.
  - Because escape writes the single quote as hex 27 and unescape recognizes amp-style
    named `apos`, decimal 39, and hex 27, the required round-trip and three-spelling
    behavior both hold.
  - Entity literals are built by string concatenation (`"&" + "amp;"` etc.) so no
    contiguous entity text appears in the source; see hazard below.
- Created `tests/test_htmlescape.py` with one test per acceptance item (10 test
  functions, 40+ assertions): empty/plain escape, the full tag sample, re-escaping
  pre-existing entity text, named unescape including all three single-quote
  spellings, decimal+hex (`ABC`), unknown entity, missing semicolon,
  surrogate and out-of-range codepoints, no-entity input, round-trip over the three
  sample strings, and both `TypeError` cases. All entity constants in the test are
  assembled at runtime from `chr(38)` so the test source itself contains no literal
  entity spellings.
- Ran both process checks from the repository root (see below); both pass.

## What I did not do

- Did not touch `stirling2.py`, `segdist.py`, or their tests (other cards own them).
- Did not modify any pre-existing file; only the four new files exist as my output:
  `htmlescape.py`, `tests/test_htmlescape.py`, this handoff, `team/status/htmlescape.json`.
- Did not commit or push (workflow does that).
- Did not run the other rounds' gates; only the two checks listed on the card.

## Checks and results

1. `python3 -m pytest tests/test_htmlescape.py -q` → `10 passed in 0.01s`
2. `python3 -m pytest tests/ -q` → `352 passed, 2 skipped in 17.59s`

No `verdict.json` / `verdict.md` byproducts existed after the runs; verified and
`rm -f verdict.json verdict.md` executed anyway.

## Notes for the validator

- **Entity-decoding hazard:** file content written through this environment's tools
  gets HTML-entity-decoded (a literal `&` written to a file lands as `&`).
  I verified raw bytes on disk with `python3 -c` reads: all entity spellings in
  `htmlescape.py` are split across concatenations (`"&" + "amp;"`), so the source on
  disk is correct. If you grep the file, expect entities only in that split form.
  Likewise, this handoff and the status JSON deliberately contain no literal
  entity spellings for the same reason.
- The `escape`/`unescape` asymmetry from the spec is intentional: escape emits hex 27
  for the single quote; unescape accepts named `apos`, decimal 39, and hex 27.
- Round-trip holds for the required sample set because unescape decodes hex 27 back to
  the original character.
- Unescape treats a reference as valid only with a trailing semicolon (`&` with no
  semicolon stays verbatim), per spec.
- No file imports another project module; only `re` from the standard library is used.
