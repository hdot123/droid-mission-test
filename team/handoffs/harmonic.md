# Handoff: harmonic (sub-issue #822)

## What was requested

Implement the harmonic-number component of work order #815 (第54轮并发 D 单):

- `harmonic.py` at repo root exposing `harmonic(n) -> fractions.Fraction`, the exact
  harmonic number H_n = Σ_{k=1}^{n} 1/k, with H_0 = Fraction(0).
- Validation: `n` must be `int` (`bool` rejected, so `harmonic(True)` raises TypeError);
  non-int raises TypeError; `n < 0` raises ValueError.
- `tests/test_harmonic.py` with one pytest case per acceptance item (14 items).
- Constraints: only these two new files; no existing file modified; standard library only
  (`fractions.Fraction`); no import of `daycount360` or `sllist`.

## What I did

- Created `harmonic.py`: type check first (`isinstance(n, bool) or not isinstance(n, int)`
  -> TypeError), then `n < 0` -> ValueError, then accumulate `Fraction(1, k)` for k in
  `range(1, n + 1)` starting from `Fraction(0)`. Exact rational arithmetic throughout.
- Created `tests/test_harmonic.py`: 14 tests, one per acceptance item —
  H_0/H_1/H_2/H_3/H_4/H_5/H_6/H_10/H_20 values, `isinstance(harmonic(7), Fraction)`,
  `harmonic(-1)` -> ValueError, and `harmonic(2.5)` / `harmonic("5")` / `harmonic(True)`
  -> TypeError. Test style matches the existing `tests/test_roman.py` (pytest.raises).

## What I did not do

- Did not touch `daycount360.py`, `sllist.py`, or their tests (other process cards).
- Did not modify or delete any pre-existing repository file.
- Did not add any file outside `harmonic.py`, `tests/test_harmonic.py`,
  `team/handoffs/harmonic.md`, `team/status/harmonic.json`.
- Did not commit or push (workflow does that).
- Note: `pytest`/`jsonschema` were not installed in the environment; I installed them via
  `python3 -m pip install pytest jsonschema` (from `requirements-dev.txt`) to run the
  checks. No repository file changed for this.

## Checks run

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_harmonic.py -q` | PASS — 14 passed in 0.02s (exit 0) |
| `python3 -m pytest tests/ -q` | PASS — 201 passed, 2 skipped in 16.33s (exit 0) |

The 2 skips are pre-existing suite skips, unrelated to this card (they were present in
the baseline suite; harmonic contributes 14 passing tests). No `verdict.json` /
`verdict.md` by-products were produced by these runs (verified absent afterward).

## Validator attention points

- Order of validation matters for the error-type checks: TypeError for non-int (including
  bool) must be raised before the `n < 0` ValueError check, otherwise `harmonic(-1.5)`
  would report the wrong exception type; the spec's listed cases are all covered.
- `harmonic(True)` must raise TypeError, not be treated as 1 — the explicit
  `isinstance(n, bool)` guard handles this since bool subclasses int.
- All expected values are exact `Fraction` equality (not float comparison); the H_20
  expected value `Fraction(55835135, 15519504)` is the exact numerator/denominator.
- Full-suite run must be done post-merge with all three components present; the
  baseline suite is green without them, and this card adds only passing tests.
