# Handoff: crockford32 (sub-issue #290)

## What was requested
Implement the Crockford Base32 component of work order #277 (round 35, group A):
- New module `crockford32.py` with `encode(n: int) -> str` and `decode(s: str) -> int`.
- New test file `tests/test_crockford32.py` covering every acceptance item.
- Only new files; no existing file may be modified; standard library only; no imports from sibling modules.

Spec highlights:
- Alphabet exactly `0123456789ABCDEFGHJKMNPQRSTVWXYZ` (no I, L, O, U), uppercase output, no padding, `encode(0) == "0"`, negative input raises `ValueError`.
- `decode` uppercases first, maps `I`/`L` -> `1` and `O` -> `0`, rejects any other out-of-alphabet character (including `U`) with `ValueError`, and rejects the empty string with `ValueError`.

## What I did
- Created `crockford32.py`: `ALPHABET` constant, `encode` (base-32 conversion with negative check), `decode` (alias mapping then alphabet lookup; raises `ValueError` on empty string or invalid character).
- Created `tests/test_crockford32.py` with 10 tests, one per acceptance item:
  1. `encode(123456789) == "3NQK8N"`
  2. `decode("3NQK8N") == 123456789`
  3. `decode("3nqk8n") == 123456789`
  4. `decode("O") == 0`
  5. `decode("L") == 1`
  6. `decode("U")` raises `ValueError`
  7. `encode(-1)` raises `ValueError`
  8. round-trip identity for 0, 1, 31, 32, 1024
  9. `encode(0) == "0"` (also asserted inside the round-trip case)
  10. `decode("")` raises `ValueError`

## What I did NOT do
- Did not create or touch `fletcher16.py`, `zigzag.py`, `tests/test_fletcher16.py`, `tests/test_zigzag.py`, or any other process's files.
- Did not modify any pre-existing file (README.md, roman.py, legacy_stringkit.py, existing tests, CI config).
- Did not commit or push.
- Did not add any non-standard-library dependency.

## Checks run and results
pytest was not installed in the environment, so I installed it first (`python3 -m pip install pytest`, pytest 9.2.0), then ran:

- `python3 -m pytest tests/test_crockford32.py -q` -> `10 passed in 0.01s` (exit 0)
- `python3 -m pytest tests/ -q` -> `21 passed in 0.02s` (exit 0) (10 crockford32 + 11 pre-existing roman/stringkit tests)

Both required checks pass.

## Notes for the validator
- The module exposes a public `ALPHABET` constant; the spec does not forbid it and no check depends on its absence or presence.
- `decode` relies on `str.upper()` before alias mapping, so lowercase input works; `I`, `L`, `O` are handled after uppercasing, so lowercase `i`/`l`/`o` also map correctly (not required by spec but consistent with it).
- Out-of-alphabet characters raise `ValueError` with a message naming the character; `U` is not in the alphabet so it is rejected, as required.
- The test file mirrors the acceptance list one-to-one; if the validator's own tests use different wording (e.g. expecting a specific exception type), `ValueError` is what the spec mandates and what is raised.
- Full-suite green includes tests owned by other processes; a failure there is not attributable to this component unless it imports `crockford32`.
