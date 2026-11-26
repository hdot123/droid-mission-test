# Handoff: unaccent (sub-issue #895)

## What was requested

Work order #876 第56轮 A 单, process card `unaccent`: implement the accent-stripping component as two new files only:

- `unaccent.py` — module with `strip_accents(text: str) -> str`.
- `tests/test_unaccent.py` — tests covering every acceptance point verbatim.

Spec: NFD decomposition, delete all combining marks with category `Mn`, recompose with NFC. Letters with no decomposition mapping (æ / ø / đ etc.) are preserved as-is (explicitly specified). Non-`str` input raises `TypeError`. Standard library only; must not import `kruskal` or `energyconv`.

## What I did

- Created `unaccent.py` at the repository root: `strip_accents` normalizes to NFD, filters out every character whose `unicodedata.category` is `Mn`, then normalizes to NFC. Raises `TypeError` for non-`str` input (including `None`, which is not caught by the `isinstance(text, str)` guard).
- Created `tests/test_unaccent.py` with one test function per acceptance grouping, transcribing the spec's values verbatim:
  - basic accents (`café`, `naïve`, `Zürich`, `résumé`, `Ångström`, `niño`, `čau`, `őrség`, `tiếng Việt`, `İstanbul`)
  - preserved no-mapping letters (`Æsop`, `smørrebrød`)
  - plain/edge inputs (`plain ascii`, `""`, `東京`)
  - decomposed spelling `e\u0301` → `"e"`
  - both spellings of Å (`\u00c5` and `A\u030a`) both → `"A"`
  - phrases (`crème brûlée`, `façade`, `señor`)
  - properties: no `Mn` in output, idempotence, NFD/NFC input spellings agree
  - `TypeError` for `123` and `None`

## What I did NOT do

- Did not modify any existing repository file (only created the six-deliverable pair owned by this card plus the two required team files under `team/`).
- Did not create or touch `kruskal.py`, `energyconv.py`, or their tests (owned by other processes in this work order).
- Did not commit or push.
- No cross-imports between the three components; standard library only.

## Checks run and results

From the repository root:

1. `python3 -m pytest tests/test_unaccent.py -q` → **10 passed** in 0.01s
2. `python3 -m pytest tests/ -q` → **352 passed, 2 skipped** in 17.60s (suite exits 0)

The 2 skips are pre-existing suite skips unrelated to this card.

## Notes for the validator

- `unaccent.py` is a new root-level module; tests import it as `from unaccent import strip_accents`, matching the existing convention (`from roman import ...` in `tests/test_roman.py`). No `conftest.py` changes were needed.
- The spec's decomposed-spelling acceptance points use literal escape sequences (`"e\u0301"`, `"\u00c5"`, `"A\u030a"`); the test file writes them as real Unicode characters, which is exactly equivalent.
- `verdict.json` / `verdict.md` pipeline by-products were checked for and are not present in the working tree.
- Full-suite green (352 passed) confirms no regression against existing tests from this card's files.
