# Handoff: i8-live-a-marker

## What was requested
Process card `i8-live-a-marker` (sub-issue #568) under work order #566 [I8] API墙活验 A 采认失败.

Deliverable: add exactly one file, `docs/evidence/i8-scratch/a-marker.txt`, containing exactly one line `i8-live-a` (with trailing newline). Also required: write this handoff and the status file `team/status/i8-live-a-marker.json`.

Acceptance criteria carried from the work order:
- foreman plan has exactly 1 process card (satisfied by the card itself)
- checks include `test -f docs/evidence/i8-scratch/a-marker.txt`

## What I did
1. `mkdir -p docs/evidence/i8-scratch` (plus `team/handoffs` and `team/status` so the required team files could be written).
2. Wrote `docs/evidence/i8-scratch/a-marker.txt` with the single line `i8-live-a` and a trailing newline.
3. Wrote `team/handoffs/i8-live-a-marker.md` (this file) and `team/status/i8-live-a-marker.json`.
4. Ran the process checks (results below).

## What I did NOT do
- Did not create, edit, or delete any other file.
- Did not add any test file.
- Did not touch `team/` paths other than the two required team files, and did not touch `.github/` paths (system-managed).
- Did not commit or push.

## Checks run and results
| Command | Result |
| --- | --- |
| `test -f docs/evidence/i8-scratch/a-marker.txt` | PASS (exit 0) |
| `grep -qx i8-live-a docs/evidence/i8-scratch/a-marker.txt` | PASS (exit 0, exact whole-line match) |

## Notes for the validator
- The marker file content is exactly `i8-live-a\n`; `grep -qx` confirms the whole line matches with no extra characters.
- The only deliverable owned by this card under `docs/` is `docs/evidence/i8-scratch/a-marker.txt`. The two files under `team/` are the handoff/status artifacts explicitly requested alongside the process card, not scope expansion.
- No commit was made; the workflow performs commit/push.
