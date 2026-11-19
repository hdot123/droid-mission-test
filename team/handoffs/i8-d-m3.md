# Handoff: i8-d-m3 (sub-issue #605)

## What was requested
Process card `i8-d-m3` under work order #601 ([I8] API墙活验 D 半套artifact, scenario D: half artifact, `complete=false`):

- Create exactly one file, `docs/evidence/i8-scratch/d-m3.txt`, containing exactly the single line `i8-live-d-m3` followed by a newline.
- Run the process check: `test -f docs/evidence/i8-scratch/d-m3.txt`.
- Write this handoff (`team/handoffs/i8-d-m3.md`) and the status file (`team/status/i8-d-m3.json`).
- Do not commit or push.

## What I did
1. Inspected `docs/evidence/i8-scratch/` (contains only `.gitkeep`) and confirmed `team/` did not exist yet.
2. Created `docs/evidence/i8-scratch/d-m3.txt` with content `i8-live-d-m3\n` (single line + trailing newline, no other bytes).
3. Created this handoff and `team/status/i8-d-m3.json`.
4. Ran the process check `test -f docs/evidence/i8-scratch/d-m3.txt` — exit code 0 (pass).

## What I did not do
- Did not create or modify `d-m1.txt`, `d-m2.txt`, `d-m4.txt`, `d-m5.txt`, or `d-m6.txt` — each is owned by a separate process.
- Did not touch any existing evidence file (the `.gitkeep` in `i8-scratch/` is untouched) or anything outside `docs/evidence/i8-scratch/`, `team/handoffs/i8-d-m3.md`, and `team/status/i8-d-m3.json`.
- Did not commit or push.

## Checks run and results
- `test -f docs/evidence/i8-scratch/d-m3.txt` → **PASS** (exit 0).

## Notes for the validator
- Scenario D is a half artifact: validate accepts it but `complete=false`, so only marker files exist; no completion artifact is expected from this card.
- The marker file must contain exactly `i8-live-d-m3` plus a trailing newline — do not strip or add content.
- The other five markers (`d-m1`, `d-m2`, `d-m4`–`d-m6`) are produced by their own processes; absence of any of them in this handoff is intentional, not a gap.
- This card owns only `docs/evidence/i8-scratch/d-m3.txt` among evidence files; ownership of the two `team/` files follows the work-order instruction to every process.
