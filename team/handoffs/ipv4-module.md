# Handoff: ipv4-module (sub-issue #209)

## What was requested
Process card `ipv4-module` under work order #204 (round 29, unit C). Scope: implement only `ipv4.py` and `tests/test_ipv4.py` in the repo root.

- `is_valid_ipv4(s)` → `True`/`False`, never raises: exactly four dot-separated decimal segments; each segment non-empty, ASCII digits only, value 0–255, no leading zeros except the single digit `"0"`.
- `parse_ipv4(s)` → 4-int tuple when valid, raises `ValueError` when invalid.
- Spec examples must hold: `"192.168.0.1"` → True, `"0.0.0.0"` → True, `"01.2.3.4"` → False, `"256.1.1.1"` → False, `"1.2.3"` → False, `parse_ipv4("192.168.0.1")` → `(192, 168, 0, 1)`.
- Constraints: standard library only; must not import `hexcolor` or `morse`; no package directory; no CLI; tests cover only this module, including all spec examples plus boundaries (leading zeros, empty segments, 255/256 bounds, non-digit characters, too many digits, `parse_ipv4` raising `ValueError` on invalid input).

## What I did
- Created `ipv4.py` with `is_valid_ipv4(s)` and `parse_ipv4(s)`. Segment validation uses an explicit ASCII-range check (`"0" <= ch <= "9"`) so Unicode digit characters (e.g. Arabic-Indic digits that `str.isdigit()` accepts) are rejected as non-digits. Leading-zero rule: segment length > 1 starting with `"0"` → invalid. Range check: `int(part) > 255` → invalid. `parse_ipv4` delegates to `is_valid_ipv4` and raises `ValueError("invalid IPv4 address: ...")` on failure.
- Created `tests/test_ipv4.py` with 22 tests covering: all six spec examples, leading zeros (several positions), empty/missing segments, out-of-range 255/256 and 999, non-digit and whitespace/suffix characters, wrong segment counts (3, 5, trailing dot), too many digits (e.g. `192.168.0001.1`, `0000.0.0.0`, `1.1.1.1000`), non-string input returning `False` without raising, valid parses (`0.0.0.0`, `255.255.255.255`, `10.0.0.1`), and 11 parametrized invalid inputs asserting `ValueError`.
- Wrote `team/handoffs/ipv4-module.md` and `team/status/ipv4-module.json`.

## What I did not do
- Did not create or modify `hexcolor.py`, `morse.py`, or their tests (other process cards own those).
- Did not modify any pre-existing repository files (`legacy_stringkit.py`, `tests/test_legacy_stringkit.py`, README, git metadata).
- Did not create a package directory, CLI, or any file outside the four listed above.
- Did not commit or push.

## Checks run and results
Commands executed verbatim from the process card, from the repo root:

1. `python -m pytest -q tests/test_ipv4.py` → **exit 0, 22 passed in 0.02s**
2. `python -m pytest -q` → **exit 0, 26 passed in 0.02s** (22 mine + 4 pre-existing `tests/test_legacy_stringkit.py`)

Environment note: pytest was not preinstalled; I installed it with `python3 -m pip install pytest` (pytest 9.2.0) so the mandated checks could run. No other environment changes.

## What the validator must pay attention to
- Leading-zero rule is intentionally strict: `"0.0.0.0"` is valid, `"00.0.0.0"` and `"01.2.3.4"` are invalid — this matches the card's examples.
- Non-string input (`None`, `int`) returns `False` from `is_valid_ipv4` rather than raising; `parse_ipv4(None)` therefore raises `ValueError` (via the same path), which is consistent with "invalid → ValueError".
- The full-suite green (26 passed) includes the pre-existing legacy tests; the round-29 baseline note in the work order refers to备料 across all four concurrent units, not to this card alone.
- Full suite also depends on other workers' `hexcolor`/`morse` cards landing; at the time I ran it, only `ipv4` + legacy existed and everything passed.
