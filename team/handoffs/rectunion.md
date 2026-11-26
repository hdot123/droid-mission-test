# Handoff — rectunion (sub-issue #945, work order #926)

## What was requested

Implement `rectunion.py` exposing `union_area(rects) -> int | float` returning the
union area of a list of axis-aligned rectangles `(x1, y1, x2, y2)` (list or tuple
form accepted, int/float coordinates), plus `tests/test_rectunion.py`. New files
only; no existing file may be touched; standard library only; no imports of the
other two components (`eulerian`, `joaat`).

## What I did

Created exactly two new files:

- `rectunion.py` — validation (list container / length-4 sequence / int-float
  non-bool coords / `x1 < x2 and y1 < y2`, else TypeError or ValueError; empty
  list returns 0) followed by a coordinate-compression grid sweep: all distinct
  x and y boundaries are sorted, every grid cell is checked against every
  rectangle and covered cells are summed once. Overlap is naturally counted
  once; edge-touching rectangles contribute separately; containment adds nothing.
  Return type: `int` when all coordinates are `int`, `float` when any is `float`
  (arithmetic is direct, no coercion).
- `tests/test_rectunion.py` — one test per acceptance item, transcribed verbatim
  from the acceptance section: empty/single/disjoint/partial-overlap/containment/
  edge-contact/mixed (3+2+9=14)/float single (2.25)/float overlap (7.0), the
  grid-rasterization property (300 random groups with coords 0..7, side 1..4,
  1–5 rects, seeded RNG; plus a variant where all coordinates fall inside 0..7),
  the three ValueError cases, the five TypeError cases, return-type checks, and
  extra TypeError coverage for tuple/dict containers.

## What I did not do

- Did not modify, move, or delete any pre-existing file (`git status` shows only
  the two new files plus the pre-existing untracked `worker-prompt.txt` /
  `worker-stream.jsonl`).
- Did not touch `eulerian.py`, `joaat.py`, or their tests.
- Did not implement or import the other two components; only the standard
  library (`random` and `pytest` in the test file) is used.
- Did not commit or push.

## Checks run and results

1. `python3 -m pytest tests/test_rectunion.py -q` → **14 passed in 0.02s**
2. `python3 -m pytest tests/ -q` → **356 passed, 2 skipped in 19.32s** (the 2
   skips are pre-existing, unrelated to this component)

No `verdict.json` / `verdict.md` by-products were produced by these runs (checked
with `ls`).

## Notes for the validator

- Acceptance values are transcribed exactly; the mixed case comment in the test
  mirrors the spec's `3＋2＋9＝14`.
- The property test is deterministic (fixed seed `20261126`), so failures, if any,
  are reproducible.
- `union_area` rejects non-list containers (`tuple`, `dict`, `str`) and
  non-sequence elements with TypeError, and rejects `bool` coordinates with
  TypeError, per the card's wording "容器不是列表形态" and "坐标非数值（含 bool）".
- Edge contact and containment semantics are explicitly covered by dedicated
  tests as required.
