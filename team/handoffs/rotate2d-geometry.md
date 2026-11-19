# Handoff: rotate2d-geometry (sub-issue #645)

## What was requested

Process card `rotate2d-geometry` under work order #632 (第四十七轮 · 并发 C 单):
own exactly two new files — `rotate2d.py` and `tests/test_rotate2d.py` — implementing
2D point rotation, covering every acceptance item of the work order verbatim, standard
library only, without touching any other deliverable or existing file.

## What I did

- Created `rotate2d.py` with:
  - `rotate_point(x, y, degrees, center=(0, 0)) -> tuple[float, float]` — counterclockwise
    rotation about `center`, using exactly the specified formula:
    `dx = x - cx`, `dy = y - cy`,
    `(cx + dx*cos(theta) - dy*sin(theta), cy + dx*sin(theta) + dy*cos(theta))`,
    with `theta = radians(degrees)`. Returns floats; tolerance 1e-9 satisfied (exact for
    the tested angles up to double-precision rounding, well under 1e-9).
  - `rotate_points(points, degrees, center=(0, 0)) -> list[tuple[float, float]]` —
    validates `points` is a list/tuple and each element a length-2 list/tuple
    (else `TypeError`), rotates each point via `rotate_point`, order preserved.
  - Validation: `x`/`y`/`degrees` must be int/float with bool rejected, else `TypeError`;
    `center` must be a length-2 list/tuple with numeric elements (bool rejected), else
    `TypeError`.
- Created `tests/test_rotate2d.py` with a test for every acceptance item in the work
  order: all 9 `rotate_point` numeric cases, `rotate_points` list and empty cases, and
  all 6 `TypeError` cases, plus supplementary coverage (bool rejection, non-numeric y,
    center element type, non-sequence point element, returned types, list center,
    order preservation, 360° identity).
- Only imports `math` from the standard library; does not import `partitions`,
  `bifid`, or any other module.

## What I did not do

- Did not edit, move, or delete any pre-existing file (including `roman.py`,
  `legacy_stringkit.py`, existing tests, docs, schemas, scripts).
- Did not create `partitions.py`, `bifid.py`, or their tests (other processes own them).
- Did not commit or push (per instructions).

## Checks run and results

- `python3 -m pytest tests/test_rotate2d.py -q` → **25 passed**, exit 0.
- `python3 -m pytest tests/ -q` → **54 passed** (full suite incl. pre-existing tests),
  exit 0.
- Note: pytest was not initially installed; installed it from `requirements-dev.txt`
  (`pytest>=7.4.0`, resolved to 9.2.0) to run the checks. No repo files changed by this.

## What the validator must pay attention to

- All six required `TypeError` cases raise `TypeError` (checked with `pytest.raises`).
- `rotate_point` always returns a tuple of two Python `float`s, even for integer inputs.
- `bool` is rejected everywhere (x, y, degrees, center elements) — `True`/`False` are
  not accepted as 1/0.
- Empty `rotate_points([], 90)` returns `[]` exactly.
- The three deliverables are independent: this module has no cross-imports.
