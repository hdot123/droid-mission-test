# Handoff: pointinpoly (sub-issue #866)

## What was requested

Process card #866 under work order #851 (round 55, concurrent card D): implement
point-in-polygon three-state classification in a new `pointinpoly.py`, plus
`tests/test_pointinpoly.py`. Scope is strictly those two files; no existing file
may be modified; standard library only; no cross-imports with punycode/a1z26.

Spec (verbatim from the acceptance criteria):

- `point_in_polygon(x, y, polygon: list[tuple[float, float]]) -> str`: ray-casting
  method, returns `"inside"`, `"outside"`, or `"boundary"`.
- CW and CCW vertex order both accepted.
- Boundary covers points on an edge segment and points coinciding with any
  vertex.
- Integer coordinates must be judged exactly.
- Fewer than 3 vertices raises `ValueError`.
- Every acceptance example must have a corresponding test case.

## What I did

Created `pointinpoly.py` (new, ~2 KB):

- Boundary detection first: integer cross-product collinearity test
  (`_on_segment`), exact for integer coordinates and safe for floats; covers both
  on-edge and on-vertex points.
- Ray-casting parity test: an edge straddles the horizontal line through the
  query point when `(y1 > y) != (y2 > y)`; the half-plane comparison
  `x1 + (y - y1) * (x2 - x1) / (y2 - y1) > x` is evaluated as an integer
  inequality (`(x1 - x) * den + num` vs `0`, sign applied by `den`) so no
  division ever happens and integer inputs are judged exactly.
- `len(polygon) < 3` raises `ValueError` before any geometry runs.

Created `tests/test_pointinpoly.py` (new, 8 tests) covering every acceptance
point: square inside/outside, square boundary edges and vertices, CW-reversed
square, triangle (hypotenuse boundary, inside, outside, edge), concave L-polygon
(inside x3, outside x2 including the notch, boundary x3 including the concave
vertex and a collinear mid-edge point), and both `ValueError` cases
(2-vertex and empty polygon).

## What I did not do

- Did not touch `punycode.py`, `a1z26.py`, or any other process's files.
- Did not modify any pre-existing file.
- Did not add cross-imports; the module is standalone.
- Did not commit or push (workflow owns that).

## Checks I ran and their results

1. `python3 -m pytest tests/test_pointinpoly.py -q` — **8 passed in 0.01s**
   (PASS; every acceptance example in the card maps to a passing assertion).
2. `python3 -m pytest tests/ -q` — **348 passed, 2 skipped, 1 failed** in 18.15s.
   The single failure is `tests/test_check_summary_focused_counts.py::
   test_summary_block_on_r54_pack_produces_real_focused_counts`, which fails
   with `FileNotFoundError: /tmp/r54-audit/a/evidence/packs/damm/checks-output.txt`.
   This failure is **pre-existing and unrelated to this card**: I verified it by
   stashing my two new files (`git stash -u`) and re-running the test — it fails
   identically on a clean tree. It reads external `/tmp` audit artifacts that do
   not exist in this environment.

## What the validator must pay attention to

- The full-suite run shows 1 failure in `test_check_summary_focused_counts.py`.
  It is an environment artifact dependency (`/tmp/r54-audit/...`), not caused by
  `pointinpoly.py` / `tests/test_pointinpoly.py`. The card's own check
  (`tests/test_pointinpoly.py -q`) is fully green: 8/8 passed.
- No `verdict.json` / `verdict.md` by-products were present after my runs; the
  repo working tree contains only my two deliverables plus the pre-existing
  untracked `worker-prompt.txt` / `worker-stream.jsonl` (owned elsewhere).
