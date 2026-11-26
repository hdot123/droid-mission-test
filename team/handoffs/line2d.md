# Handoff: line2d (sub-issue #911, work order #902 第57轮 B 单)

## What was requested

Implement `line2d.py` (2D infinite-line geometry) plus `tests/test_line2d.py` for
work order #902 (process card `line2d`, sub-issue #911), covering every acceptance
item verbatim:

- `line_from_points(p, q) -> tuple[float, float, float]`: unit-normal form
  (A, B, C) of `Ax + By + C = 0`, with `A² + B² = 1` and sign pinned
  (A > 0, or A = 0 and B > 0). Coincident points raise `ValueError`.
- `point_line_distance(p, line) -> float`: distance from a point to a line given
  as any `(A, B, C)` triple (not required to be normalized).
- `lines_intersection(l1, l2) -> tuple[float, float] | None`: intersection point;
  parallel or coincident lines return `None`.
- Input rules: points are `(x, y)` pairs; bool / non-numeric coordinates and
  malformed shapes (not a pair, length ≠ 2) raise `TypeError`.
- Floating-point acceptance: relative error 1e-9.

## What I did

Created exactly two new files (no existing file touched):

- `line2d.py` — standard library only (`math`), no imports of motzkin/extractnums.
  - `_coerce_number` / `_coerce_point` / `_coerce_line` enforce the type and
    shape rules (`bool` rejected via `isinstance(v, bool)` first, so
    `line_from_points((1, True), (2, 3))` raises `TypeError`).
  - `line_from_points` builds the perpendicular `(dy, -dx)`, normalizes with
    `math.hypot`, then flips the sign if `A < 0` or (`A == 0` and `B < 0`);
    `-0.0` is cleaned to `0.0` for output. Coincident points → `ValueError`.
  - `point_line_distance` = `|Ax + By + C| / hypot(A, B)` (works unnormalized);
    a degenerate line (A = B = 0) raises `ValueError` (not part of spec but
    avoids ZeroDivisionError).
  - `lines_intersection` uses the Cramer determinant `det = A1·B2 − A2·B1`;
    parallel/coincident detected with a scale-relative test
    `|det| ≤ 1e-12 · ‖(A1,B1)‖ · ‖(A2,B2)‖` → returns `None`. Deterministic:
    the two diagonal lines return exactly `(0.5, 0.5)`.
- `tests/test_line2d.py` — 19 test functions covering every acceptance item:
  the three named numeric anchors (diagonal form ≈ ±√2/2, distances √2/2 and
  3√2/2, diagonal intersection == (0.5, 0.5)), parallel → None, coincident →
  None, vertical line x = 3 (`|A| ≈ 1`, `B ≈ 0`, distance 3.0), the three
  `TypeError` cases and the `ValueError` case, unnormalized-line distance,
  bad inputs on both `point_line_distance` and `lines_intersection`, and the
  property tests: `A² + B² == 1` within 1e-12 for many point pairs, defining
  points substitute back to distance 0, and intersection points substitute back
  to distance 0 in both lines. Also asserts sign pinning (never returns the
  negated form).

## What I did NOT do

- Did not implement motzkin or extractnums (other cards own those).
- Did not touch, move, or delete any existing file (git status shows only
  `line2d.py`, `tests/test_line2d.py`, `team/…` as new; `worker-prompt.txt`
  and `worker-stream.jsonl` were pre-existing untracked pipeline files).
- No third-party dependencies; only `math` from the standard library.
- No commit/push (left to the workflow).

## Checks I ran and results

1. `python3 -m pytest tests/test_line2d.py -q` → **19 passed** in 0.02s
2. `python3 -m pytest tests/ -q` → **361 passed, 2 skipped** in 18.34s (exit 0)

No `verdict.json` / `verdict.md` by-products appeared in the repo root, so
nothing to clean up there.

## Notes for the validator

- Anchor values are hard-coded in the tests as literals (e.g.
  `0.7071067811865476`, `2.1213203435596424`) and compared with relative
  error 1e-9 via the local `relclose` helper (`|got − want| ≤ tol·max(1,|want|)`);
  `lines_intersection` of the two diagonals is asserted with `== (0.5, 0.5)`.
- Parallel detection is relative (`1e-12` of the product of normal lengths), so
  it is dimensionally sound for both tiny and huge coefficients; coincident
  lines hit the same `|det| ≈ 0` branch and return `None`.
- Both acceptance checks were run exactly as specified in the card.
