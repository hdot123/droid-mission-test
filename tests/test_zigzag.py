import pytest

from zigzag import decode, encode


def test_encode_known_values():
    assert encode(0) == b"\x00"
    assert encode(-1) == b"\x01"
    assert encode(1) == b"\x02"
    assert encode(-2) == b"\x03"
    assert encode(150) == b"\xac\x02"


def test_decode_known_values():
    assert decode(b"\xac\x02") == 150


def test_roundtrip_identity():
    for n in (-1000000, -1, 0, 1, 1000000):
        assert decode(encode(n)) == n


def test_roundtrip_known_values():
    for n in (-2, -1, 0, 1, 150):
        assert decode(encode(n)) == n


def test_decode_empty_raises():
    with pytest.raises(ValueError):
        decode(b"")


def test_decode_unterminated_raises():
    with pytest.raises(ValueError):
        decode(b"\x80")
