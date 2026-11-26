# Handoff: segdist (sub-issue #882, work order #877 B 单)

## What was requested

Implement two files only, per the process card:

- `segdist.py` — continuous point-to-segment geometry:
  - `point_segment_distance(px, py, ax, ay, bx, by) -> float`: shortest distance, projection parameter clamped to [0, 1].
  - `closest_point_on_segment(px, py, ax, ay, bx, by) -> tuple[float, float]`: closest point on the segment.
  - Degenerate segment (a == b) handled as point-to-point distance.
  - Relative tolerance 1e-9; returns continuous values, NOT boolean intersection/containment predicates.
- `tests/test_segdist.py` — one test case per acceptance item (13 items listed in the card), plus consistency/robustness cases.

Constraints: standard library only, no cross-module imports, no modification of any existing file.

## What I did

- Created `segdist.py`: `closest_point_on_segment` computes `t = ((p-a)·(b-a))/|b-a|²`, clamps t to [0, 1], returns `(ax + t*dx, ay + t*dy)`; returns `(float(ax), float(ay))` for the degenerate case (`denom == 0`). `point_segment_distance` reuses the closest point and returns the Euclidean distance to it, which by construction equals the clamped-projection distance and handles the degenerate case correctly.
- Created `tests/test_segdist.py`: 17 tests — one per each of the 13 acceptance items (10 distance values with `pytest.approx(rel=1e-9)`, 3 exact closest-point tuples), plus 4 extra tests (clamp-to-a, closest point on a diagonal, distance/closest-point consistency across cases, closest point always within projection range [0,1]).

## What I did NOT do

- Did not touch `stirling2.py`, `htmlescape.py`, or any other existing file (stirlling2 and htmlescape are other cards' scope).
- Did not add input type validation (no TypeError/ValueError contract was specified for this module's functions — the card specifies none for segdist, unlike stirling2/htmlescape).
- Did not commit or push.

## Checks run

- `python3 -m pytest tests/test_segdist.py -q` → `17 passed in 0.03s`
- `python3 -m pytest tests/ -q` → `359 passed, 2 skipped in 19.65s`

No `verdict.json` / `verdict.md` by-products were produced by these runs; nothing needed cleanup.

## Notes for the validator

- All 13 acceptance items map 1:1 to named tests in `tests/test_segdist.py` (e.g. `test_degenerate_segment_sqrt2`, `test_closest_point_clamped_to_b`, `test_closest_point_degenerate`).
- Exact-coordinate items are asserted with `==` on tuples: `(0.0, 0.0)`, `(2.0, 0.0)`, `(0.0, 0.0)` for degenerate — these are float-exact under the implementation given (t clamp to 0.0/1.0, multiplication by segment vector of exact small integers).
- The sqrt values (`1.4142135623730951`, `2.8284271247461903`, `4.242640687119286`) are checked with relative tolerance 1e-9 as the card requires, not with `==`.
- This module intentionally returns floats (not bools): no intersection/containment API exists here.
