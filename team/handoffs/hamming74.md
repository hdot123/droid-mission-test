# Handoff: hamming74 (sub-issue #282)

## What was requested

Process card `hamming74` for work order #279 (第三十五轮 · 并发加压第四组 C 单):
implement the (7,4) Hamming code component, owning exactly two new files:

- `hamming74.py`
- `tests/test_hamming74.py`

Spec (verbatim scope):

- Convention: data bits d1d2d3d4 (4 bits, integer 0-15, MSB first); 7-bit codeword
  MSB first is `p1 p2 d1 p3 d2 d3 d4`, where p1 checks d1d2d4, p2 checks d1d3d4,
  p3 checks d2d3d4, all even parity.
- `encode(data: int) -> int`: input 0-15, returns 7-bit codeword (0-127); ValueError
  on out-of-range input.
- `decode(code: int) -> int`: input 0-127, correct at most one bit error using the
  syndrome, then return the 4 data bits; ValueError on out-of-range input.

Acceptance items: `encode(0) == 0`; `encode(0b1011) == 0b0110011` (51); round-trip
identity for all 16 values; all 7 single-bit flips of `encode(0b1011)` decode back to
`0b1011`; `encode(16)` raises ValueError.

## What I did

- Created `hamming74.py` (standard library only, no imports of `crc16`/`parity2d`):
  - `encode` computes p1/p2/p3 as even parity over the specified groups and packs the
    codeword as `p1 p2 d1 p3 d2 d3 d4` (MSB first).
  - `decode` recomputes the three check groups; a nonzero syndrome maps directly to the
    erroneous bit position (MSB-first positions 1..7 = p1,p2,d1,p3,d2,d3,d4), flips it,
    then returns the 4 data bits.
  - Out-of-range inputs (and non-int/bool inputs) raise `ValueError`.
- Created `tests/test_hamming74.py` with one test case per acceptance item:
  - `test_encode_zero`, `test_encode_1011`, `test_encode_out_of_range`,
    `test_roundtrip_all_16_values`, `test_flip_each_bit_of_1011`.

## What I did not do

- Did not create or touch `crc16.py`, `parity2d.py`, or their tests (other processes
  own those).
- Did not modify any existing file (`README.md`, `roman.py`, `legacy_stringkit.py`,
  existing tests, git state).
- Did not commit or push.
- No dependencies beyond the standard library (`unittest` in tests).

## Checks run and results

- `python3 -m pytest tests/test_hamming74.py -q` → **5 passed** (exit 0)
- `python3 -m pytest tests/ -q` → **16 passed** (exit 0) — includes the other
  processes' test files present in the tree at run time.

Note: pytest was not installed in the environment initially; I installed it via
`pip3 install pytest` (pytest 9.2.0) to run the checks verbatim. This did not modify
any repository file.

## What the validator must pay attention to

- The checks are sensitive to sibling deliverables: `tests/ -q` passes only when
  `crc16.py`/`parity2d.py` and their tests are present and correct (they were present
  and green at my run time; 16 tests total).
- The codeword bit order is MSB-first `p1 p2 d1 p3 d2 d3 d4`; bit-flip tests index
  bits as `1 << bit` for `bit in range(7)`, matching that order.
- `decode` corrects only single-bit errors; double-bit errors are outside the spec and
  are not tested.
