# Handoff — solids.py (sub-issue #776, work order #764 D单)

## What was requested

Implement `solids.py` and `tests/test_solids.py` only (new files; no existing file modified), for the 第52轮 并发 D 单 work order #764. Ten functions for common solid volume/surface area, standard library only (`math.pi`), results as `float`, no imports of the sibling modules (`numwords`, `code39`).

Spec recap:

- Functions: `sphere_volume(r)`, `sphere_surface(r)`, `cylinder_volume(r, h)` (closed, both bases), `cylinder_surface(r, h)`, `cone_volume(r, h)`, `cone_surface(r, h)` (base included, slant = √(r²+h²)), `box_volume(l, w, h)`, `box_surface(l, w, h)`, `pyramid_volume(b, h)`, `pyramid_surface(b, h)` (regular square pyramid: base square side b, surface = b² + 2b·slant, triangle slant = √((b/2)²+h²)).
- Formulas: sphere V=4πr³/3, S=4πr²; cylinder V=πr²h, S=2πr²+2πrh; cone V=πr²h/3, S=πr²+πr·slant; box V=lwh, S=2(lw+lh+wh); pyramid V=b²h/3, S=b²+2b·slant.
- Every dimension argument: positive int/float, bool rejected; non-numeric → `TypeError`; ≤ 0 → `ValueError`.

## What I did

- Created `solids.py` with a shared `_dim(value, name)` validator (rejects `bool`, rejects non-`int`/`float`, rejects ≤ 0) used by all ten functions, and the ten functions implemented exactly per the formulas above with `math.pi`.
- Created `tests/test_solids.py` with a test case for **every** acceptance item in the card: all 18 float/equality values (within `1e-9`), all 5 `ValueError` cases, all 3 `TypeError` cases, plus extras (bool/non-numeric rejected across functions, other non-positive dimensions, results-are-float).
- One adjustment made during testing: `box_volume` originally returned a bare int for int inputs (`2*3*4 == 24`); the spec says results are `float`, so box volume/surface now wrap the product with `float(...)`. The acceptance equality `box_volume(2, 3, 4) == 24` and `box_surface(2, 3, 4) == 52` still hold (24.0 == 24 is True).

## What I did not do

- Did not touch `numwords.py`, `code39.py`, or any existing file (only the six new-file scope of the D单, of which I own two plus the two team files).
- Did not import any non-stdlib module or the sibling worker modules.
- Did not commit or push (left to the workflow).
- Note: `pytest` was not installed in the environment (`python3 -m pytest` initially failed with "No module named pytest"); I installed it with `python3 -m pip install pytest` (pytest 9.2.0) to run the required checks. This touched no repository file.

## Checks run and results

- `python3 -m pytest tests/test_solids.py -q` → **31 passed**
- `python3 -m pytest tests/ -q` → **168 passed, 1 skipped** (the skip is a pre-existing test, unrelated to this change)

## Notes for the validator

- Float tolerance: tests use `pytest.approx(..., abs=1e-9)` as the card requires ("浮点值须在 1e-9 内相等").
- Exact-equality items (`box_volume(2,3,4) == 24`, `box_surface(2,3,4) == 52`, `pyramid_volume(2,3) == 4`, `pyramid_volume(6,4) == 48`, `pyramid_surface(6,4) == 96`) are asserted with `==` directly and pass because the float values are exact for these inputs.
- `bool` rejection is enforced before the numeric check (`isinstance(value, bool)` first), so `pyramid_volume(True, 3)` raises `TypeError`, not `ValueError`.
- Result type: all ten functions return `float` (verified by `test_results_are_float`); the box functions wrap their products in `float(...)` because pure-int inputs would otherwise yield an int.
