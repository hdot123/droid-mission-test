# Handoff: macaddr (sub-issue #331)

## What was requested
Create `macaddr.py` (standard library only, no imports from other deliverables) and `tests/test_macaddr.py`, implementing exactly:

- `normalize(text: str) -> str`: accept three input forms — colon-separated (`AA:BB:CC:DD:EE:FF`), hyphen-separated (`AA-BB-CC-DD-EE-FF`), and dot-separated groups of four (`AABB.CCDD.EEFF`) — case-insensitive hex digits; output lowercase colon-separated form. Raise `ValueError` for wrong group count, wrong group length, non-hex characters, or mixed separators.

Acceptance criteria (each needs a test case):
- `normalize("AA:BB:CC:DD:EE:FF") == "aa:bb:cc:dd:ee:ff"`
- `normalize("AA-BB-CC-DD-EE-FF") == "aa:bb:cc:dd:ee:ff"`
- `normalize("AABB.CCDD.EEFF") == "aa:bb:cc:dd:ee:ff"`
- `normalize("aa:bb:cc:dd:ee")` raises ValueError (too few groups)
- `normalize("GG:BB:CC:DD:EE:FF")` raises ValueError (non-hex character)

## What I did
- Created `macaddr.py`: three compiled regexes (colon 6x2, hyphen 6x2, dot 3x4) match the input form, then lower the separators/ digits into canonical lowercase colon form. For the dot form, each 4-hex group is split into two 2-hex octets so `AABB.CCDD.EEFF` → `aa:bb:cc:dd:ee:ff`. Non-str input and any non-matching form (wrong group count, wrong group length, non-hex chars, mixed separators, empty string) raise `ValueError`. Only `re` from the standard library is used; no imports from other deliverables.
- Created `tests/test_macaddr.py` (unittest-style, runs under pytest) with 10 cases: the 5 required acceptance cases plus lowercase input, mixed separators, too many groups, wrong group length (both dot and colon forms), and empty string.

## What I did not do
- Did not touch any pre-existing file (`roman.py`, `legacy_stringkit.py`, `README.md`, existing tests, etc.).
- Did not create or modify `ipv4kit.py`, `duration.py`, or their tests (other processes own those).
- Did not commit or push.
- Note: `pytest` was not installed in this environment; I installed it with `python3 -m pip install pytest` (now 9.2.0) so the required checks could run. This is an environment change, not a file change.

## Checks run
- `python3 -m pytest tests/test_macaddr.py -q` → **10 passed in 0.01s**
- `python3 -m pytest tests/ -q` → **21 passed in 0.01s** (includes the 10 macaddr cases plus 11 pre-existing baseline cases)

First run failed on the dot form (`'aabb:ccdd:eeff' != 'aa:bb:cc:dd:ee:ff'`); fixed by splitting each 4-hex group into two octets before joining with colons, then both checks passed.

## Notes for the validator
- The dot form must yield six 2-hex octets (`aa:bb:cc:dd:ee:ff`), not three 4-hex groups joined by colons — this was the one subtle point.
- Mixed separators (e.g. `AA:BB-CC-DD-EE-FF`) fail all three regexes and correctly raise `ValueError`.
- All three input forms are matched by anchored full-match regexes, so trailing spaces, wrong counts, and stray characters all raise `ValueError`.
