# Handoff: mod97-module (sub-issue #288)

## What was requested
Process card `mod97-module` under work order #278 (第三十五轮 · 并发加压第四组 B 单): implement the IBAN-style mod-97 component as two new files only:

- `mod97.py` with
  - `remainder(digits: str) -> int`: non-empty pure-ASCII-digit string treated as a big integer, return its mod-97 remainder, computed in chunks or an equivalent method (must not convert an arbitrarily long string to `int` in one shot). Raise `ValueError` on non-digit characters or empty string.
  - `is_valid_iban_numeric(digits: str) -> bool`: `remainder(digits) == 1`; invalid input returns `False` without raising.
- `tests/test_mod97.py` covering all seven mandatory acceptance items:
  1. `remainder("97") == 0`
  2. `remainder("98") == 1`
  3. `remainder("100") == 3`
  4. `remainder("12345678901234567890") == 3`
  5. `is_valid_iban_numeric("98") is True`
  6. `is_valid_iban_numeric("97") is False`
  7. `remainder("")` raises `ValueError`

Constraints: only new files (never modify any existing file), standard library only, no imports from `luhn` or `isbn13`.

## What I did
- Created `mod97.py`:
  - `remainder` validates the input (must be a non-empty `str` of ASCII digits, `0`-`9`; anything else raises `ValueError`, including `None`/ints, which are rejected rather than silently coerced), then folds the string in 9-digit chunks: `rem = (rem * 10**len(chunk) + int(chunk)) % 97`. Each intermediate stays a small machine-word int, so arbitrarily long inputs are supported without one-shot `int()` conversion. Chunk size 9 keeps `rem * 10**9 + chunk` within ~60 bits, far from Python's 4300-digit int-str conversion limit.
  - `is_valid_iban_numeric` wraps `remainder` in `try/except ValueError` and returns `remainder(digits) == 1`; invalid input returns `False` and never raises.
  - Both functions are exported via `__all__`. No imports from `luhn`/`isbn13`/anything else (pure stdlib, in fact zero imports).
- Created `tests/test_mod97.py` with 7 test functions covering:
  - the three short acceptance values (97→0, 98→1, 100→3),
  - the 20-digit acceptance value `12345678901234567890` → 3 (this spans 3 chunks, so the chunked path is what produces it),
  - an independent oracle cross-check: `remainder("1234567890" * 50)` (500 digits) equals `int(digits) % 97`,
  - `is_valid_iban_numeric("98") is True` / `("97") is False`,
  - `remainder("")` raises `ValueError`,
  - non-digit/non-str inputs for `remainder` (`"98a"`, `"98 7"`, `"98.0"`, `"98\n"`, full-width digits `"１２"`, int `12345`) all raise `ValueError`,
  - invalid inputs for `is_valid_iban_numeric` (`""`, `"98a"`, `"97-0"`, `None`, `98`) all return `False` without raising.

All seven mandatory acceptance items have a dedicated assertion. `is_valid` checks use `is True` / `is False` so the return type is pinned to a real `bool`.

## What I did not do
- Did not touch `luhn.py`, `isbn13.py`, or any other existing file (only the two files named in the card were created, plus the two required team files under `team/`).
- Did not implement or test the Luhn or ISBN-13 components — those are separate process cards.
- Did not commit or push anything.
- Did not add `conftest.py`, `pytest.ini`, or any config; the repo relies on rootdir-based sys.path insertion for `import mod97` / `import roman`, which works as-is.

## Checks I ran
Environment note: `pytest` was not installed in this container (`python3 -m pytest` → "No module named pytest"), so I ran `pip3 install --user pytest` (installed pytest 9.2.0 + pluggy/iniconfig) before running the required checks. This is a tooling install, not a repo change.

1. `python3 -m pytest tests/test_mod97.py -q` → **7 passed in 0.01s**
2. `python3 -m pytest tests/ -q` → **18 passed in 0.02s** (full suite: 7 mine + 11 pre-existing roman/stringkit tests)

Both checks from the process card pass.

## What the validator must pay attention to
- The seven mandatory acceptance items each map to a named test; the chunked-algorithm requirement is exercised by the 20-digit case (3 chunks) and reinforced by the 500-digit oracle test.
- `remainder` intentionally rejects non-`str` types (`None`, `int`) with `ValueError` rather than coercing; `is_valid_iban_numeric` therefore returns `False` for those. This matches "非法输入返回 False 不抛异常" for the boolean wrapper and keeps `remainder` strict.
- Full-width/non-ASCII digits are rejected (only ASCII `0`-`9` count), consistent with "纯数字字符串".
- `is_valid_iban_numeric` returns a genuine `bool` (`is True`/`is False` in tests would catch an accidental `numpy`-style truthy int).
- No shared files were touched; `mod97.py` and `tests/test_mod97.py` are the only code files I created. `luhn.py`, `isbn13.py`, and their tests belong to other cards and were left alone (they may not exist yet in this working tree).
- Files created by this card: `mod97.py`, `tests/test_mod97.py`, `team/handoffs/mod97-module.md`, `team/status/mod97-module.json`.
