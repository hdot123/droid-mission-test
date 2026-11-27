# Handoff: zarray (sub-issue #965, work order #953 item 1)

## What was requested

Implement the Z-array component of round-59 C-unit (#953), owning exactly two new files:

- `zarray.py` — `z_array(s: str) -> list[int]`: Z[0] = 0, Z[i] (i >= 1) = length of longest
  common prefix of `s` and suffix `s[i:]`; empty string returns `[]`; non-str raises
  `TypeError` (no ValueError surface).
- `tests/test_zarray.py` — a test for every acceptance point:
  - `z_array("") == []`
  - `z_array("aaaaa") == [0, 4, 3, 2, 1]`
  - `z_array("abcab") == [0, 0, 0, 2, 0]`
  - `z_array("aabcaabxaaaz") == [0, 1, 0, 0, 3, 1, 0, 0, 2, 2, 1, 0]`
  - property: random strings over a small alphabet (length 0–30) agree element-by-element
    with a naive pairwise-comparison reference implementation
  - `z_array(b"ab")` and `z_array(None)` raise `TypeError`

Constraints: new files only, no modification of any existing file, standard library only,
no imports of sibling modules (millerrabin / abacheck).

## What I did

- `zarray.py`: linear Z-box algorithm (O(n) time), with an upfront `isinstance(s, str)`
  check raising `TypeError`. Docstring notes the distinction from the KMP prefix function π.
- `tests/test_zarray.py`: the four fixed cases, a naive reference implementation defined
  in the test file itself (no import of zarray internals), a property test with
  `random.Random(20261127)` fixed seed over alphabet "abc" with lengths 0–30 (300 draws),
  and TypeError cases for `b"ab"` and `None`. Standard library + pytest only.

## What I did not do

- Did not touch `millerrabin.py` / `abacheck.py` (owned by other workers).
- Did not modify any pre-existing file (verified via `git status`: only `zarray.py`,
  `tests/test_zarray.py` are new; `worker-prompt.txt` / `worker-stream.jsonl` are
  pre-existing untracked pipeline files I did not touch).
- Did not commit or push, per instructions.
- No verdict.json / verdict.md by-products were produced by these checks (checked and none
  present).

## Checks run and results

1. `python3 -m pytest tests/test_zarray.py -q` → `7 passed in 0.02s`
2. `python3 -m pytest tests/ -q` → `349 passed, 2 skipped in 21.31s` (exit 0; the 2 skips
   are pre-existing repo-wide skips, unrelated to this card)

## Notes for the validator

- Verification only checks values; implementation is the linear Z-box variant but the
  acceptance property test independently cross-checks against a naive O(n^2) pairwise
  reference, so any value disagreement would fail.
- The property test uses a fixed seed (`20261127`) — deterministic across runs.
- Test file imports only `zarray` (its own module) plus stdlib `random`/`pytest`; no
  cross-imports to sibling cards.
