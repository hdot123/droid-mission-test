# Handoff: circle (sub-issue #918, work order #903 第57轮 C 单)

## What was requested

Implement the circle geometry module per the #903 work order, card "circle":

- New file `circle.py` at repo root with `circle_area(r)`, `circle_circumference(r)`,
  `sector_area(r, angle_deg)`, `segment_area(r, angle_deg)`. Angles are in degrees.
  Segment = sector − isosceles triangle: `(θ − sinθ)·r²/2`, θ in radians.
- New file `tests/test_circle.py` covering every acceptance point verbatim.
- Validation: `r < 0` → ValueError (`r = 0` legal, area 0); angle outside
  `[0, 360]` → ValueError; non-numeric (including bool) → TypeError.
- Float assertions use relative tolerance 1e-9.
- Only these two product files plus this handoff and `team/status/circle.json`.
  Standard library only; no import of `josephus` or `decibel`.

## What I did

- Created `circle.py`:
  - Helpers `_check_number` (TypeError for bool/non-number), `_check_radius`
    (ValueError for r < 0), `_check_angle` (ValueError outside [0, 360]).
  - `circle_area` = πr²; `circle_circumference` = 2πr;
    `sector_area` = πr²·a/360; `segment_area` = (θ − sinθ)·r²/2 with
    `θ = math.radians(a)`.
  - Validation runs before arithmetic, so e.g. `sector_area(1, True)` raises
    TypeError (bool rejected by `_check_number`), `circle_area("1")` TypeError,
    `circle_area(-1)` / `sector_area(1, 361)` / `segment_area(1, -10)` ValueError.
- Created `tests/test_circle.py` with 17 tests, each acceptance point mapped:
  - `circle_area(1)` ≈ π; `circle_area(0)` ≈ 0.0; `circle_circumference(1)` ≈ 2π;
    `sector_area(2, 90)` ≈ π; `sector_area(1, 360)` ≈ π; `sector_area(3, 0)` ≈ 0.0;
    `segment_area(1, 90)` ≈ 0.2853981633974483; `segment_area(1, 180)` ≈ π/2;
    `segment_area(1, 360)` ≈ π; `segment_area(2, 0)` ≈ 0.0.
  - Property tests: `sector_area(r, a) / circle_area(r) ≈ a/360` for several
    r > 0 and angles incl. 0/90/180/360; `segment_area(r, a) ≈ sector_area(r, a)
    − 0.5·r²·sin(a°)` (sin via `math.sin(math.radians(a))`).
  - ValueError cases: `circle_area(-1)`, `sector_area(1, 361)`,
    `segment_area(1, -10)`.
  - TypeError cases: `circle_area("1")`, `sector_area(1, True)`.
  - All float assertions use `pytest.approx(..., rel=1e-9)`.

## What I did not do

- Did not touch any existing file (only added the two product files above).
- Did not create `josephus.py` / `decibel.py` or their tests (other cards own them).
- Did not import josephus or decibel; standard library only (`math`).
- Did not commit or push.

## Checks run and results

1. `python3 -m pytest tests/test_circle.py -q` → **17 passed** in 0.03s.
2. `python3 -m pytest tests/ -q` → **359 passed, 2 skipped** in 21.69s (exit 0).

The 2 skips are pre-existing suite skips, unrelated to this card.

## Notes for the validator

- Degree-vs-radian convention is pinned: angles are degrees everywhere;
  only the internal sin/θ step converts to radians.
- Segment is the exact decomposition (180° → half circle, 360° → full circle),
  verified by dedicated tests, not an approximation.
- bool is rejected as TypeError even though bool subclasses int — handled by an
  explicit `isinstance(value, bool)` check in `_check_number`.
- The full-suite run may drop pipeline by-products (`verdict.json`,
  `verdict.md`) in the repo root; I deleted them after running the checks —
  they are not deliverables of this card.
