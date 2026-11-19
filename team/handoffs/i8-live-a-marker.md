# Handoff: i8-live-a-marker (sub-issue #613)

## What was requested
Work order #611 [I8] API墙活验 A 采认失败. Deliverable: only the new file `docs/evidence/i8-scratch/a-marker.txt` containing a single line `i8-live-a` (with trailing newline). Acceptance: foreman produced exactly 1 process card; checks must include `test -f docs/evidence/i8-scratch/a-marker.txt`.

## What I did
- Created directory `docs/evidence/i8-scratch/` (did not exist) and created `docs/evidence/i8-scratch/a-marker.txt` with exactly one line: `i8-live-a` plus trailing newline.
- Wrote this handoff and the status file `team/status/i8-live-a-marker.json`.

## What I did not do
- Did not create or edit any other docs, code, tests, `team/` files other than the two required team files, or `.github/` files.
- Did not commit or push (workflow does that).

## Checks run and results
- `test -f docs/evidence/i8-scratch/a-marker.txt && test "$(head -n 1 docs/evidence/i8-scratch/a-marker.txt)" = "i8-live-a"` → PASS (exit 0).

## Notes for the validator
- The deliverable is a single-file addition; no code, tests, or schemas were touched.
- File content is exactly `i8-live-a\n` (one line, trailing newline).
- Untracked files `worker-prompt.txt` and `worker-stream.jsonl` in the repo root predate this process and were left untouched.
