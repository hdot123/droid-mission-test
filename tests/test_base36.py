import pytest

from base36 import decode, encode


def test_encode_zero():
    assert encode(0) == "0"


def test_encode_boundaries():
    assert encode(35) == "z"
    assert encode(36) == "10"
    assert encode(9) == "9"
    assert encode(10) == "a"


def test_encode_samples():
    assert encode(123456789) == "21i3v9"
    assert encode(987654321) == "gc0uy9"
    assert encode(2**64 - 1) == "3w5e11264sgsf"


def test_decode_samples():
    assert decode("21i3v9") == 123456789
    assert decode("z") == 35
    assert decode("10") == 36
    assert decode("0") == 0


def test_decode_case_insensitive():
    assert decode("GC0UY9") == 987654321
    assert decode("21I3V9") == 123456789
    assert decode("Z") == 35


def test_encode_negative_raises():
    with pytest.raises(ValueError):
        encode(-1)


def test_decode_empty_raises():
    with pytest.raises(ValueError):
        decode("")


def test_decode_invalid_character_raises():
    with pytest.raises(ValueError):
        decode("12!")
    for bad in ("12!", "abc-", "a b", "hello world"):
        with pytest.raises(ValueError):
            decode(bad)


def test_roundtrip():
    for n in (0, 1, 35, 36, 123456789, 987654321, 2**32, 2**64 - 1):
        assert decode(encode(n)) == n


def test_roundtrip_large():
    n = 2**64 - 1
    assert decode(encode(n)) == n
