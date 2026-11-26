"""Tests for joaat.py — Jenkins one-at-a-time 32-bit hash.

Every acceptance item from the work order has a corresponding test case.
The independent reference implementations (reduce/decomposed-step and
streaming chunked-update) live in this file.
"""

import random
from functools import reduce

import pytest

from joaat import joaat_hash

_MASK = 0xFFFFFFFF


# ---------------------------------------------------------------------------
# Independent reference implementation 1: reduce / decomposed steps
# ---------------------------------------------------------------------------
def ref_reduce_joaat(data: bytes) -> int:
    def step(h: int, b: int) -> int:
        h = (h + b) & _MASK
        h = (h + ((h << 10) & _MASK)) & _MASK
        h = (h ^ (h >> 6)) & _MASK
        return h

    h = reduce(step, data, 0)
    h = (h + ((h << 3) & _MASK)) & _MASK
    h = (h ^ (h >> 11)) & _MASK
    h = (h + ((h << 15) & _MASK)) & _MASK
    return h


# ---------------------------------------------------------------------------
# Independent reference implementation 2: streaming chunked update
# ---------------------------------------------------------------------------
class _JoaatStreamer:
    """Streaming joaat: holds partial state, feeds bytes in chunks."""

    def __init__(self) -> None:
        self._h = 0

    def update(self, chunk: bytes) -> None:
        h = self._h
        for b in chunk:
            h = (h + b) & _MASK
            h = (h + (h << 10)) & _MASK
            h ^= h >> 6
            h &= _MASK
        self._h = h

    def digest(self) -> int:
        h = self._h
        h = (h + (h << 3)) & _MASK
        h ^= h >> 11
        h &= _MASK
        h = (h + (h << 15)) & _MASK
        return h


def ref_stream_joaat(data: bytes, chunk_size: int = 7) -> int:
    s = _JoaatStreamer()
    for i in range(0, len(data), chunk_size):
        s.update(data[i : i + chunk_size])
    return s.digest()


# ---------------------------------------------------------------------------
# Acceptance: known values
# ---------------------------------------------------------------------------
def test_empty_input_is_zero():
    assert joaat_hash(b"") == 0


@pytest.mark.parametrize("k", [1, 2, 3, 4, 5])
def test_all_zero_input_fixed_point(k):
    assert joaat_hash(b"\x00" * k) == 0


# ---------------------------------------------------------------------------
# Acceptance: result always in [0, 2^32)
# ---------------------------------------------------------------------------
def test_result_always_in_uint32_range():
    rng = random.Random(20261126)
    for _ in range(200):
        n = rng.randint(0, 40)
        data = bytes(rng.getrandbits(8) for _ in range(n))
        h = joaat_hash(data)
        assert isinstance(h, int)
        assert 0 <= h < 2**32


# ---------------------------------------------------------------------------
# Acceptance: agreement with independent implementations over random
# byte strings of length 0-40 (reduce/decomposed-step and streaming
# chunked-update), byte for byte
# ---------------------------------------------------------------------------
def test_agrees_with_independent_implementations():
    rng = random.Random(944)
    for _ in range(300):
        n = rng.randint(0, 40)
        data = bytes(rng.getrandbits(8) for _ in range(n))
        expected_reduce = ref_reduce_joaat(data)
        expected_stream = ref_stream_joaat(data, chunk_size=rng.randint(1, 13))
        assert joaat_hash(data) == expected_reduce, data
        assert joaat_hash(data) == expected_stream, data


def test_agreement_includes_empty_and_edge_lengths():
    # Explicit coverage of every length 0..40 (short strings, chunk edges).
    rng = random.Random(7)
    for n in range(41):
        data = bytes(rng.getrandbits(8) for _ in range(n))
        assert joaat_hash(data) == ref_reduce_joaat(data)
        assert joaat_hash(data) == ref_stream_joaat(data, chunk_size=1)
        assert joaat_hash(data) == ref_stream_joaat(data, chunk_size=n or 1)


# ---------------------------------------------------------------------------
# Acceptance: TypeError on non-bytes input (str, int, list, bytearray)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "bad",
    [
        "abc",
        123,
        [1, 2],
        bytearray(b"a"),
    ],
)
def test_non_bytes_input_raises_typeerror(bad):
    with pytest.raises(TypeError):
        joaat_hash(bad)
