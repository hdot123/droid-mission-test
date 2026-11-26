# Handoff: asciitable (sub-issue #914, work order #904 D 单)

## What was requested

Process card `asciitable` from work order #904 (round 57, D-unit: lfucache / asciitable / ngrams). Own **only** two new files:

- `asciitable.py` — `render_table(headers, rows) -> str`: ASCII table output rendering.
- `tests/test_asciitable.py` — tests covering every acceptance item.

Scope constraints honored: only these two files created at the repo root / tests/; no existing repository file modified; standard library only; no imports of `lfucache` / `ngrams` or any other round-57 module; nothing written under `team/` other than this card's own handoff/status files.

## What I did

Implemented `render_table` per the pinned spec:

- Border rows `+---+` style: each column contributes `"+" + "-" * (col_width + 2)`, columns joined with `"+"`.
- Cells padded with one space each side (`| a |`), everything left-aligned.
- Column width = longest of the header **and** all cells in that column (headers and cells in the same width computation).
- Separator border directly below the header; **no** separators between data rows; closing border at the end.
- Lines joined with `"\n"`, **no trailing newline**; empty `rows` renders the header section only.
- Total line count is always `len(rows) + 4`.

Validation (each with a test):

- empty `headers` → `ValueError` (`render_table([], [])`).
- row length ≠ header column count → `ValueError` (`render_table(["a"], [["1", "2"]])`).
- non-`str` header/cell → `TypeError` (`render_table(["a"], [[1]])`, `render_table([1], [])`).
- `headers`/`rows` not in list form, including `headers` being a `str` → `TypeError` (`render_table("ab", [])`). Also covered: `rows` not a list, and a row that is not a list.

Tests cover every acceptance example verbatim:

- `render_table(["a", "bb"], [["ccc", "d"]])` equals the exact five-line string.
- `render_table(["x"], []) == "+---+\n| x |\n+---+\n+---+"`.
- Properties: line count == `len(rows) + 4`, all lines equal length, no trailing newline.
- All five error cases with `pytest.raises`.
- Extra structural checks: width grows with data cells, separator appears only below the header (no inter-data-row borders).

## What I did not do

- Did not touch `lfucache.py`, `ngrams.py`, or any pre-existing repository file (read-only inspection of `roman.py`/`tests/` for style only).
- Did not create anything under `team/` besides this card's `team/handoffs/asciitable.md` and `team/status/asciitable.json`.
- Did not commit or push.
- Did not implement csv-family parsing (this card is output rendering only).

## Checks run

- `python3 -m pytest tests/test_asciitable.py -q` → **14 passed** (exit 0).
- `python3 -m pytest tests/ -q` → **356 passed, 2 skipped** (exit 0).

No `verdict.json` / `verdict.md` by-products were produced by these runs (verified after run; removed with `rm -f` if present).

## What the validator must pay attention to

- The empty-table example `render_table(["x"], [])` intentionally renders `"+---+\n| x |\n+---+\n+---+"` — the separator and closing border are both present even with no data rows; this is the spec's verbatim expectation (total lines = `len(rows) + 4` = 4).
- Line count check uses `split("\n")`, which counts `len(rows) + 4` only because there is no trailing newline — both properties are asserted together.
- Type errors take precedence over value errors only where specified: non-list `headers` raises `TypeError` before the empty check; empty list `headers` raises `ValueError`.
