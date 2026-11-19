# Handoff: rotate2d (sub-issue #677)

## What was requested

Implement the `rotate2d` component of work order #663 第四十八轮 C 单:

- `rotate_point(x, y, degrees, center=(0, 0)) -> tuple[float, float]`: rotate point
  (x, y) counterclockwise (math-positive direction) by `degrees` around `center`,
  using `theta = radians(degrees)`, `dx = x - cx`, `dy = y - cy`, result =
  `(cx + dx*cos(theta) - dy*sin(theta), cy + dx*sin(theta) + dy*cos(theta))`.
  Float tolerance 1e-9. `x`/`y`/`degrees` must be numeric (int/float, `bool`
  rejected) else `TypeError`; `center` must be a length-2 list/tuple with numeric
  elements else `TypeError`.
- `rotate_points(points, degrees, center=(0, 0)) -> list[tuple[float, float]]`:
  `points` must be a list/tuple and every element a length-2 list/tuple, else
  `TypeError`; rotate each via `rotate_point`, preserve order.
- Every listed acceptance point must have a corresponding test case in
  `tests/test_rotate2d.py`.
- Only add `rotate2d.py` and `tests/test_rotate2d.py`; no existing files may be
  modified; standard library only; no cross-imports of sibling modules.

## What I did

- Created `rotate2d.py` with `rotate_point` and `rotate_points`, plus a private
  `_is_number` helper that rejects `bool` explicitly (since `bool` subclasses
  `int` in Python).
- Created `tests/test_rotate2d.py` covering every acceptance point:
  - Numeric results: 90, 180, -90, 360, 0-degree identity, origin fixed,
    center-based rotation, center-fixed case, `(0,1)` by 90, multi-point list,
    empty list — all asserted within 1e-9.
  - Type errors: `rotate_point("1", 0, 90)`, `rotate_point(1, 0, "90")`,
    `rotate_point(1, 0, 90, center=(1,))`, `rotate_point(1, 0, 90, center=5)`,
    `rotate_points([(1, 2, 3)], 90)`, `rotate_points("ab", 90)`.
  - Extra validation tests: `bool` rejected for coordinates/degrees, non-numeric
    `y`, non-numeric center element, return type is `tuple[float, float]`,
    order preservation, list-of-lists points with list center.
- Installed `pytest>=7.4.0` (from `requirements-dev.txt`) into the environment;
  it was not preinstalled. No repository files were changed for this.

## What I did not do

- Did not touch `partitions.py`, `bifid.py`, or any test belonging to them
  (owned by other processes).
- Did not modify any pre-existing repository file (only added the two files
  listed above plus the two team files).
- Did not commit or push.

## Checks run and results

From the repository root:

1. `python3 -m pytest tests/test_rotate2d.py -q`
   → **23 passed** in 0.02s
2. `python3 -m pytest tests/ -q`
   → **59 passed** in 1.81s (includes existing tests; no regressions)

## Notes for the validator

- `rotate_point` returns Python `float` components even when inputs are `int`
  (e.g. `rotate_point(1, 0, 0)` returns `(1.0, 0.0)`), matching the declared
  `tuple[float, float]` return type.
- `bool` is rejected for `x`, `y`, `degrees`, and center elements because
  `isinstance(True, int)` is `True` in Python; a dedicated `_is_number` check
  excludes it.
- Angles are treated in degrees and converted via `math.radians`; negative and
  large angles (e.g. 360) work without special-casing.
- Only `rotate2d.py` and `tests/test_rotate2d.py` were added as deliverables;
  `team/handoffs/rotate2d.md` and `team/status/rotate2d.json` are the required
  team files.
