"""Tests for hexcodec only."""

import pytest

import hexcodec


def test_encode_example():
    assert hexcodec.encode(b"\xde\xad") == "dead"


def test_encode_empty():
    assert hexcodec.encode(b"") == ""


def test_encode_lowercase_and_full_byte_range():
    data = bytes(range(256))
    out = hexcodec.encode(data)
    assert out == data.hex()
    assert out == out.lower()
    assert len(out) == 512


def test_decode_example():
    assert hexcodec.decode("dead") == b"\xde\xad"


def test_decode_empty():
    assert hexcodec.decode("") == b""


def test_roundtrip():
    data = b"\x00\x01\xfe\xffhello"
    assert hexcodec.decode(hexcodec.encode(data)) == data


def test_decode_rejects_odd_length():
    with pytest.raises(ValueError):
        hexcodec.decode("abc")


def test_decode_rejects_non_hex_characters():
    with pytest.raises(ValueError):
        hexcodec.decode("zz")
    with pytest.raises(ValueError):
        hexcodec.decode("de ad!")  # space and punctuation are illegal
