# Handoff: bytefmt (sub-issue #425)

## What was requested

Work order #410, process card `bytefmt` (sub-issue #425): implement `bytefmt.py` with
`format_bytes(n: int) -> str` — IEC 1024 byte-size formatting — plus
`tests/test_bytefmt.py`, as new files only.

Spec (verbatim requirements):

- `n` is a non-negative integer; output is `"{value} {unit}"`.
- Unit sequence: `B`, `KiB`, `MiB`, `GiB`, `TiB` (each step 1024x).
- Below 1024: integer `B`; otherwise one decimal place.
- Negative `n` raises `ValueError`.
- Acceptance items, each needing a test case:
  - `format_bytes(0) == "0 B"`
  - `format_bytes(512) == "512 B"`
  - `format_bytes(1536) == "1.5 KiB"`
  - `format_bytes(1048576) == "1.0 MiB"`
  - `format_bytes(1536 * 1024) == "1.5 MiB"`
  - `format_bytes(-1)` raises `ValueError`

## What I did

- Created `bytefmt.py`: standard library only (no imports at all), no imports from
  `dms` or `kelvin`. `format_bytes` scales `n` by 1024 steps up to `TiB`, returns
  `f"{n} B"` for the `B` unit and `f"{value:.1f} {unit}"` otherwise, and raises
  `ValueError` for negative `n`.
- Created `tests/test_bytefmt.py`: one test function per acceptance item
  (6 tests), using `pytest.raises` for the negative case.

## What I did not do

- Did not create, modify, or delete `dms.py`, `kelvin.py`, or any other existing
  file (including `roman.py`, `legacy_stringkit.py`, existing tests, README).
- Did not modify `tests/` beyond adding `tests/test_bytefmt.py`.
- Did not add dependencies beyond the standard library / pytest.
- Did not commit or push.

## Checks run

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_bytefmt.py -q` | PASS — `6 passed` |
| `python3 -m pytest tests/ -q` | PASS — full suite green (includes pre-existing `test_roman.py` and `test_legacy_stringkit.py`) |

## Notes for the validator

- All six acceptance items are covered one-to-one by test functions; no other
  behavior is asserted (no extra edge-case tests beyond the spec).
- The implementation uses no imports, so it cannot collide with `dms` or `kelvin`.
- Formatting for values at or above `TiB` caps at `TiB` (per unit sequence limit);
  this edge is not in the acceptance list but follows the spec's unit sequence.
- Only two product files were added: `bytefmt.py` and `tests/test_bytefmt.py`.
  The two `team/` files are workflow artifacts required by the process card.
