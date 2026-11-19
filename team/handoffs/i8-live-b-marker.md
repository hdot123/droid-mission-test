# Handoff: i8-live-b-marker (sub-issue #620)

## What was requested
Work order #617 [I8] API wall live verification B (comment hard failure). Process card `i8-live-b-marker` scoped to exactly one deliverable:

- Create `docs/evidence/i8-scratch/b-marker.txt` (creating the directory if needed) containing exactly one line: `i8-live-b`.
- Acceptance: exactly 1 process card; check `test -f docs/evidence/i8-scratch/b-marker.txt`.

## What I did
- Created directory `docs/evidence/i8-scratch/` (it did not exist).
- Created `docs/evidence/i8-scratch/b-marker.txt` with a single line `i8-live-b` (plus trailing newline).
- Wrote this handoff and `team/status/i8-live-b-marker.json`.

## What I did not do
- Did not touch any application code, `team/` files other than the two required, or `.github/` paths.
- Did not create, edit, or delete any file outside my scope: only `docs/evidence/i8-scratch/b-marker.txt`, `team/handoffs/i8-live-b-marker.md`, `team/status/i8-live-b-marker.json`.
- Did not commit or push (left for the workflow).
- Did not run any dispatch/verification scenario; this process is marker-only per the process card.

## Checks run and results
- `test -f docs/evidence/i8-scratch/b-marker.txt` → PASS (exit 0).

## Notes for the validator
- The deliverable is a marker file only; it does not itself prove the B-scenario hard-failure behavior, only that this process card completed.
- File content is exactly one line: `i8-live-b`.
