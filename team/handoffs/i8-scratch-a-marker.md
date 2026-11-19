# Handoff: i8-scratch-a-marker (sub-issue #558)

## What was requested
Work order #556 [I8] scenario A: add a single minimal deliverable file
`docs/evidence/i8-scratch/a-marker.txt` containing exactly one line `i8-live-a`
(with trailing newline), to observe acceptance under the foreman pattern
(exactly 1 process card).

## What I did
- Created `docs/evidence/i8-scratch/a-marker.txt` with content `i8-live-a\n`.
- Wrote this handoff and `team/status/i8-scratch-a-marker.json`.

## What I did not do
- Did not modify any other file (no `team/` files other than the two required,
  no `team/` process files owned by others, no `.github/` paths).
- Did not commit or push (workflow handles that).
- Did not touch `roman.py`, `legacy_stringkit.py`, `tests/`, `docs/` other than
  the new marker, or any other process's deliverables.

## Checks ran and results
- `test -f docs/evidence/i8-scratch/a-marker.txt` → exit 0 (pass).
- Content verified: file contains exactly `i8-live-a` plus trailing newline.

## Notes for the validator
- The only deliverable is the marker file; its existence is the acceptance
  criterion (`test -f docs/evidence/i8-scratch/a-marker.txt`).
- Status JSON is at `team/status/i8-scratch-a-marker.json`, state `done`.
