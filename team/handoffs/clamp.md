# Handoff: clamp (sub-issue #93, r2 retry)

## What was requested
Process card #93 "Implement clamp module and tests (corrected acceptance check)":
- Own only `clamp.py` and `tests/test_clamp.py` (no other files, no shared config).
- `clamp(v, lo, hi)`: return `lo` when `v < lo`, `hi` when `v > hi`, otherwise `v` itself.
- Standard library only; no cross-module imports; no package dir; no CLI.
- `tests/test_clamp.py` covers only this module, including all four example values,
  with the corrected expectation `clamp(7, 0, 10) -> 7` (the v1 card's forced
  expectation of 10 was the plan fault that made the check unpassable; this retry
  corrects it so the in-range rule wins).
- Check command (verbatim from the card): `python -m pytest -q tests/test_clamp.py`

## What I did
- Created `clamp.py` with `clamp(v, lo, hi)` implementing the in-range rule.
- Created `tests/test_clamp.py` with four tests:
  - `clamp(5, 1, 10) == 5`
  - `clamp(-3, 0, 100) == 0`
  - `clamp(99, 0, 10) == 10`
  - `clamp(7, 0, 10) == 7` (corrected expectation, per this card)
- Ran the card's check from the repository root.

## What I did not do
- Did not touch `vowelcount`, `initials`, any other test file, or shared config.
- Did not commit or push.
- Did not alter the work-order acceptance text; only implemented the card's
  corrected expectation as instructed.

## Checks and results
- Environment note: `pytest` was not installed in this environment
  (`python -m pytest` reported "No module named pytest"). I installed it via
  `python3 -m pip install pytest` (pytest 9.2.0) so the mandated check could run.
- `python -m pytest -q tests/test_clamp.py` → exit 0, actual output:

```
....                                                                     [100%]
4 passed in 0.01s
```

## For the validator
- The single point of attention is the corrected acceptance: `clamp(7, 0, 10)`
  must be asserted as `7`, not `10`. All four tests pass and the check exits 0.
- `python -m pytest -q` (full suite) may include other processes' tests; this
  card's scope is only `tests/test_clamp.py`, which passes on its own.
