# Handoff: paritybit (sub-issue #855)

## What was requested

Process card #855 under work order #848 (round 55 concurrent card A): create two new files only —
`paritybit.py` and `tests/test_paritybit.py` — implementing three parity-bit helpers
(`append_parity`, `check_parity`, `strip_parity`) with the full input contract
(ValueError for empty string / non-0-1 characters / invalid mode / length < 2 for
`strip_parity`; TypeError for non-str input), plus a test case for every acceptance
item in the card. Standard library only; no imports from `derange` or `bearing`;
no modification of any existing file.

## What I did

- Created `paritybit.py`:
  - `append_parity(bits: str, mode: str = "even") -> str` — appends one parity bit
    so the total count of 1s is even (`"even"`) or odd (`"odd"`).
  - `check_parity(bits: str, mode: str = "even") -> bool` — True iff the total count
    of 1s satisfies the mode.
  - `strip_parity(bits: str) -> str` — drops the last bit; raises ValueError when
    length < 2 (covers the empty string too).
  - Shared private validators enforce: non-str → TypeError; empty string or any
    character outside `01` → ValueError; mode not in `{"even", "odd"}` → ValueError
    (non-str mode → TypeError). No third-party imports.
- Created `tests/test_paritybit.py` with 19 tests covering every acceptance item:
  all nine `append_parity` examples (even and odd), all three `check_parity`
  examples, round-trips (example strings plus an exhaustive loop over all bit
  strings of length 1–5 for both modes), and every error case in the contract for
  all three functions (`append_parity("")`, `"102"`, `"10"/"x"`, `strip_parity("1")`,
  `strip_parity("")`, `check_parity("")`, `check_parity("0a1")`, `check_parity("10", "even-o")`,
  `append_parity(10)`, `check_parity(10)`, `strip_parity(10)`, `append_parity("10", 1)`).

## What I did NOT do

- Did not modify, move, or delete any pre-existing file (only the two deliverables
  and the two team files were created).
- Did not create `derange.py` or `bearing.py` / their tests (owned by the sibling cards).
- Did not touch `team/**` files owned by other processes, nor `.github/**`.
- Did not import from `derange` or `bearing` (standard library only: `pytest` in tests,
  nothing but builtins in `paritybit.py`).
- Did not commit or push.

## Checks run and results

1. `python3 -m pytest tests/test_paritybit.py -q` → **19 passed in 0.03s** (exit 0).
2. `python3 -m pytest tests/ -q` → **1 failed, 359 passed, 2 skipped** (exit 1).
   The single failure is `tests/test_check_summary_focused_counts.py::test_summary_block_on_r54_pack_produces_real_focused_counts`,
   which fails with `FileNotFoundError: /tmp/r54-audit/a/evidence/packs/damm/checks-output.txt`.
   That test reads external audit-pack fixtures from `/tmp/r54-audit/...` that do not
   exist in this environment. It is unrelated to `paritybit` (it never imports or
   reads my files) and is pre-existing/environment-dependent, not caused by this card.

## What the validator must pay attention to

- The full-suite run is red only because of the pre-existing `/tmp/r54-audit` fixture
  dependency above; every paritybit test passes, and the other 359 tests pass.
  Confirm whether that test is expected to be green in a properly provisioned
  environment (with `/tmp/r54-audit` seeded) before treating the full-suite exit
  code as a regression from this card.
- `paritybit.py` validates the mode argument after the bits argument in
  `append_parity`/`check_parity` (empty/invalid bits raise before an invalid mode
  does); the card only requires that each bad input raises, not a specific order.
- `strip_parity` accepts only length >= 2; `strip_parity("1")` and `strip_parity("")`
  both raise ValueError, as specified.
