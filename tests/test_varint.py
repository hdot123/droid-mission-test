"""tests for varint: unsigned LEB128 encode/decode."""

import pytest

import varint


def test_encode_zero():
    assert varint.encode(0) == b"\x00"


def test_encode_one():
    assert varint.encode(1) == b"\x01"


def test_encode_127():
    assert varint.encode(127) == b"\x7f"


def test_encode_128():
    assert varint.encode(128) == b"\x80\x01"


def test_encode_300():
    assert varint.encode(300) == b"\xac\x02"


def test_encode_624485():
    assert varint.encode(624485) == b"\xe5\x8e\x26"


def test_decode_624485():
    assert varint.decode(b"\xe5\x8e\x26") == 624485


def test_decode_300():
    assert varint.decode(b"\xac\x02") == 300


def test_encode_negative_raises():
    with pytest.raises(ValueError):
        varint.encode(-1)


def test_decode_empty_raises():
    with pytest.raises(ValueError):
        varint.decode(b"")


def test_decode_unterminated_raises():
    with pytest.raises(ValueError):
        varint.decode(b"\x80")


def test_decode_trailing_raises():
    with pytest.raises(ValueError):
        varint.decode(b"\x01\x02")


def test_roundtrip_123456789():
    assert varint.decode(varint.encode(123456789)) == 123456789
