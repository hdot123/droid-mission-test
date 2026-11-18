# Handoff: manchester-module (sub-issue #260)

## What was requested
Implement `manchester.py` with an IEEE 802.3 Manchester codec plus `tests/test_manchester.py`, scoped strictly to those two files:
- `encode(bits)`: input string of only `'0'`/`'1'`; `'1'` -> `"10"`, `'0'` -> `"01"`; returns doubled-length string; any other character raises `ValueError`.
- `decode(signal)`: even-length signal; `"10"` -> `'1'`, `"01"` -> `'0'`; odd length or illegal pairs (`"00"`, `"11"`, etc.) raise `ValueError`.
- Required examples: `encode("1") -> "10"`, `encode("0") -> "01"`, `encode("1011") -> "10011010"`, `encode("") -> ""`, `decode("10011010") -> "1011"`.
- Standard library only; no imports of other modules; no package directory; no CLI.

## What I did
- Created `manchester.py` with `encode(bits)` and `decode(signal)`, using internal encode/decode pair maps. Both raise `ValueError` (including on non-`str` inputs) per spec.
- Created `tests/test_manchester.py` covering all five required examples, round-trip, and every `ValueError` case (non-bit chars, odd-length decode, `"00"`/`"11"`/mixed/invalid pairs).

## What I did not do
- Did not touch `base32hex.py`, `crc8.py`, `roman.py`, `legacy_stringkit.py`, or any other test file.
- Did not create package directories, a CLI, or any cross-module imports.
- Did not commit or push anything.

## Checks run and results
- `python -m pytest -q tests/test_manchester.py` — could not run at first: this environment's `python`/`python3` had no `pytest` module (`No module named pytest`).
- Installed pytest via `python3 -m pip install pytest`, then ran the required check verbatim as `python3 -m pytest -q tests/test_manchester.py` → **6 passed in 0.02s** (exit 0).
- The check command from the card (`python -m pytest -q tests/test_manchester.py`) is identical modulo the interpreter name; `python` in this container is `/usr/bin/python` and still lacks pytest, so `python3` was used to actually execute the suite. Validator should run the check with whichever interpreter has pytest available.

## Notes for validator
- File ownership: only `manchester.py` and `tests/test_manchester.py` were created; nothing else was modified.
- Test suite is self-contained: imports only `manchester` and `pytest`.
- All required examples and ValueError paths are asserted in the test file.
