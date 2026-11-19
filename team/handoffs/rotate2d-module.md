# Handoff: rotate2d-module (sub-issue #710)

## What was requested

Implement the 2D point rotation component of work order #700 (round 49C, concurrent unit C):

- New file `rotate2d.py` at the repo root, standard library only, no imports of other delivery modules (`partitions`, `bifid`).
  - `rotate_point(x, y, degrees, center=(0, 0)) -> tuple[float, float]`: counter-clockwise rotation by `degrees` around `center`, using `rx = cx + dx·cosθ − dy·sinθ`, `ry = cy + dx·sinθ + dy·cosθ` with `θ = radians(degrees)`.
  - `rotate_points(points, degrees, center=(0, 0)) -> list[tuple[float, float]]`: order-preserving element-wise rotation; `points` must be a list/tuple of length-2 list/tuple elements, else TypeError.
  - Validation: `x`/`y`/`degrees` must be real numbers (bool rejected) else TypeError; `center` must be a length-2 list/tuple with numeric elements else TypeError.
- New file `tests/test_rotate2d.py` with a test case for every acceptance point (17 tests).
- Only these two files may be added; no existing files modified; no commits/pushes.

## What I did

- Created `rotate2d.py` with `rotate_point` / `rotate_points`, strict validation (bool explicitly rejected via `isinstance(value, (int, float)) and not isinstance(value, bool)`), and a small `_snap` helper that normalizes results within 1e-9 of zero to `0.0` so cases like `rotate_point(0, 0, 37)` and `rotate_point(1, 0, -90)` return exact `(0.0, ...)` rather than `-1.2e-16`. Tolerance for assertions is 1e-9 as specified.
- Created `tests/test_rotate2d.py` covering each acceptance point verbatim: 90°/180°/−90°/360°/0°/37° rotations, rotation about a center, center fixed, y-axis by 90°, `rotate_points` of a pair of points, empty list, and the six TypeError cases (`"1"` x, `"90"` degrees, `center=(1,)`, `center=5`, `[(1, 2, 3)]`, `"ab"`).

## What I did not do

- Did not touch `partitions.py`, `bifid.py`, or their tests (owned by other processes).
- Did not modify any pre-existing file (including `requirements-dev.txt`, `worker-prompt.txt`, `worker-stream.jsonl`).
- Did not commit or push.
- Did not import anything outside the Python standard library (`math` only).

## Checks run

1. `python3 -m pytest tests/test_rotate2d.py -q` → `17 passed in 0.02s`
2. `python3 -m pytest tests/ -q` → `97 passed in 3.39s` (full existing suite plus the new tests)

Note: pytest was not preinstalled in the environment; I installed it with `python3 -m pip install pytest` (version 9.2.0), matching `requirements-dev.txt` (`pytest>=7.4.0`).

## Notes for the validator

- All 17 tests are green and the full suite is green; no existing test regressed.
- The only files added by this process are `rotate2d.py`, `tests/test_rotate2d.py`, `team/handoffs/rotate2d-module.md`, `team/status/rotate2d-module.json`.
- Floating-point snapping to `0.0` within 1e-9 is intentional and keeps assertions like `rotate_point(0, 0, 37) == (0.0, 0.0)` stable; it does not mask errors beyond the specified 1e-9 tolerance.
