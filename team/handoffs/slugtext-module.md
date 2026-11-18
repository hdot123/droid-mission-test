# Handoff: slugtext-module (sub-issue #262)

## What was requested
Process card "slugtext-module" under work order #246 (round 33, foreman v2.6.5):
create `slugtext.py` in the repo root and `tests/test_slugtext.py`, with exactly:

- `slugify(text)`: lowercase, replace each maximal run of non-`[a-z0-9]` characters
  with a single `-`, then strip leading/trailing `-`. Non-ASCII letters (e.g. `é`)
  count as non-`[a-z0-9]`; result may be `""`.
- `is_slug(s)`: valid iff non-empty, only `[a-z0-9]` and `-`, no leading/trailing
  `-`, no consecutive `--`.

All nine spec examples must hold. Only the Python standard library; no imports of
`lcs`/`packbits`; no package directory; no CLI. Scope owns only `slugtext.py` and
`tests/test_slugtext.py`.

## What I did
- Created `slugtext.py`: `slugify` uses `re.sub(r"[^a-z0-9]+", "-", text.lower())`
  then `.strip("-")`; `is_slug` uses `re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", s)`
  with an explicit empty-string rejection.
- Created `tests/test_slugtext.py` covering every spec example plus edge cases:
  empty input, punctuation-only input, consecutive separators, non-ASCII letters,
  leading/trailing dashes, digits/mixed case, and invalid slug shapes.
- Ran the process check verbatim: `python -m pytest -q tests/test_slugtext.py`
  → `8 passed in 0.02s` (exit 0).

## What I did not do
- Did not create or modify `lcs.py`, `packbits.py`, or any test other than
  `tests/test_slugtext.py`.
- Did not touch `team/` files of other processes, `.github/`, or any other path.
- Did not commit or push.
- Did not build a package directory or CLI.

## Checks run and results
| Command (verbatim) | Result |
| --- | --- |
| `python -m pytest -q tests/test_slugtext.py` | passed: 8 passed, exit 0 |

Environment note: pytest was not preinstalled; `python3 -m pip install pytest`
(pytest 9.2.0) was run first so the check command could execute.

## For the validator
- The check command above is verbatim from this card's checks column.
- All nine spec examples are asserted in `tests/test_slugtext.py`.
- Global acceptance (whole-suite `python -m pytest -q` after all three
  deliverables merge) is not this card's check; it applies post-merge.
