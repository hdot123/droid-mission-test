# Handoff: ipv6fmt (sub-issue #937)

## What was requested

Process card `ipv6fmt` under work order #928 (round 58, concurrent C card): implement a
standalone IPv6 text formatting module — `expand_ipv6(addr) -> str` and
`compress_ipv6(addr) -> str` with strict RFC 5952 compression semantics — as **new files
only**: `ipv6fmt.py` and `tests/test_ipv6fmt.py`. Standard library only; no edits to any
existing file; no imports of the existing IPv4-family modules (`ipaddr`, `ipv4`,
`ipv4kit`); no `team/**` or `.github/**` files owned by other processes touched.

Key strictness requirements (verbatim from the card):
- Expand to 8 groups of 4 lowercase hex digits joined by `:`.
- Compress per RFC 5952: no leading zeros, lowercase; **only** the longest zero run of
  length ≥ 2 becomes `::`; a single zero group is **not** compressed; equal-length zero
  runs resolve to the **leftmost**.
- Invalid address → `ValueError` (group > 4 hex digits, multiple `::`, wrong group count,
  v4-embedded form like `::ffff:1.2.3.4`, `%zone` form like `fe80::1%eth0` are ALL
  invalid); non-`str` → `TypeError`. Both functions accept the same legal input forms
  (expanded and compressed forms alike).
- Property: on random 128-bit addresses, expand == stdlib `ipaddress.exploded`,
  compress == `ipaddress.compressed`, compress idempotent,
  `expand(compress-form) == expand(expanded-form)`.

## What I did

1. Created `ipv6fmt.py`:
   - `_parse(addr)` — strict validator: rejects non-`str` (`TypeError`), rejects `.` in
     the address (kills v4-embedded forms), rejects `%` (kills `%zone`), requires at most
     one `::`, requires each group to match `[0-9a-fA-F]{1,4}`, handles `::` expansion
     (must stand for ≥ 1 group, so `1:2:3:4:5:6:7:8::` is invalid), and requires exactly
     8 groups when no `::` is present.
   - `expand_ipv6` — formats each of the 8 groups as `%04x` (lowercase, zero-padded).
   - `compress_ipv6` — converts groups to `%x`, finds the longest zero run of length ≥ 2
     (leftmost on ties), replaces it with `::`; otherwise joins as-is.
   - Module uses only `re` from the stdlib; no cross-imports.
2. Created `tests/test_ipv6fmt.py` covering:
   - every expand/compress acceptance example (including single-zero-group and
     leftmost-tie cases);
   - expand/compress agreement across compressed and expanded input forms;
   - idempotence of compress;
   - all 13 `ValueError` inputs against **both** functions;
   - `expand_ipv6(123)` and `compress_ipv6(None)` `TypeError`;
   - 200 random 128-bit addresses (half forced to contain zero runs) compared against
     stdlib `ipaddress` for exploded/compressed/idempotence/round-trip, seeded with a
     fixed RNG;
   - an AST-based guard asserting the module imports nothing beyond `re` (and never
     `ipaddr`/`ipv4`/`ipv4kit`/`inversions`/`egyptian`).

## What I did NOT do

- Did not modify, move, or delete any pre-existing file (only added the two owned files
  plus the two required team files below).
- Did not touch `inversions.py` / `egyptian.py` (other workers' cards).
- Did not create or edit `team/**` files other than my own two, nor anything under
  `.github/**`.
- Did not commit or push.
- Did not relax any acceptance rule to make tests pass (e.g. single-zero-group
  compression and v4-embedded/%zone acceptance are rejected, per the card).

## Checks run

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_ipv6fmt.py -q` | **54 passed** in 0.05s |
| `python3 -m pytest tests/ -q` | **396 passed, 2 skipped** in 19.40s (2 skips are pre-existing, unrelated to this card) |

No `verdict.json` / `verdict.md` by-products were produced by these runs (checked; none
existed, nothing to delete).

## Notes for the validator

- The two acceptance-strict points most likely to be probed:
  - `compress_ipv6("2001:0db8:0000:0001:0001:0001:0001:0001")` →
    `2001:db8:0:1:1:1:1:1` (single zero group **not** compressed);
  - `compress_ipv6("1:0:0:2:0:0:0:3")` → `1:0:0:2::3` (equal-length runs: leftmost wins).
- Invalid inputs are rejected by `_parse` before any formatting; the same parser backs
  both functions, so their legal-input forms are identical by construction.
- `expand_ipv6`/`compress_ipv6` accept uppercase input and always emit lowercase.
- Files delivered: `ipv6fmt.py`, `tests/test_ipv6fmt.py`, plus
  `team/handoffs/ipv6fmt.md` and `team/status/ipv6fmt.json` as required by the worker
  instructions.
