# Handoff: d-m4-marker (sub-issue #594)

## What was requested
Process card `d-m4-marker` under work order #589 [I8] API墙活验 D 半套artifact (scenario D: half-set artifact, validate accepts the failure, complete=false).

- Owns exactly one deliverable file: `docs/evidence/i8-scratch/d-m4.txt`
- The file must contain the line `i8-live-d-m4`
- Acceptance check: `test -f docs/evidence/i8-scratch/d-m4.txt`
- Also required: this handoff and the status JSON.

## What I did
1. Created the directory `docs/evidence/i8-scratch/` (it did not exist).
2. Created `docs/evidence/i8-scratch/d-m4.txt` containing exactly one line: `i8-live-d-m4` (with trailing newline).
3. Created `team/handoffs/d-m4-marker.md` (this file) and `team/status/d-m4-marker.json`.

## What I did not do
- Did not create or modify the other five markers: `d-m1.txt`, `d-m2.txt`, `d-m3.txt`, `d-m5.txt`, `d-m6.txt` (owned by other process cards).
- Did not touch any shared scratch content, `team/` files owned by other processes, `.github/` files, or any source file.
- Did not commit or push (workflow handles that).

## Checks run and results
- `test -f docs/evidence/i8-scratch/d-m4.txt` → PASS (exit 0)
- File content verified: `cat` printed `i8-live-d-m4`, single line, 13 bytes (12 chars + newline).

## Notes for the validator
- The work order's acceptance criteria describe all 6 markers existing; this card is only responsible for `d-m4.txt`. The other five are owned by sibling process cards — do not fail this card if they are absent at the time of this card's validation.
- The marker content is the literal string `i8-live-d-m4` on one line.
