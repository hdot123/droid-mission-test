# Handoff: trifid-cipher (sub-issue #647)

## What was requested

Process card for work order #630 (第四十七轮 · 并发 A 单), scope: the Trifid cipher module only.

- Create `trifid.py` — Trifid cipher over a 3×3×3 cube with period split:
  - Alphabet pinned to `ABCDEFGHIJKLMNOPQRSTUVWXYZ+` (27 chars); index i (0-based) maps to (layer, row, col) = (i//9 + 1, (i%9)//3 + 1, i%3 + 1), coordinates 1–3.
  - `trifid_encrypt(text: str, period: int = 5) -> str`: uppercase + strip non-alphabet; group by `period` (last group may be short); per group write layer row, then row row, then column row into one digit string; map back in 3-digit triples. Empty in → empty out.
  - `trifid_decrypt(cipher: str, period: int = 5) -> str`: inverse (coordinates written horizontally, split into three rows, read column-wise). Returns preprocessed plaintext. Empty in → empty out.
  - Validation: period non-int → TypeError, period ≤ 0 → ValueError; text/cipher non-str → TypeError (same rules for decrypt).
- Create `tests/test_trifid.py` covering every acceptance criterion verbatim (22 test cases including parametrized round-trips).

## What I did

- Created `trifid.py` (standard library only, no cross-module imports).
- Created `tests/test_trifid.py` with a test case for each acceptance point: all fixed vectors (`"A"→"A"`, `"AZ"→"GT"`, `"HELLO"→"BOJN+"`, `"THEQUICKBROWNFOX"→"SPXEOBFA+OQENQRX"`, `"ATTACKATDAWN"` @3, `"XYZ+ABC"` @4), preprocessing tests (`"hello"`, `"HE LLO!"`), three parametrized round-trips (incl. period=1), period-affects-result inequality, all ValueError/TypeError cases, plus decrypt-side validation tests (additional, still within my files).
- Note: the spec requires decrypt to apply the same period rules as encrypt, so `trifid_decrypt` validates period identically; this was explicitly allowed by the card ("apply the same period rules to decrypt").

## What I did not do

- Did not touch `mobius.py`, `gasmark.py` (owned by other processes), or any pre-existing file.
- No cross-module imports; standard library only (plus `pytest` in tests).
- Did not commit or push.

## Checks run and results

1. `python3 -m pytest tests/test_trifid.py -q` → **22 passed** in 0.03s.
2. `python3 -m pytest tests/ -q` → **51 passed** in 2.87s (full suite, includes other teams' modules; all green).

(One environment note: pytest was not preinstalled; I installed it with `python3 -m pip install pytest` per `requirements-dev.txt`. No repo files changed by this.)

## What the validator must pay attention to

- Alphabet contains `+` at index 26, so ciphertext may contain `+` — expected (e.g. `"BOJN+"`).
- Non-int period is rejected as TypeError before ≤0 ValueError check; bool period would be rejected as TypeError (isinstance guard rejects `bool` explicitly) — spec says "非 int 抛 TypeError"; bools are not listed in acceptance tests but are handled strictly.
- `trifid_decrypt` returns the *preprocessed* plaintext (uppercase, non-alphabet stripped), per spec; round-trip tests use already-clean text so this is transparent.
- Files owned by this process: `trifid.py`, `tests/test_trifid.py`, plus this handoff and `team/status/trifid-cipher.json`.
