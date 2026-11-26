# Handoff: speedconv (sub-issue #869, work order #850, card retry r2)

## What was requested

Process card `speedconv` (REVISE retry, branch suffix `-r2`): create exactly two code
files — `speedconv.py` and `tests/test_speedconv.py` — implementing
`convert_speed(value, from_unit, to_unit) -> float` per the verbatim acceptance
criteria in work order #850 (round 55, concurrent card C):

- Unit set `{m/s, km/h, mph, kn, ft/s}`, converted through a base of m/s.
- Coefficients pinned with full precision: m/s = 1, km/h = 1/3.6,
  mph = 1609.344/3600, kn = 1852/3600, ft/s = 0.3048.
- Unknown units (including case mismatches `"MS"`, `"knots"`, `"fps"`) raise `ValueError`.
- Float acceptance tolerance: relative error 1e-9 for every approx check.
- Round-trip over ALL unit pairs: `convert_speed(convert_speed(37.5, u1, u2), u2, u1)`
  restores 37.5 within rel 1e-9 for every ordered pair.
- CARD PIN (v2): the ONLY mandated check is `python3 -m pytest tests/test_speedconv.py -q`
  (must exit 0). The full-suite run is deliberately out of card scope.

Plus two team files: this handoff and `team/status/speedconv.json`.

## What I did

- Created `speedconv.py`: module docstring documents the coefficients;
  `_TO_METERS_PER_SECOND` dict pins each coefficient exactly as specified
  (`1`, `1/3.6`, `1609.344/3600`, `1852/3600`, `0.3048`);
  `convert_speed` looks up both units (KeyError/TypeError from unhashable/None
  inputs converted to `ValueError`) and computes `value * factor_from / factor_to`.
  Standard library only; no imports from sibling modules.
- Created `tests/test_speedconv.py`: one test per acceptance example (11 named
  examples), a parametrized round-trip over all 25 ordered unit pairs with 37.5
  and rel 1e-9, three unknown-unit `ValueError` cases plus an unknown-target case,
  identity/convention checks, and coefficient pinning. All approx assertions use
  `pytest.approx(..., rel=1e-9)`.

## What I did NOT do

- Did not modify, create, skip, or seed any existing file. Only the four card
  deliverables exist: `speedconv.py`, `tests/test_speedconv.py`,
  `team/handoffs/speedconv.md`, `team/status/speedconv.json`.
- Did not implement `titlecase` or `divisorsum` (other cards own those).
- Known out-of-scope context (mentioned once, per card): the full-suite command
  `python3 -m pytest tests/ -q` exits 1 solely from a pre-existing environmental
  `FileNotFoundError` under `/tmp/r54-audit/` in
  `tests/test_check_summary_focused_counts.py`. It belongs to no process on this
  plan; I did not fix, modify, skip, or seed it, and it is not a card check.
- Did not commit or push.

## Checks run

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_speedconv.py -q` | **47 passed**, exit 0 |

## What the validator must pay attention to

- The card pin (v2) mandates only the module check above; it exits 0.
- Round-trip coverage is exhaustive over all 25 ordered pairs, as the spec's
  "全单位对往返" requires.
- Unknown-unit rejection covers both the unit keys and case mismatches; note
  `"fps"` and `"knots"` fail because exact-key lookup is case/alias sensitive by design.
- The full-suite failure in `tests/test_check_summary_focused_counts.py` is
  environmental and out of card scope — do not treat it as a defect of this card.
