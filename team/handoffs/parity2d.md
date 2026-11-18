# Handoff: parity2d (sub-issue #284)

## What was requested
Process card #284 under work order #279 (round 35, concurrency group C): implement the 2D parity component with exactly two new files, `parity2d.py` and `tests/test_parity2d.py`. No existing file may be modified; the three components must use only the standard library and must not import each other. Every acceptance item needs a test case.

Spec (as given):
- `add_parity(rows: list[str]) -> list[str]` — input is a non-empty list of equal-length '0'/'1' strings (at least 1 row and 1 column); append a row-parity bit to each row, then append a column-parity row whose entries are each column's even parity, with the corner cell being the parity of the whole block. Raise `ValueError` on empty list, unequal row lengths, or any character outside '0'/'1'.
- `locate_error(block: list[str]) -> tuple[int, int] | None` — input is a checked block (output shape of `add_parity`); `None` when all checks pass; `(row, col)` when exactly one row check and one column check fail (the intersection, the actually flipped bit, 0-based, data region or check region); `ValueError` for any other failure shape (e.g. multiple failing rows/columns) or malformed input.

## What I did
- Created `parity2d.py` with `add_parity` and `locate_error`. Both funnel shape/content validation through a shared `_validate` helper: empty list, unequal row lengths, non-'0'/'1' characters always raise `ValueError`. `add_parity` also requires ≥1 row and ≥1 column; `locate_error` requires the checked-block shape (≥2 rows and ≥2 columns) so a bare data row or empty list raises `ValueError` instead of silently "passing".
- Row/column check failure is computed as odd parity of the full row/column (data bit plus check bit), so a flip in the check row, check column, or corner cell is located at its own coordinates.
- Created `tests/test_parity2d.py` with 18 tests covering every acceptance item: the `add_parity(["101", "010"]) == ["1010", "0101", "1111"]` example; `locate_error` → `None` on the clean block; flip at (0,1) → `(0, 1)`; check-row flip located at its own position; `add_parity(["10", "1"])` raises `ValueError`. Also covered: check-column and corner flips, exhaustive single-bit flips on a 4×5 block, all-even invariant on output, empty list, empty row, invalid characters, 1×1 blocks, two-error patterns (same row, same column, scattered), and malformed `locate_error` inputs. Input non-mutation is asserted too.

## What I did not do
- Did not touch `hamming74.py`, `crc16.py`, any other test file, or any existing repository file — deliverables are new files only.
- Did not add cross-imports (standard library only, no import of hamming74 or crc16).
- Did not commit or push (workflow does that).
- Note: `pytest` was not present in the environment, so I installed it via `pip install pytest` to run the required checks. This is an environment change only, not a file change.

## Checks run (verbatim commands)
- `python3 -m pytest tests/test_parity2d.py -q` → **18 passed**
- `python3 -m pytest tests/ -q` → **29 passed** (11 pre-existing + 18 new)

## For the validator
- Acceptance items to spot-check directly: `add_parity(["101", "010"]) == ["1010", "0101", "1111"]`; clean-block `locate_error` → `None`; flip (0,1) → `(0,1)`; check-row flip located at its own index; `add_parity(["10", "1"])` → `ValueError`.
- All `ValueError` clauses are raised as `ValueError` (not a subclass/other exception): empty list, unequal lengths, bad characters, and the `locate_error` failure-shape cases.
- The corner-cell behavior: a flip in the check row (including the corner) fails exactly that row and exactly that column (the check column's parity), so `locate_error` returns the corner's own coordinates, e.g. `(2, 3)` for the base example — this matches "pointing at the actually flipped bit in the check region".
- Only `parity2d.py` and `tests/test_parity2d.py` were created; no existing file was modified (`git status` should show only new files plus this team output).
