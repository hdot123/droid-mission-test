# Handoff: polygonarea (sub-issue #448, work order #433 round 44 D)

## What was requested

Process card `polygonarea`: create `polygonarea.py` and `tests/test_polygonarea.py` (both new files, nothing else touched) implementing:

- `polygon_area(points) -> float` — signed shoelace area (CCW positive, CW negative); fewer than 3 points → `ValueError`; non-numeric point → `TypeError`.
- `polygon_perimeter(points) -> float` — closed perimeter (last point connects back to first); fewer than 2 points → `ValueError`; same non-numeric rule.

Every acceptance point from the work order had to have a corresponding test case. Standard library only; no imports from this round's other deliverables (`binheap.py`, `ordinal.py`).

## What I did

- Created `polygonarea.py`:
  - Shared `_validate` helper: rejects non-list/tuple input with `TypeError`, too-few points with `ValueError`, malformed or non-`int`/`float` point coordinates (including `bool`) with `TypeError`, and non-finite floats with `TypeError`.
  - `polygon_area`: shoelace sum over edges with wraparound, divided by 2.0 (returns `float`, signed).
  - `polygon_perimeter`: sum of `math.hypot` edge lengths with wraparound.
- Created `tests/test_polygonarea.py` with 12 tests covering all 11 acceptance points plus one extra (`polygon_perimeter([(0, 0), ("a", 1)])` raises `TypeError`, exercising the perimeter non-numeric rule explicitly).

## What I did not do

- Did not touch any pre-existing file (`legacy_stringkit.py`, `roman.py`, existing tests, etc.).
- Did not create or modify `binheap.py`, `ordinal.py`, or their tests (other process cards own those).
- Did not commit or push.
- Note: `pytest` was not installed in the environment; I installed it via `python3 -m pip install --break-system-packages pytest` (pytest 9.2.0) to run the checks. No project files were changed by that.

## Checks run

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_polygonarea.py -q` | 12 passed |
| `python3 -m pytest tests/ -q` | 23 passed |

## Validator attention points

- Area sign convention is verified by the two unit-square tests: `[(0,0),(1,0),(1,1),(0,1)] == 1.0` (CCW) and `[(0,0),(0,1),(1,1),(1,0)] == -1.0` (CW).
- Area returns a float even for integer inputs (e.g. `6.0`, `0.0`); comparisons in tests are exact against the spec's literals — shoelace arithmetic on these inputs is exact in IEEE-754, so `==` is safe.
- Full-suite pass count (23) includes tests owned by other process cards; if a sibling's tests fail after merge, that is not this card's regression.
- Validation accepts `points` as list or tuple; point pairs as list or tuple of exactly two numbers; `bool` coordinates are rejected as non-numeric per the "numeric (bool excluded)" convention used across this round.
