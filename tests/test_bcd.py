"""bcd 的验收测试。"""

import pytest

import bcd


def test_encode_zero():
    assert bcd.encode(0) == 0x0


def test_encode_single_digit():
    assert bcd.encode(9) == 0x9


def test_encode_two_digits():
    assert bcd.encode(12) == 0x12


def test_encode_three_digits():
    assert bcd.encode(123) == 0x123


def test_encode_four_digits():
    assert bcd.encode(2026) == 0x2026


def test_encode_ninety_nine():
    assert bcd.encode(99) == 0x99


def test_decode_three_digits():
    assert bcd.decode(0x123) == 123


def test_decode_four_digits():
    assert bcd.decode(0x2026) == 2026


def test_decode_ninety_nine():
    assert bcd.decode(0x99) == 99


def test_decode_invalid_nibble_raises():
    with pytest.raises(ValueError):
        bcd.decode(0x1A)


def test_decode_negative_raises():
    with pytest.raises(ValueError):
        bcd.decode(-1)


def test_encode_negative_raises():
    with pytest.raises(ValueError):
        bcd.encode(-1)


def test_round_trip_0_to_999():
    for i in range(1000):
        assert bcd.decode(bcd.encode(i)) == i
