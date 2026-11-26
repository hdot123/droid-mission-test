# Handoff: speedconv (sub-issue #862)

## What was requested

Work order #850, process card `speedconv` (sub-issue #862): create exactly two new files —
`speedconv.py` and `tests/test_speedconv.py` — implementing
`convert_speed(value, from_unit, to_unit) -> float` for the unit set
`{m/s, km/h, mph, kn, ft/s}` converted through a base of `m/s`, with pinned
full-precision coefficients (m/s = 1, km/h = 1/3.6, mph = 1609.344/3600,
kn = 1852/3600, ft/s = 0.3048), `ValueError` on unknown units (including case
mismatches like "MS", "knots", "fps"), and relative error 1e-9 for all approx
checks. Every acceptance example in the card needed a corresponding test case.
Standard library only; no imports of sibling modules; no modification of any
existing file.

## What I did

- Created `speedconv.py`:
  - Module-level `_FACTORS` dict mapping each unit to its exact "m/s per unit"
    coefficient as pinned above (expressions `1 / 3.6`, `1609.344 / 3600`,
    `1852 / 3600` written literally so full precision is preserved).
  - `convert_speed(value, from_unit, to_unit) -> float` raises
    `ValueError("unknown speed unit: ...")` when either unit is not an exact
    key of `_FACTORS`, else returns `value * _FACTORS[from_unit] / _FACTORS[to_unit]`.
- Created `tests/test_speedconv.py` with 15 test functions covering every
  acceptance point verbatim: exact zero, all 10 scalar approximations, the
  full 5x5 round-trip (all 25 ordered unit pairs) at rel tol 1e-9, and the
  three ValueError cases (`"fps"`, `"knots"`, `"MS"`).
- Followed the repo's existing test import convention (`from roman import ...`
  in `tests/test_roman.py`): plain `from speedconv import convert_speed`, no
  sys.path manipulation.

## What I did not do

- Did not touch any existing file (only the two card files plus the two
  team files `team/handoffs/speedconv.md` and `team/status/speedconv.json`).
- Did not implement titlecase or divisorsum (other cards own those).
- Did not import from sibling modules; standard library only
  (`math.isclose`, `pytest` in tests).
- Did not commit or push.
- Did not fix the pre-existing full-suite failure described below (out of scope).

## Checks I ran and results

1. `python3 -m pytest tests/test_speedconv.py -q` → **15 passed**.
2. `python3 -m pytest tests/ -q` → **355 passed, 2 skipped, 1 failed**.
   The single failure is `tests/test_check_summary_focused_counts.py::
   test_summary_block_on_r54_pack_produces_real_focused_counts`, which reads
   evidence from `/tmp/r54-audit/a/evidence/packs/damm/checks-output.txt`
   (outside the repo; absent in this environment).
3. Verified pre-existing: `git stash -u` (hiding my two files) and re-running
   that test fails identically (`1 failed, 4 passed`), so it fails on the
   clean baseline too and is not caused by my change.

## What the validator must pay attention to

- The only full-suite failure is the environmental, pre-existing
  `/tmp/r54-audit` fixture test — not related to `speedconv`. Expected state
  for this card: all 15 speedconv tests green; everything else unchanged
  relative to baseline.
- No `verdict.json` / `verdict.md` by-products were produced by the runs, so
  nothing to delete; `git status` shows only the two card files (plus the
  pre-existing untracked `worker-prompt.txt` / `worker-stream.jsonl`).
- Unit matching is intentionally exact and case-sensitive: `"m/s"` ok,
  `"MS"` / `"knots"` / `"fps"` raise `ValueError`, per the pinned spec.
