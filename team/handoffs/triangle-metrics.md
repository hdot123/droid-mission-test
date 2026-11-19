# Handoff: triangle-metrics (sub-issue #488)

## What was requested

Process card `triangle-metrics` under work order #479 (第 46 轮 B): implement
`triangle.py` (triangle classification and metrics) and `tests/test_triangle.py`,
covering every acceptance item in the work order verbatim, using only the
standard library, without importing other project modules, and without touching
any existing file.

## What I did

- Created `triangle.py` with:
  - `classify(a, b, c) -> str` — `"equilateral"` / `"isosceles"` / `"scalene"`.
  - `area(a, b, c) -> float` — Heron's formula.
  - `inradius(a, b, c) -> float` — area / semiperimeter.
  - `circumradius(a, b, c) -> float` — `a*b*c / (4*area)`.
  - Shared private `_validate(a, b, c)`: rejects `bool` and non-`int`/`float`
    with `TypeError`; rejects sides ≤ 0 and violations of the strict triangle
    inequality (`a+b>c`, `a+c>b`, `b+c>a`) with `ValueError`.
  - Only `math` from the standard library; no project-module imports.
- Created `tests/test_triangle.py` with 20 tests covering every acceptance
  item: all four classification examples, `area`/`inradius`/`circumradius`
  exact and 1e-9-tolerance cases, degenerate/zero/negative/inequality
  `ValueError`s, and non-numeric/`None`/`bool` `TypeError`s.
- Tolerance assertions are written as `abs(actual - expected) <= 1e-9`
  (the exact wording of the spec) rather than `pytest.approx`.

## What I did NOT do

- Did not touch `bloom.py`, `pangram.py`, `roman.py`, `legacy_stringkit.py`,
  or any file under `tests/` other than the new `tests/test_triangle.py`.
- Did not create or modify anything under `team/` other than the two required
  files `team/handoffs/triangle-metrics.md` and `team/status/triangle-metrics.json`.
- Did not commit or push (left to the workflow).
- Did not expand scope beyond the process card.

## Checks run and results

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_triangle.py -q` | 20 passed |
| `python3 -m pytest tests/ -q` | 31 passed |

Note: pytest was not present in the environment; I installed it with
`python3 -m pip install pytest` (pytest 9.2.0) to run the required checks.
No repository files were changed by that install.

## What the validator must pay attention to

- Only two files were added by this process: `triangle.py` and
  `tests/test_triangle.py` (plus the two `team/` files). No existing file was
  modified.
- Float tolerance cases use `<= 1e-9` absolute difference, exactly as the work
  order words it.
- Validation order matters: `TypeError` is raised for non-numeric input
  (including `bool`, `str`, `None`) before any `ValueError` checks, so e.g.
  `classify("3", 4, 5)` raises `TypeError` even though such input would also
  fail the numeric inequality checks.
- Degenerate triangles (`1, 2, 3`) are rejected by the strict inequality even
  though each side is positive.
