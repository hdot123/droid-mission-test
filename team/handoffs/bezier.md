# Handoff: bezier (sub-issue #961, work order #952 round B)

## What was requested
Implement `bezier.py` (Bézier curve evaluation: `bezier_point` / `bezier_curve`) plus
`tests/test_bezier.py`, per the card SPEC verbatim: only these two new repo files, no
existing file modified, standard library only, no import of `bwt` or `fenwick`.
Every acceptance example (value checks, property check, all ValueError/TypeError cases)
had to land as a test case, float tolerance 1e-9 relative.

## What I did
- Created `bezier.py`:
  - `bezier_point(points, t) -> tuple[float, float]` — de Casteljau linear-interpolation
    loop. `lerp(a, b, u) = a*(1-u) + b*u` is exact at u=0/1, so `t=0.0` returns exactly
    `(float(first))` and `t=1.0` exactly `(float(last))`.
  - `bezier_curve(points, samples) -> list[tuple[float, float]]` — `samples` equally
    spaced params on [0,1] including both ends (`i / (samples - 1)`).
  - Shared validation `_validate_points`: `TypeError` for non-list container, points that
    are not length-2 list/tuple pairs, non-numeric coordinates (bool excluded);
    `ValueError` only after structural checks when `len(points) < 2`.
  - `t` validation: non-numeric (incl. bool) → `TypeError`; outside `[0, 1]` → `ValueError`.
  - `samples` validation: bool or non-int → `TypeError`; `< 2` → `ValueError`.
    Note ordering: `bezier_curve` validates points first, then `samples`.
- Created `tests/test_bezier.py` with 23 tests covering every acceptance item:
  - the four exact/approx `bezier_point` examples, the 5-sample `bezier_curve` example,
    endpoint-exactness (fixed and seeded-random polygons), list/tuple point acceptance;
  - property: seeded de Casteljau-vs-Bernstein agreement (degree 1–6, `random.Random(20261127)`,
    independent `math.comb` Bernstein reference, rel/abs tol 1e-9);
  - all four `ValueError` cases and all four `TypeError` cases from the card, plus
    extra edge cases (bool `samples`/`t`, tuple/dict `points`, malformed point shapes).

## What I did NOT do
- Did not touch `bwt.py`, `fenwick.py`, or any existing file (only the two new module/test
  files plus this handoff and `team/status/bezier.json`).
- Did not commit or push.
- Did not run anything beyond the two prescribed checks.

## Checks run and results
1. `python3 -m pytest tests/test_bezier.py -q` → **23 passed** (exit 0).
2. `python3 -m pytest tests/ -q` → **365 passed, 2 skipped** (exit 0, 21.7s).

No `verdict.json` / `verdict.md` byproducts appeared; `git status` shows only my two new
files (plus the pre-existing untracked `worker-prompt.txt` / `worker-stream.jsonl`).

## Notes for the validator
- Endpoint exactness holds by construction (de Casteljau at u=0/u=1), so the
  `== (0.0, 0.0)` / `== (3.0, 4.0)` strict-equality examples pass literally, not via approx.
- Validation order in `bezier_curve`: points are validated before `samples`, so
  `bezier_curve("ab", 2.5)` raises `TypeError` for points. Each card-specified input is
  unambiguous under this order.
- The only free parameter choice: coordinates are coerced to `float` on the way in, so an
  all-int example like `bezier_point([(0, 0), (3, 4)], 0.0)` returns `(0.0, 0.0)` as the
  spec's expected literals require.
