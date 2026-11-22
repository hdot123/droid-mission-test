# Handoff: temperature-convert (sub-issue #183)

## What was requested
Implement `temperature.py` in the repository root with exactly three public functions, each returning a float:
- `c_to_f(c)` — Celsius to Fahrenheit
- `f_to_c(f)` — Fahrenheit to Celsius
- `c_to_k(c)` — Celsius to Kelvin

Required examples: `c_to_f(0) -> 32.0`; `c_to_f(100) -> 212.0`; `f_to_c(212) -> 100.0`; `c_to_k(-273.15) -> 0.0`.

Also create `tests/test_temperature.py` covering only this module: the four examples above, float return types, and round-trip consistency of `c_to_f`/`f_to_c`.

Constraints: Python standard library only; no imports of `vigenere.py` or `ean13.py`; no package directory; no CLI.

## What I did
- Created `temperature.py` with the three functions, all returning floats (inputs coerced via `float(...)` so int inputs still yield float results):
  - `c_to_f(c) = float(c) * 9.0 / 5.0 + 32.0`
  - `f_to_c(f) = (float(f) - 32.0) * 5.0 / 9.0`
  - `c_to_k(c) = float(c) + 273.15`
- Created `tests/test_temperature.py` with tests for the four required examples, float return types of all three functions, and a parametrized `c_to_f`/`f_to_c` round trip (`pytest.approx`).
- Installed `pytest` via `python -m pip install` because it was not present in the environment (needed to run the mandated checks).

## What I did not do
- Did not create or modify `vigenere.py`, `ean13.py`, or their test files (owned by other processes).
- Did not touch any `team/` files other than this handoff and my own `team/status/temperature-convert.json`, nor any `.github/` path.
- No package directory, no CLI, no non-standard-library imports.
- Did not commit or push (workflow handles that).

## Checks run and results
1. `python -m pytest -q tests/test_temperature.py` → exit 0, `11 passed`
2. `python -m pytest -q` → exit 0, `11 passed` (only the temperature tests exist in the repo at this point; the full run will cover the other modules as they land)

## Notes for the validator
- The first attempt at check 1 failed only because `pytest` was not installed (`No module named pytest`); after installing it, both checks pass as shown above. This is an environment issue, not a code issue.
- Function signatures match the spec exactly: `c_to_f(c)`, `f_to_c(f)`, `c_to_k(c)`; all return `float`.
- Behavior matches the four required examples exactly (`== 32.0`, `== 212.0`, `== 100.0`, `== 0.0` — exact float equality holds for these values).
- The test file imports only `temperature` and `pytest`; no cross-module imports.
