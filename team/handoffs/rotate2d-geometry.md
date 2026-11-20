# Handoff: rotate2d-geometry (sub-issue #742, work order #729 第五十轮 C · 并发 C 单)

## What was requested

Own and deliver exactly two new files for the 2D point rotation component of work order #729:

- `rotate2d.py` — `rotate_point(x, y, degrees, center=(0, 0)) -> tuple[float, float]` rotating a point counterclockwise (mathematically positive) around `center`, and `rotate_points(points, degrees, center=(0, 0)) -> list[tuple[float, float]]` rotating a sequence of points in order. Exact formula: `theta = radians(degrees)`, `dx = x - cx`, `dy = y - cy`, result `(cx + dx*cos(theta) - dy*sin(theta), cy + dx*sin(theta) + dy*cos(theta))`. Float tolerance 1e-9. Validation: `x`/`y`/`degrees` must be numeric (int/float, `bool` rejected) else `TypeError`; `center` must be a length-2 list/tuple with numeric elements else `TypeError`; `points` must be a list/tuple whose every element is a length-2 list/tuple else `TypeError`.
- `tests/test_rotate2d.py` — one test case per acceptance item, each comparing component-wise within 1e-9 where marked approx.

Constraints: standard library only; no imports from other project modules (`partitions`, `bifid`, `legacy_stringkit`, `roman`, …); only these two new files plus the two team files; touch no pre-existing repository file; do not commit or push.

## What I did

- Created `rotate2d.py` (new): `_is_number`/`_require_number`/`_require_center` validation helpers (rejecting `bool` explicitly), `rotate_point` implementing the spec formula exactly, and `rotate_points` validating the container and each element before delegating to `rotate_point`. Docstrings in the repo's existing Chinese-comment style; `__all__` declared.
- Created `tests/test_rotate2d.py` (new): 23 tests covering every acceptance item:
  - 9 `rotate_point` positive cases (90, 180, -90, 360, 0°, origin/37°, center=(1,1) on (2,1), center fixed point (1,1), (0,1) at 90°), each component-wise within 1e-9 via a `_assert_close` helper that also asserts a 2-tuple return.
  - 2 `rotate_points` positive cases (list of two points approx, empty list exact `== []`).
  - The 6 mandated `TypeError` cases: `rotate_point("1", 0, 90)`, `rotate_point(1, 0, "90")`, `rotate_point(1, 0, 90, center=(1,))`, `rotate_point(1, 0, 90, center=5)`, `rotate_points([(1, 2, 3)], 90)`, `rotate_points("ab", 90)`.
  - 6 additional validation tests: `bool` rejected for x/y/degrees, non-numeric `y`, non-numeric `center` elements (both tuple and list forms), non-sequence element in `points`, non-numeric `degrees` in `rotate_points`, invalid `center` in `rotate_points`.
- Ran both process checks from the repo root (results below).

## What I did NOT do

- Did not create or touch `partitions.py`, `bifid.py`, their tests, or any other pre-existing file (no modifications, deletions, or moves anywhere in the repo).
- Did not add any non-stdlib import or import from other project modules.
- Did not commit or push (left for the workflow).
- Did not add `team/` entries other than my own two required files.

## Checks run and results

Both run from the repository root (`/home/runner/work/droid-mission-test/droid-mission-test`) with Python 3.14.4:

1. `python3 -m pytest tests/test_rotate2d.py -q` → **23 passed** (exit 0).
2. `python3 -m pytest tests/ -q` → **126 passed** (exit 0; the whole pre-existing suite plus my 23).

Environment note: the system interpreter had no pytest, so I installed the repo's own `requirements-dev.txt` (pytest>=7.4.0, jsonschema) into the per-user site packages to run the checks. This changes no repository file.

## What the validator must pay attention to

- Only two repository files were added by this process: `rotate2d.py` and `tests/test_rotate2d.py`. Plus the two team files `team/handoffs/rotate2d-geometry.md` and `team/status/rotate2d-geometry.json`. Nothing else was modified.
- The mandated `TypeError` cases and the positive cases each map 1:1 to named test functions in `tests/test_rotate2d.py`; the helper `_assert_close` enforces the 1e-9 component-wise tolerance and a 2-tuple return type.
- `bool` rejection is implemented and tested (spec: "int/float, bool 拒"), since `bool` is a subclass of `int` in Python.
- Rotation direction is counterclockwise (positive degrees), verified by `rotate_point(1, 0, 90) == (0.0, 1.0)` within tolerance.
- No cross-module coupling: `rotate2d.py` imports only `math`.
