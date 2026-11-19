# Handoff: i8-live-a-marker (sub-issue #563)

## What was requested
Work order [I8] API墙活验 A 采认失败 (#561), process card `i8-live-a-marker`:
- Deliverable: `docs/evidence/i8-scratch/a-marker.txt` containing exactly one line, `i8-live-a` (plus trailing newline).
- Acceptance check: `test -f docs/evidence/i8-scratch/a-marker.txt`
- Scope: own only that deliverable file; do not touch other docs, tests, `team/` files owned by others, or `.github/` workflows.

## What I did
- Created directory `docs/evidence/i8-scratch/` (did not exist) and the file `docs/evidence/i8-scratch/a-marker.txt` with content `i8-live-a\n`.
- Wrote this handoff at `team/handoffs/i8-live-a-marker.md` and status at `team/status/i8-live-a-marker.json`, as instructed by the worker instructions.

## What I did not do
- Did not create, edit, or delete any other file (no docs, tests, `team/` files from other processes, no `.github/` workflows).
- Did not commit or push (workflow handles that).
- Did not expand scope beyond this single process card.

## Checks run and results
- `test -f docs/evidence/i8-scratch/a-marker.txt` → passed (exit 0). See status JSON for the recorded result.

## For the validator
- The deliverable is a one-line file: `i8-live-a` with a trailing newline. Content check: `cat docs/evidence/i8-scratch/a-marker.txt` should print `i8-live-a`.
- Foreman has exactly 1 process card for this work order; this card is that card.
- The only repo files I authored are: `docs/evidence/i8-scratch/a-marker.txt`, `team/handoffs/i8-live-a-marker.md`, `team/status/i8-live-a-marker.json`.
