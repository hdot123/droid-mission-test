# Handoff: i8-d-m5 (sub-issue #607)

## What was requested
Process card `i8-d-m5` under work order #601 ([I8] API wall live-verification scenario D, half artifact): create exactly one marker file `docs/evidence/i8-scratch/d-m5.txt` containing the single line `i8-live-d-m5` followed by a newline, as one of six separate deliverables (validate accepts, complete=false). Scope was limited to that one file; no other marker files, evidence files, or anything outside `docs/evidence/i8-scratch/` (plus the two mandated team files) could be touched.

## What I did
1. Created the directory `docs/evidence/i8-scratch/` (`mkdir -p`, then listed it).
2. Created `docs/evidence/i8-scratch/d-m5.txt` containing exactly:
   ```
   i8-live-d-m5
   ```
   (single line, trailing newline).
3. Wrote this handoff at `team/handoffs/i8-d-m5.md` and the status file `team/status/i8-d-m5.json`.
4. Ran the process check.

## What I did NOT do
- Did not create or modify `d-m1.txt`, `d-m2.txt`, `d-m3.txt`, `d-m4.txt`, or `d-m6.txt` (each is owned by another process).
- Did not modify any pre-existing file, including anything already in `docs/evidence/i8-scratch/`.
- Did not commit or push (the workflow does that).
- Did not touch anything outside the allowed paths.

## Checks run and results
- `test -f docs/evidence/i8-scratch/d-m5.txt` → **passed** (exit 0).
- Content verified as the single line `i8-live-d-m5` plus newline.

## Notes for the validator
- Scenario D is a half artifact by design: only `d-m5.txt` exists from this process; expect the other five markers to arrive from their own processes. Do not treat the absence of `d-m1`–`d-m4`, `d-m6` from this card as a failure of this card.
- The card's single check is `test -f docs/evidence/i8-scratch/d-m5.txt`; it passes.
- Directory `docs/evidence/i8-scratch/` was created if it did not exist (it was empty when listed).
