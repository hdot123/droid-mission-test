# Handoff: i8-d-marker

## What was requested
Process card `i8-d-marker` (sub-issue #585) under work order #583 [I8] API墙活验 D 半套artifact:
create exactly one deliverable, `docs/evidence/i8-scratch/d-marker.txt`, containing the single line `i8-live-d`. Scenario D is a half-set artifact (validate acknowledges failure, complete=false).

## What I did
- Created `docs/evidence/i8-scratch/d-marker.txt` with one line: `i8-live-d`.
- Wrote this handoff and `team/status/i8-d-marker.json`.

## What I did not do
- Did not modify any other `docs/`, code, test, `team/` (other processes'), or `.github/` files.
- Did not commit or push (workflow owns that).
- Did not touch any other process's files or expand scope.

## Checks run
- `test -f docs/evidence/i8-scratch/d-marker.txt` → pass (exit 0).

## Notes for the validator
- Only one process card was executed: `i8-d-marker`.
- Acceptance criterion (2) is the file-existence check above; result was pass.
- The marker file contains exactly the line `i8-live-d` (plus trailing newline).
