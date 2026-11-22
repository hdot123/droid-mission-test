"""Tests for b64url: URL-safe Base64 with padding stripped."""

import pytest

from b64url import decode, encode


def test_encode_spec_examples():
    assert encode(b"\xfb\xff") == "-_8"
    assert encode(b"") == ""


def test_encode_uses_urlsafe_alphabet_and_strips_padding():
    # 4 bytes -> 8 base64 chars with '==' padding; padding must be stripped.
    assert encode(b"\xfb\xff\xfe\xff") == "-__-_w"
    # 1-byte input normally needs '==' padding; must be stripped.
    encoded = encode(b"f")
    assert encoded == "Zg"
    assert not encoded.endswith("=")


def test_decode_empty_string():
    assert decode("") == b""


def test_decode_restores_missing_padding():
    assert decode("Zg") == b"f"
    assert decode("Zg==") == b"f"
    assert decode("Zm9v") == b"foo"
    # 'Zg' needs '==' padding; 'Zm9v' needs none.
    assert decode("Zg") == decode("Zg==")


def test_roundtrip():
    for payload in (b"", b"f", b"fo", b"foo", b"\xfb\xff", b"\x00\x01\x02\x7f"):
        assert decode(encode(payload)) == payload


def test_decode_urlsafe_alphabet():
    # '-' and '_' decode to what '+' and '/' would in standard base64.
    assert decode("-_8") == b"\xfb\xff"
    assert decode("-_-_") == b"\xfb\xff\xbf"


def test_decode_rejects_illegal_characters():
    with pytest.raises(ValueError):
        decode("ab+d")
    with pytest.raises(ValueError):
        decode("ab/d")
    with pytest.raises(ValueError):
        decode("ab d")
    with pytest.raises(ValueError):
        decode("ab=c")  # '=' only allowed as trailing padding
    with pytest.raises(ValueError):
        decode("ab==cd")
    with pytest.raises(ValueError):
        decode("Zg===")  # more than 2 padding chars


def test_decode_rejects_bad_length():
    with pytest.raises(ValueError):
        decode("a")  # len % 4 == 1 is never valid base64
    with pytest.raises(ValueError):
        decode("abcde")
