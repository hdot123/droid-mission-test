# Handoff: textnorm-module (sub-issue #154)

## What was requested
Process card `textnorm-module`: implement `textnorm.py` with `normalize(text)` and `tests/test_textnorm.py`, per the work order #144 specs (round 25 pre-split P-card, foreman v2.6.5).

Spec for `normalize(text)`, applied in order:
1. Lowercase the text.
2. Delete characters that are neither letters, digits, nor whitespace.
3. Collapse runs of whitespace (spaces, newlines, tabs, etc.) into a single space.
4. Strip leading/trailing whitespace.

Example: `normalize("  Hello,   World!\nIt's 2026. ")` → `"hello world its 2026"` (note: the apostrophe in "It's" is removed, so "its" is one word).

Constraints: Python standard library only; no imports of `wordfreq`/`sentstats`; no package directory; no CLI; this test file only tests `textnorm`.

## What I did
- Created `textnorm.py` with `normalize(text)` implementing the four steps in order (lowercase → delete non-alphanumeric/non-whitespace → collapse whitespace → strip). Uses only `re` from the standard library.
- Created `tests/test_textnorm.py` with 5 tests covering each of the four rules individually plus the exact spec example:
  - `test_lowercase`
  - `test_delete_non_alphanumeric_non_whitespace` (includes the `It's` → `its` apostrophe case)
  - `test_collapse_whitespace`
  - `test_strip_ends`
  - `test_spec_example`
- Installed `pytest` into the environment (`python -m pip install pytest`) because it was not preinstalled; no repository files were changed by that.

## What I did not do
- Did not create or touch `wordfreq.py`, `sentstats.py`, or their test files.
- Did not touch any `team/` system-management files other than my own `team/handoffs/textnorm-module.md` and `team/status/textnorm-module.json`.
- Did not create package directories, CLI entry points, or any imports between the three modules.
- Did not commit or push.

## Checks run and results
Per the process card checks (in order, verbatim commands):

1. `python -m pytest -q tests/test_textnorm.py` → **PASS** (`..... [100%]` / `5 passed in 0.01s`)
2. `python -m pytest -q` → **PASS** (`..... [100%]` / `5 passed in 0.01s`)

Note: the full suite currently contains only this module's tests; other workers' files may land later and will be included when the suite is re-run at integration time.

## For the validator
- The single spec example passes exactly: `normalize("  Hello,   World!\nIt's 2026. ") == "hello world its 2026"`.
- Order of operations matters: lowercase first, then delete punctuation, then collapse whitespace. The implementation follows that order literally.
- `textnorm.py` imports only `re` (standard library) and does not import `wordfreq` or `sentstats`.
- `tests/test_textnorm.py` imports only `textnorm`.
