# Handoff: temperature (sub-issue #56)

## What was requested
Implement `temperature.py` with four conversion functions, each returning a `float`:
- `c_to_f(c)` — Celsius to Fahrenheit
- `f_to_c(f)` — Fahrenheit to Celsius; raises `ValueError` when the converted result would be below absolute zero (f < -459.67)
- `c_to_k(c)` — Celsius to Kelvin; raises `ValueError` when c < -273.15
- `k_to_c(k)` — Kelvin to Celsius; raises `ValueError` when k < 0

Reference examples: `c_to_f(100) -> 212.0`, `f_to_c(32) -> 0.0`, `c_to_k(0) -> 273.15`, `k_to_c(0) -> -273.15`.

Plus `tests/test_temperature.py` covering the four examples, float return types, boundary values, and each `ValueError` case. Only the standard library; no imports of the other two modules; no package directory; no CLI.

## What I did
- Created `temperature.py` implementing the four functions with the specified absolute-zero guards. `c_to_f` accepts any input and returns a float (no guard required by spec).
- Created `tests/test_temperature.py` with 7 tests: the four examples, float-type checks, boundary values (-273.15 C, 0 K, -459.67 F, roundtrips), and one `ValueError` test per guarded function (`c_to_k(-300)`, `k_to_c(-1)`, `f_to_c(-460)`).

## What I did not do
- Did not touch `urlparse_mini.py`, `stack.py`, any other test file, or shared config.
- Did not add package directories or a CLI.
- Did not commit or push.

## Checks run and results
1. `python -m pytest -q tests/test_temperature.py` — **PASS** (7 passed in 0.02s). Note: `pytest` was not preinstalled; I installed it with `pip install -q pytest` first.
2. `python -c "from temperature import c_to_f, f_to_c, c_to_k, k_to_c; assert c_to_f(100) == 212.0 and f_to_c(32) == 0.0 and c_to_k(0) == 273.15 and k_to_c(0) == -273.15; print('ok')"` — **PASS** (printed `ok`).

## Notes for the validator
- Boundary values are inclusive: `c_to_k(-273.15)` returns `0.0` and `k_to_c(0)` returns `-273.15` without raising; only strictly-below values raise.
- `f_to_c(-459.67)` is accepted (result is exactly -273.15 within float tolerance); `f_to_c(-460)` raises.
- Full-repo `python -m pytest -q` depends on the other two modules' tests, which are owned by other processes; I only ran my own test file per my process card.
