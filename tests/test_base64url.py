import pytest

from base64url import decode, encode


def test_encode_empty():
    assert encode(b"") == ""


def test_encode_hello():
    assert encode(b"hello") == "aGVsbG8"


def test_encode_urlsafe_alphabet():
    # '+' -> '-', '/' -> '_', and no '=' padding.
    assert encode(b"\xfb\xff") == "-_8"


def test_decode_hello():
    assert decode("aGVsbG8") == b"hello"


def test_decode_urlsafe_alphabet():
    assert decode("-_8") == b"\xfb\xff"


def test_decode_rejects_padding():
    with pytest.raises(ValueError):
        decode("aGVsbG8=")


def test_decode_rejects_length_mod_4_one():
    with pytest.raises(ValueError):
        decode("a")


def test_decode_rejects_out_of_alphabet_characters():
    for bad in ("a+b", "a/b", "a*b", "a b"):
        with pytest.raises(ValueError):
            decode(bad)


def test_roundtrip_identity():
    for payload in (b"", b"\x00", b"foobar"):
        assert decode(encode(payload)) == payload
