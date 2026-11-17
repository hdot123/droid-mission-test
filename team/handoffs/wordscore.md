# Handoff: wordscore (sub-issue #85)

## What was requested

Process card #85 under work order #83 (领班制 v2.6.3, 第十七轮). Owns only
`wordscore.py` and `tests/test_wordscore.py`.

Implement `score(word)`: iterate over the characters, take each letter's
alphabetical position (a=1 ... z=26, case-insensitive), ignore non-letter
characters, return the sum; empty string or no letters returns 0. Standard
library only, no CLI, no package directory, no imports from other modules.

The work order's example set is contradictory and is a hard requirement:
deliverable examples say `score("abc") == 6`, `score("z") == 26`,
`score("a-b") == 3`; acceptance criteria say `score("bad") == 7` and
`score("abc") == 7`. Per the card: preserve every example verbatim, never
resolve, drop, or renumber any value, write all of them into the checks
verbatim, implement the spec rules exactly, and let the checks run against
the real evidence.

## What I did

- Created `wordscore.py` with a single `score(word)` function implementing
  the spec rules exactly (sum of case-insensitive letter positions,
  non-letters ignored, 0 for empty/no-letter input).
- Created `tests/test_wordscore.py` covering this module only (imports only
  `wordscore`). It contains:
  - spec-rule tests (empty string, no letters, a..z positions, case
    insensitivity, non-letters ignored), and
  - five verbatim example assertions, one per work-order example:
    `score("abc") == 6`, `score("z") == 26`, `score("a-b") == 3`,
    `score("bad") == 7`, `score("abc") == 7`.
- Installed `pytest` (9.2.0) via `python -m pip install pytest` because the
  environment's `python` had no pytest module (`No module named pytest`).
- Fixed one auxiliary (non-verbatim) test I wrote: `score("hi, there!")` was
  mistakenly asserted as 44; the correct sum is 73. This was my own
  arithmetic error in a derived test, not a work-order example; the fix is
  recorded here for full transparency.

## What I did NOT do

- Did not touch `caesar.py`, `hexcolor.py`, or any other process's files.
- Did not resolve, change, drop, or renumber any contradictory example value.
- Did not weaken or delete the failing verbatim test to make checks pass.
- Did not commit or push.

## Checks run (from repository root) and results

1. `python -m pytest -q tests/test_wordscore.py`
   → FAILED, exit 1: `1 failed, 9 passed in 0.02s`.
   The single failure (verbatim):
   ```
   FAILED tests/test_wordscore.py::test_verbatim_acceptance_example_abc_is_7
   >       assert score("abc") == 7
   E       AssertionError: assert 6 == 7
   E        +  where 6 = score('abc')
   tests/test_wordscore.py:70: AssertionError
   ```
2. `python -c "from wordscore import score; assert score('abc') == 6"`
   → PASSED, exit 0.
3. `python -c "from wordscore import score; assert score('z') == 26"`
   → PASSED, exit 0.
4. `python -c "from wordscore import score; assert score('a-b') == 3"`
   → PASSED, exit 0.
5. `python -c "from wordscore import score; assert score('bad') == 7"`
   → PASSED, exit 0.
6. `python -c "from wordscore import score; assert score('abc') == 7"`
   → FAILED, exit 1 (verbatim):
   ```
   Traceback (most recent call last):
     File "<string>", line 1, in <module>
       from wordscore import score; assert score('abc') == 7
                                           ^^^^^^^^^^^^^^^^^
   AssertionError
   ```

## For the validator

- The red result is EXPECTED and EVIDENCE-PRESERVED: the work order buries a
  deterministic contradiction (`score("abc")` cannot be both 6 and 7). The
  spec rules are implemented exactly as written; both verbatim assertions are
  kept in the test file and both appear in the card's checks as given. The
  evidence (pytest failure + failing check #6) reaches downstream intact for
  the replan loop to judge as a "plan error".
- Note the spec-rule tests and the four non-conflicting verbatim examples all
  pass (9 passed). Only the contradictory pair member `score("abc") == 7`
  fails, because the spec-rule-consistent value of `score("abc")` is 6.
- pytest was not present initially and was installed (pytest 9.2.0); this is
  an environment observation, not a code change.
