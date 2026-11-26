# Handoff: pointinpoly (sub-issue #872, retry r2)

## What was requested

Process card "点在多边形内三态判定组件与测试": create `pointinpoly.py` and
`tests/test_pointinpoly.py` only. Implement `point_in_polygon(x, y, polygon)
-> str` via ray casting with three states ("inside" / "outside" /
"boundary"), CW and CCW vertex orders accepted, boundary covering edge
interior and vertices with exact integer-coordinate judgement, and
`ValueError` for polygons with fewer than 3 vertices. Every acceptance
point from work order #851 section 二 must have a corresponding test case.
Standard library only; no cross-imports with punycode/a1z26.

## What I did

- Created `pointinpoly.py`:
  - Exact boundary test first: cross product == 0 plus bounding-box
    containment per edge segment (endpoints included), so vertices and edge
    points are classified "boundary" without float tolerance.
  - Ray casting with the half-open rule `(ay > y) != (by > y)` and
    intersection comparison `x < x_int`, orientation-agnostic (CW/CCW).
  - `ValueError` when `polygon` is not a list or has fewer than 3 vertices.
- Created `tests/test_pointinpoly.py` with 24 tests covering every
  acceptance point verbatim: square SQ (inside/outside/4 boundary cases),
  SQ reversed CW (inside + outside), triangle TRI (2 inside, hypotenuse
  boundary, outside, leg boundary), concave L (3 inside, notch outside,
  3 boundary including the concave vertex, far outside), and both
  ValueError cases.

## What I did not do

- Did not touch any existing file (only the two deliverables + this handoff
  + `team/status/pointinpoly.json` were created).
- Did not implement or test punycode or a1z26 (other cards' scope).
- Did not write any diff file or other pack-shape file; no commit/push.

## Checks run

1. `python3 -m pytest tests/test_pointinpoly.py -q` → 24 passed, exit 0.
2. `python3 -m pytest tests/ -q --deselect
   tests/test_check_summary_focused_counts.py::test_summary_block_on_r54_pack_produces_real_focused_counts`
   → 364 passed, 2 skipped, 1 deselected, exit 0.

## Notes for the validator

- The deselected test is the retry-specified machine gate failure (depends
  on a `/tmp/r54-audit` fixture absent in this environment); it is excluded
  per the card's checks, not because of this component.
- Boundary detection is exact (integer arithmetic in the cross product),
  so the "整数坐标须精确判定" requirement holds by construction; floats go
  through the same cross-product test without epsilon fudging.
- `verdict.json` / `verdict.md` appearing at repo root are test-suite
  by-products and were removed after the checks ran.
