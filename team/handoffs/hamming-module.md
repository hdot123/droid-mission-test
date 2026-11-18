# Handoff: hamming-module (sub-issue #210)

## What was requested
Implement `hamming.py` at the repository root plus `tests/test_hamming.py`, owning only those two files:
- `hamming_distance(a, b)`: count of positions where two equal-length strings differ; raise `ValueError` on length mismatch.
- `is_within(a, b, k)`: return `hamming_distance(a, b) <= k`; length mismatch also raises `ValueError` (propagated from `hamming_distance`).
- Required examples: `hamming_distance("karolin", "kathrin") == 3`, `hamming_distance("1011101", "1001001") == 2`, `is_within("karolin", "kathrin", 3) is True`, `is_within("karolin", "kathrin", 2) is False`.
- Standard library only, no package directory, no CLI, no imports of other project modules; test file tests only this module.
- Card check (verbatim): `python -m pytest -q tests/test_hamming.py`

## What I did
- Created `hamming.py` with `hamming_distance` and `is_within` per spec (ValueError on unequal lengths).
- Created `tests/test_hamming.py` with 11 tests covering both signatures, all four required examples, identical/empty/completely-different strings, zero and negative thresholds, and both ValueError cases (unequal lengths for `hamming_distance` and for `is_within`).
- Installed pytest 9.2.0 via `python3 -m pip install pytest` (the environment had no pytest module initially; `python -m pytest` failed with "No module named pytest" before the install).
- Ran the card's check command verbatim: `python -m pytest -q tests/test_hamming.py` → **11 passed in 0.01s** (exit code 0).

## What I did not do
- Did not touch `isbn10.py`, `caesar.py`, any other test file, or any `team/**`/`.github/**` paths other than my own two handoff/status files.
- Did not create a package directory or CLI; did not add cross-module imports.
- Did not commit or push anything.

## Checks run and results
| Command (verbatim from check column) | Result |
| --- | --- |
| `python -m pytest -q tests/test_hamming.py` | 11 passed in 0.01s (exit code 0) |

## Notes for the validator
- First run of the check failed only because pytest was not installed in the environment; after `python3 -m pip install pytest` (pytest 9.2.0) the same command passes. The passing evidence is from the verbatim check command.
- Test file imports only `hamming` and `unittest`; no other project modules are imported.
- Environment note: system `python` is Python 3.14 (`/usr/bin/python`).
