# Handoff: lcs-module (sub-issue #263)

## What was requested
Process card `lcs-module` for work order #246 (round 33, foreman v2.6.5):
create `lcs.py` in the repo root plus `tests/test_lcs.py`, owning exactly those two files.

Spec:
- `lcs_length(a, b)` returns the LCS length of two strings.
- `lcs_string(a, b)` returns one LCS string.
- Pinned backtracking rule: build the length table bottom-up, backtrack from the
  ends of both strings; on equal characters take the character; otherwise move
  toward the side with the larger length; on a tie, move to the side that skips
  `a`'s current character (prefer keeping `b`'s characters).
- Required examples: `lcs_length("ABCBDAB", "BDCABA") == 4`,
  `lcs_string("ABCBDAB", "BDCABA") == "BCBA"`,
  `lcs_string("AGGTAB", "GXTXAYB") == "GTAB"`,
  `lcs_length("abc", "def") == 0`, `lcs_string("", "abc") == ""`,
  `lcs_string("abcde", "ace") == "ace"`.
- Standard library only; no import of `slugtext`/`packbits`; no package dir, no CLI.
- Test file must test only LCS behavior and cover all examples plus empty-string
  and no-common-subsequence cases, and must pin the observable tie-break.

## What I did
- Created `lcs.py` with `lcs_length` and `lcs_string`. Both build the classic
  bottom-up DP table; `lcs_string` backtracks with the pinned tie-break
  (`dp[i-1][j] >= dp[i][j-1]` moves up, i.e. skips `a`'s current character on
  ties, which prefers `b`'s characters).
- Created `tests/test_lcs.py` with 13 tests covering every spec example, both
  empty-string directions, both empty, no-common-subsequence (length and
  string), identical strings, the tie-break (e.g. `lcs_string("ab", "ba") ==
  "a"`, where the opposite tie-break would give `"b"`), and a
  length-matches-string consistency check over all example pairs.

## What I did not do
- Did not touch `slugtext.py`, `packbits.py`, any other test file, `team/`
  files owned by other processes, or any `team/` / `.github/` path other than
  this card's two handoff/status files.
- Did not create package directories, CLI entry points, or cross-module imports.
- Did not commit or push (left to the workflow).

## Checks run and results
- `python -m pytest -q tests/test_lcs.py` → **13 passed in 0.02s** (exit 0).
  This is the card's check command, run verbatim as written.

Note on environment: `pytest` was not preinstalled (`No module named pytest`),
so `python3 -m pip install pytest` (installs pytest 9.2.0) was run first so the
verbatim check command could execute. No repository files were changed by that.

## What the validator must pay attention to
- The tie-break is observable and pinned: on equal DP lengths the walk skips
  `a`'s current character. `test_tie_break_prefers_skipping_a` pins this with
  `lcs_string("ab", "ba") == "a"` (opposite rule would return `"b"`) and with
  the spec's `"BCBA"` result.
- The spec example `lcs_string("ABCBDAB", "BDCABA") == "BCBA"` passes; note
  some textbook traces produce `BCBA` as well, so that string is not itself a
  tie discriminator — the `"ab"`/`"ba"` case is.
- Global acceptance (all three deliverables merged): `python -m pytest -q`
  must be green across the whole repo; that is a post-merge check, not run
  for this card alone.
