# Handoff: damm (sub-issue #817)

## What was requested

Process card for work order #812 (第54轮并发A单): implement the Damm algorithm check-digit component as two brand-new files only:

- `damm.py` — pinned quasi-group table, `damm_check_digit(number) -> str`, `damm_validate(number) -> bool`, with `TypeError` for non-`str` input and `ValueError` for empty string or non-ASCII-digit characters.
- `tests/test_damm.py` — one test case per acceptance point in the spec (16 required points, 18 test functions).

Constraints: only add these two files, modify no existing files, standard library only, no import of `easterorthodox` or `graph`.

## What I did

- Added `damm.py` at repo root:
  - `_TABLE` pinned exactly to the 10x10 quasi-group table in the spec (rows = interim, columns = next digit).
  - `_interim(number)` shared helper: raises `TypeError` for non-`str` (checked before emptiness), `ValueError` for empty string, `ValueError` for any character outside ASCII `0-9` (membership test against `"0123456789"` rejects full-width digits, superscripts, spaces, tabs, hyphens, etc.), then folds `interim = table[interim][digit]` from initial `interim = 0`.
  - `damm_check_digit` returns `str(final_interim)` (diagonal is all 0, so no extra transform — per spec).
  - `damm_validate` returns `final_interim == 0`.
- Added `tests/test_damm.py` with 18 tests covering every acceptance point: public examples `572→"4"`, `5724→True`, transposition `5742→False`; `123→"4"`, `0→"0"`, `42→"7"`, `987654321→"5"`, `2024→"0"`; `1234→True`, `1235→False`, `427→True`; `damm_check_digit(572)` → `TypeError`; `""`, `"57a"`, `"57 24"` → `ValueError`. Plus a few extra edge guards (validate on non-str/empty/non-ASCII-digit chars: full-width `５７２４`, superscript `²`, tab, hyphen).

## What I did NOT do

- Did not touch any pre-existing file (git status shows only `damm.py` and `tests/test_damm.py` as my additions; `worker-prompt.txt` / `worker-stream.jsonl` were already untracked before I started).
- Did not implement `easterorthodox.py` or `graph.py` (other cards), did not add `conftest.py`, `pytest.ini`, or any config.
- Did not import anything beyond the Python standard library; `damm.py` imports nothing.
- Did not commit or push.
- Note: the environment had no `pytest`, so I installed the repo's own `requirements-dev.txt` (`pytest>=7.4.0`, `jsonschema>=4.20.0`) via `python3 -m pip install --user` — an environment setup step, not a repo change.

## Checks I ran and results

1. `python3 -m pytest tests/test_damm.py -q` → **18 passed** (exit 0).
2. `python3 -m pytest tests/ -q` → **205 passed, 2 skipped** in ~16.6s (exit 0). The 2 skips are pre-existing suite skips, unrelated to this card.

No `verdict.json` / `verdict.md` were produced by these runs (nothing to delete).

## What the validator must pay attention to

- Spec says "非 ASCII 数字字符抛 ValueError": I interpret this as "only ASCII digits `0-9` are valid", so any other character (including non-digit ASCII like space/`a`/`-` and non-ASCII digits like `５`) raises `ValueError`. If the validator meant the looser reading (only non-digit characters raise), the extra rejections are supersets and all 16 mandated points still behave exactly as written.
- `TypeError` is checked before emptiness (`damm_check_digit(None)` raises `TypeError`, not `ValueError`); the spec only mandates `TypeError` for non-`str`, which this satisfies.
- Import style matches the existing repo (`from roman import ...` in `tests/test_roman.py`): root-level module imported plainly; `python3 -m pytest` from the repo root puts the root on `sys.path`, so no `conftest.py` was needed.
- All 16 mandated acceptance points have a dedicated test function; test names map 1:1 to the spec bullets for easy audit.
