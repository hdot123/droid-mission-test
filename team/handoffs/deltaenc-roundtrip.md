# Handoff — deltaenc-roundtrip (sub-issue #469)

## What was requested

Process card `deltaenc-roundtrip` for work order #457 (第四十五轮 · 并发 C 单): implement `deltaenc.py`
with two functions, plus `tests/test_deltaenc.py` covering every acceptance item verbatim.

Scope owned by this card:
- `deltaenc.py`
- `tests/test_deltaenc.py`
- plus this handoff and `team/status/deltaenc-roundtrip.json`

## What I did

Created `deltaenc.py` (standard library only, no imports of other deliverable modules):

- `_check(nums)` — private validator: argument must be a `list`; every element must be `int` with
  `bool` explicitly rejected (`isinstance(item, bool)` checked first, since `bool` subclasses `int`).
  Violations raise `TypeError`.
- `delta_encode(nums)` — validates, returns `[]` for empty input, keeps the first element as-is, then
  appends `cur - prev` for each subsequent element.
- `delta_decode(deltas)` — validates, returns `[]` for empty input, accumulates a running total and
  appends each step, restoring the original sequence.

Created `tests/test_deltaenc.py` with one test per acceptance item (21 tests):
basic encode/decode, empty lists, single element, zero/negative deltas, negative values, all-zero
input, large values, four parametrized round-trips (`[3, 1, 4, 1, 5, 9, 2, 6]`, `[0]`,
`[-1, -2, -3]`, `[100, 200, 150, 150, 151]`), and the five `TypeError` cases
(`delta_encode((1, 2))`, `delta_encode([1, 2.5])`, `delta_encode([1, True])`, `delta_decode("abc")`,
`delta_decode([1, 0.5])`).

## What I did NOT do

- Did not touch `easter.py`, `isogram.py`, or any other deliverable (other cards own those).
- Did not modify any pre-existing file: `roman.py`, `legacy_stringkit.py`, `tests/test_roman.py`,
  `tests/test_legacy_stringkit.py`, `README.md`, or anything under `team/` owned by other cards.
- Did not add any non-standard-library dependency to the deliverable (pytest was installed into the
  runner's user site only so the required checks could execute; it is not imported by `deltaenc.py`).
- Did not commit or push.

## Checks I ran

1. `python3 -m pytest tests/test_deltaenc.py -q` → **21 passed**, exit 0.
2. `python3 -m pytest tests/ -q` → **32 passed**, exit 0.

Note: the environment initially had no pytest (`No module named pytest`); I installed it with
`python3 -m pip install --user pytest` (got 9.2.0) before running the checks above. Both commands
now pass as specified.

## Notes for the validator

- Type rules are enforced before any computation, so non-list arguments raise `TypeError` even for
  empty-looking inputs such as `"abc"` or a tuple.
- `bool` elements are rejected on both encode and decode (`True`/`False` are `int` subclasses in
  Python, so an explicit `isinstance(item, bool)` guard is required); the acceptance case
  `delta_encode([1, True])` exercises this.
- Decode of an empty list returns `[]` (not `[0]`), matching the spec.
- The implementation is self-contained; it does not import `easter`, `isogram`, or any other module.
