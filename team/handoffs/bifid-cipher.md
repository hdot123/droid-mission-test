# Handoff: bifid-cipher (sub-issue #644)

## What was requested

Process card `bifid-cipher` under work order #632 第四十七轮 · 并发 C 单. Own `bifid.py` and `tests/test_bifid.py` only, standard library only, new files only (no edits to any existing file, no touching other deliverables — `partitions.py` / `rotate2d.py` and their tests are owned by other processes).

Spec (verbatim intent from the work order):

- 5×5 Polybius square pinned to alphabet `ABCDEFGHIKLMNOPQRSTUVWXYZ` (25 letters, no J; J folds into I), filled row-major: row r, column c (1–5) holds `alphabet[(r−1)*5 + (c−1)]` (0-based).
- `bifid_encrypt(text: str, period: int = 5) -> str`: preprocess to uppercase, J→I, keep only in-alphabet characters; split into groups of `period` chars (last group may be short); per group, concatenate all row coordinates as digits, then all column coordinates as digits, then map the merged digit string back per 2 digits as (row, column). Empty string → empty string.
- `bifid_decrypt(cipher: str, period: int = 5) -> str`: inverse — same grouping, per char its two coordinates written horizontally, first half of the digit string is the row column, second half the column column, pair up to restore. Returns the prepared plaintext (including folded I). Empty string → empty string.
- Validation: `period` positive int — non-int raises TypeError, ≤ 0 raises ValueError; non-str `text` raises TypeError.
- Every acceptance item had to have a corresponding test case.

## What I did

1. Created `bifid.py` (new file):
   - `ALPHABET`, `SQUARE_SIZE = 5`, lookup dicts `_ROW`, `_COL`, `_LOOKUP` derived from the pinned alphabet (no hardcoded square rows).
   - `_validate_text` / `_validate_period` (note: `period=True` is rejected as non-int because `bool` is explicitly excluded, consistent with the repo-wide "bool 拒" convention used by sibling cards).
   - `_prepare`: uppercase, J→I, filter to alphabet.
   - `bifid_encrypt`: per-period group → rows digits + cols digits → pairs → characters.
   - `bifid_decrypt`: per-period group → each char's `row col` digits concatenated → first half = row column, second half = col column → zip to restore.
   - Empty prepared string returns `""` in both directions.
2. Created `tests/test_bifid.py` with one test per acceptance item (15 test functions, 2 parametrized round-trip cases):
   - `HELLO`→`FNNVD`, `FNNVD`→`HELLO`, `A`→`A`, `""`→`""` (encrypt and decrypt), `J`→`I`, `JUMP`→`INUK`, `CRYPTOGRAPHY` period 6 →`DXSMUTICKGEO`, `HELLOWORLD` period 3 →`FNVNVROOFD`, round-trips for (`THEQUICKBROWNFOX`, 5) and (`ATTACKATDAWN`, 4), period 5 ≠ period 4 for `HELLOWORLD`, period 0 → ValueError, period `"5"` → TypeError, text `42` → TypeError.
3. Wrote `team/handoffs/bifid-cipher.md` and `team/status/bifid-cipher.json`.

## What I did not do

- Did not create or modify `partitions.py`, `rotate2d.py`, or their test files (other process cards own them).
- Did not modify any pre-existing repository file (only the six new deliverable/team files listed above; `git status` shows only additions).
- Did not commit or push.
- Did not import any module other than the standard library; `bifid.py` does not import `partitions` or `rotate2d`.

## Checks run and results

Environment note: `pytest` was not installed at first attempt (`No module named pytest`); installed it from `requirements-dev.txt` (`pytest>=7.4.0`), then:

- `python3 -m pytest tests/test_bifid.py -q` → **15 passed** in 0.02s
- `python3 -m pytest tests/ -q` → **44 passed** in 2.82s (includes all pre-existing tests plus mine; no existing test broke)

Both commands from the work order pass verbatim.

## What the validator must pay attention to

- Every acceptance item from the work order has a named test in `tests/test_bifid.py`; the two expected-value vectors (`FNNVD`, `INUK`, `DXSMUTICKGEO`, `FNVNVROOFD`) were verified by running the tests, not hand-computed.
- Decrypt returns the *prepared* plaintext (uppercase, J folded to I) — by design per spec, so a round-trip of lowercase input would not equal the raw input; the required round-trip cases in the acceptance list use already-prepared uppercase input and pass.
- `period` validation rejects `bool` explicitly (TypeError), matching the "bool 拒" convention in the sibling modules' specs even though this card's text says only "non-int raises TypeError".
- Scope discipline: `bifid.py` and `tests/test_bifid.py` are the only deliverables touched; `partitions.py`/`rotate2d.py` may still be pending from their own cards when this handoff is read — their absence is not a regression from this process.
