# Handoff: cssunits (process card #830, sub-issue #830)

## What was requested

Implement the CSS length unit conversion widget for work order #813 round 54
concurrency-B batch, owning exactly two new files:

- `cssunits.py` — module with `css_convert(value, from_unit, to_unit, base_font_px=16.0, dpi=96.0) -> float`
- `tests/test_cssunits.py` — tests covering every acceptance item

Spec (verbatim from the card):

- Unit set pinned as `{px, pt, pc, in, cm, mm, em, rem}`.
- Convert through px as intermediary with pinned px factors: `px = 1`;
  `in = dpi`; `pt = dpi / 72`; `pc = dpi / 6`; `cm = dpi / 2.54`;
  `mm = dpi / 25.4`; `em = base_font_px`; `rem = base_font_px`.
- Result = `value * factor(from_unit) / factor(to_unit)`; return float, no rounding.
- Validation: value not numeric (int/float, bool rejected, must be finite)
  raises TypeError; from_unit/to_unit not str raises TypeError, not in unit set
  raises ValueError; base_font_px/dpi not numeric raises TypeError, <= 0 raises
  ValueError.
- Every acceptance line must have a corresponding test case (floats compared
  with abs diff < 1e-9).

## What I did

- Created `cssunits.py`:
  - `UNITS` frozenset of the 8 pinned units.
  - `_is_number(x)` helper: `isinstance(x, (int, float)) and not isinstance(x, bool)`.
  - `_px_factor(unit, base_font_px, dpi)` implementing the pinned factors.
  - `css_convert` performs validation in the order value → from_unit → to_unit
    → base_font_px → dpi, then computes `value * factor(from) / factor(to)`
    and returns a `float` (no rounding). Non-finite value/base_font_px/dpi raise
    TypeError (the card pins "must be finite" as part of the numeric check).
- Created `tests/test_cssunits.py` with 31 tests covering every acceptance line:
  - 16 conversion cases (all pinned approx expectations, 1e-9 tolerance).
  - ValueError cases: unknown to-unit `m`, `dpi=0`, `base_font_px=-1`, plus
    unknown from-unit and zero base_font_px.
  - TypeError cases: `"1"` value, `5` as from_unit, `True` value, `None` value,
    NaN/inf value, non-numeric base_font_px, non-numeric dpi, bool from_unit.
  - A no-rounding / returns-float check.
- Standard library only (`import math`); no imports of flesch or braille.

## What I did not do

- Did not create or modify `flesch.py`, `braille.py`, or their tests (owned by
  other process cards).
- Did not modify any pre-existing repository file.
- Did not commit or push.
- Installed dev dependencies (`pip3 install -r requirements-dev.txt`, which
  provides pytest) because pytest was not present in the environment; this only
  affects the environment, not repository files.

## Checks run and results

1. `python3 -m pytest tests/test_cssunits.py -q` → **31 passed in 0.02s**
2. `python3 -m pytest tests/ -q` → **218 passed, 2 skipped in 15.56s**

Both checks exit 0.

## Notes for the validator

- Float comparisons use `abs(actual - expected) < 1e-9` per the card.
- `css_convert` returns a plain `float` even for integral inputs (e.g.
  `css_convert(0, "pt", "mm") == 0.0`).
- The two skips in the full suite are pre-existing (unrelated to this card).
- No `verdict.json` / `verdict.md` by-products were produced by these checks
  (neither file exists in the repo root after the runs).
