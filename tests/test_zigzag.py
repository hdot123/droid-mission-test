import pytest

from zigzag import decode, encode


def test_encode_basic():
    assert encode(0) == 0
    assert encode(-1) == 1
    assert encode(1) == 2
    assert encode(-2) == 3
    assert encode(2) == 4


def test_encode_int32_bounds():
    assert encode(2147483647) == 4294967294
    assert encode(-2147483648) == 4294967295


def test_decode_basic():
    assert decode(1) == -1
    assert decode(2) == 1


def test_decode_int32_min():
    assert decode(4294967295) == -2147483648


def test_decode_negative_raises():
    with pytest.raises(ValueError):
        decode(-1)


def test_roundtrip_minus5_to_5():
    for n in range(-5, 6):
        assert decode(encode(n)) == n
