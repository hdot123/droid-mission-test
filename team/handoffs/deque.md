# Handoff: deque (sub-issue #857, work order #849 并发 B 单)

## What was requested

Implement process card `deque`: a `Deque` double-ended queue as two new files only:

- `deque.py` — class `Deque` constructible from an iterable (`Deque()` empty, `Deque(iterable)` enqueues in iteration order). Methods: `append`, `appendleft`, `pop`, `popleft`, `peek`, `peekleft`, `clear`, `is_empty() -> bool`, `to_list() -> list` (left-to-right snapshot), `__len__`. Empty-queue `pop`/`popleft`/`peek`/`peekleft` must raise `IndexError`. Standard library only; must not import `monthgrid` or `sdbmhash`.
- `tests/test_deque.py` — one test case per acceptance point (11 acceptance points from the card).
- No existing files modified; nothing else created besides the two required team files.

## What I did

- `deque.py`: implemented `Deque` backed by `collections.deque` (true O(1) both ends), all ten specified members plus `__iter__`/`__repr__` conveniences, `IndexError` guards on all four empty-queue operations. Only standard-library imports (`collections.deque`, `typing`).
- `tests/test_deque.py`: 13 tests covering every acceptance point verbatim:
  - empty `is_empty() is True`; `len(Deque()) == 0`
  - `append(1)/append(2)/appendleft(0)` → `to_list() == [0, 1, 2]`, `len == 3`
  - `peek() == 2`, `peekleft() == 0` (and non-removal asserted)
  - `pop() == 2`, `popleft() == 0` → `to_list() == [1]`
  - `Deque([5, 6, 7]).to_list() == [5, 6, 7]`; `Deque("ab").to_list() == ["a", "b"]`
  - `clear()` → empty + `to_list() == []`
  - model consistency: 600 seeded random mixed ops (`append`/`insert(0)`/`pop`/`pop(0)`/`peek`/`peekleft`/`clear`/`len` against a Python-list model), `to_list()` compared to the model after **every** step
  - all four empty-queue operations raise `IndexError` (one test each)

## What I did NOT do

- Did not modify, move, or delete any pre-existing file.
- Did not implement or touch `monthgrid.py`, `sdbmhash.py`, or their tests (owned by sibling workers).
- Did not create any other deliverable, did not commit or push.

## Checks ran and results

1. `python3 -m pytest tests/test_deque.py -q` → **13 passed in 0.02s**.
2. `python3 -m pytest tests/ -q` → **353 passed, 2 skipped, 1 failed** in 18s.

The single failure is `tests/test_check_summary_focused_counts.py::test_summary_block_on_r54_pack_produces_real_focused_counts`, a pre-existing environment failure unrelated to this card: it reads a hard-coded external fixture `/tmp/r54-audit/a/evidence/packs/damm/checks-output.txt` which does not exist on this machine (`/tmp/r54-audit` absent entirely). It fails identically on a clean tree and imports nothing from `deque.py`. Everything else in the suite passes.

No `verdict.json` / `verdict.md` byproducts were produced by my runs; nothing to clean up.

## What the validator must pay attention to

- `deque.py` shadows nothing in the stdlib for the test process (Python's stdlib `deque` module is not importable as a top-level module in CPython; `collections.deque` is used inside the implementation regardless).
- The full-suite failure above is environmental (missing `/tmp/r54-audit` fixtures), not a regression from this card. Full suite is otherwise green: 353 passed + 13 from this card included.
- `tests/test_deque.py` prepends the repo root to `sys.path` so `from deque import Deque` resolves regardless of pytest rootdir configuration, mirroring the existing `test_roman.py` pattern.
