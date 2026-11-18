# Handoff: base36-codec (sub-issue #389)

## What was requested

Process card `base36-codec` under work order #380 (第四十二轮 A · crc32／base36／graycode).

Scope: own `base36.py` and `tests/test_base36.py` **only**. Do not touch crc32, graycode, or any existing file.

Requirements, verbatim from the card:

- `encode(n: int) -> str`: n is a non-negative int converted to a base36 string using
  digits `0-9` and lowercase letters `a-z`, no leading zeros, zero itself is `"0"`;
  raise `ValueError` for negative n.
- `decode(text: str) -> int`: the inverse operation, case-insensitive for letters;
  raise `ValueError` for empty string or characters outside the base36 alphabet.
- Acceptance criteria, each with a corresponding test case:
  `encode(0) == "0"`; `encode(35) == "z"`; `encode(36) == "10"`;
  `encode(123456789) == "21i3v9"`; `encode(987654321) == "gc0uy9"`;
  `decode("21i3v9") == 123456789`; `decode("GC0UY9") == 987654321`;
  `decode("z") == 35`; `encode(2**64 - 1) == "3w5e11264sgsf"`;
  `encode(-1)` raises `ValueError`; `decode("")` and `decode("12!")` raise `ValueError`;
  round-trip identity for `2**64 - 1`.
- Standard library only. No cross-imports between the three components.
- Only the six files across all three processes are new; no existing file may be modified.

## What I did

Created exactly two new files (no existing file was read-modified or written):

1. `base36.py`
   - `_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"` and a reverse lookup map.
   - `encode(n)`: rejects non-`int` with `TypeError` (defensive, not required by the card),
     raises `ValueError` for `n < 0`, returns `"0"` for zero, otherwise repeated
     `divmod(n, 36)` and reversed digit join → no leading zeros by construction.
   - `decode(text)`: rejects non-`str` with `TypeError` (defensive), raises `ValueError`
     for empty string, raises `ValueError` on the first character not in the alphabet
     (compared case-insensitively via `ch.lower()`), otherwise Horner accumulation
     `total = total * 36 + value`.

2. `tests/test_base36.py` — 10 test functions covering every acceptance bullet:
   `test_encode_zero`, `test_encode_boundaries` (35→"z", 36→"10", plus 9→"9", 10→"a"),
   `test_encode_samples` (123456789, 987654321, 2**64-1), `test_decode_samples`,
   `test_decode_case_insensitive` ("GC0UY9", "21I3V9", "Z"), `test_encode_negative_raises`,
   `test_decode_empty_raises`, `test_decode_invalid_character_raises` ("12!" plus three
   more out-of-alphabet strings), `test_roundtrip` (0, 1, 35, 36, 123456789, 987654321,
   2**32, 2**64-1), `test_roundtrip_large` (explicit 2**64-1 identity).

## What I did NOT do

- Did not create or modify `crc32.py`, `graycode.py`, `tests/test_crc32.py`,
  `tests/test_graycode.py`, or any other process's files.
- Did not modify any pre-existing repository file (`roman.py`, `legacy_stringkit.py`,
  `tests/test_roman.py`, `README.md`, `.github/**`, etc.). The pre-existing test suite
  still passes untouched.
- Did not commit or push (workflow owns that).
- Did not add third-party dependencies to the repo. Note: `pytest` was **not installed**
  in the environment (`No module named pytest`); I installed it with `pip3 install pytest`
  (pytest 9.2.0) so the mandated checks could run. This is an environment change only,
  no repository file was touched by it.

## Checks run and results

Both checks from the card, executed from the repository root, exit code 0:

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_base36.py -q` | `10 passed in 0.02s` (exit 0) |
| `python3 -m pytest tests/ -q` | `21 passed in 0.03s` (exit 0) |

The full-suite count of 21 = 11 pre-existing `tests/test_roman.py` cases + my 10 new
`tests/test_base36.py` cases, confirming no regression in the baseline.

## What the validator must pay attention to

1. **File ownership**: only `base36.py` and `tests/test_base36.py` were added by this
   process. `crc32.py` / `graycode.py` / their tests are other processes' deliverables;
   a full-suite run before they land will show only roman + base36.
2. **Two defensive `TypeError`s** (`encode` on non-int, `decode` on non-str) go slightly
   beyond the card, which only mandates `ValueError` for the listed invalid inputs. They
   cannot fire on any acceptance input (all of which are correct types), so no acceptance
   criterion is weakened. If strictness against extra behavior is desired, they are the
   first thing to drop.
3. **`decode` rejects at the first bad character** and short-circuits; it does not
   pre-validate the whole string. This satisfies "含 base36 字母表外字符抛 ValueError".
4. **Case-insensitivity** applies only to letters, via `str.lower()`; digits `0-9` are
   unaffected. `"GC0UY9"` → 987654321 and `"21I3V9"` → 123456789 are both asserted.
5. **Leading zeros**: `encode` never emits them (divmod loop stops at n == 0), so
   `encode(36) == "10"` holds. `decode("007")` would be 7 — the card does not specify
   behavior for leading zeros on decode, and no test asserts it either way.
6. **Environment**: if the validator runs in a fresh container without pytest, it must
   `pip3 install pytest` first; the repo itself carries no dependency manifest.
