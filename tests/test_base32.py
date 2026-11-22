"""Tests for base32 module (RFC 4648 standard Base32)."""

import pytest

import base32


# --- Spec examples ---------------------------------------------------------

def test_encode_foo():
    assert base32.encode(b"foo") == "MZXW6==="


def test_encode_empty():
    assert base32.encode(b"") == ""


def test_decode_foo():
    assert base32.decode("MZXW6===") == b"foo"


def test_decode_empty():
    assert base32.decode("") == b""


# --- RFC 4648 test vectors -------------------------------------------------

@pytest.mark.parametrize(
    "raw,encoded",
    [
        (b"", ""),
        (b"f", "MY======"),
        (b"fo", "MZXQ===="),
        (b"foo", "MZXW6==="),
        (b"foob", "MZXW6YQ="),
        (b"fooba", "MZXW6YTB"),
        (b"foobar", "MZXW6YTBOI======"),
    ],
)
def test_rfc4648_vectors(raw, encoded):
    assert base32.encode(raw) == encoded
    assert base32.decode(encoded) == raw


# --- Round trips for every remainder length --------------------------------

@pytest.mark.parametrize("n", list(range(12)))
def test_roundtrip_various_lengths(n):
    data = bytes((i * 7 + 3) % 256 for i in range(n))
    assert base32.decode(base32.encode(data)) == data


# --- Rejections ------------------------------------------------------------

def test_decode_lowercase_raises():
    with pytest.raises(ValueError):
        base32.decode("mzxw6===")


def test_decode_unpadded_raises():
    with pytest.raises(ValueError):
        base32.decode("MZXW6")


def test_decode_too_short_padding_raises():
    with pytest.raises(ValueError):
        base32.decode("MZXW6==")


def test_decode_illegal_character_raises():
    with pytest.raises(ValueError):
        base32.decode("MZXW68==")  # '8' not in alphabet
    with pytest.raises(ValueError):
        base32.decode("MZXW6!==")
    with pytest.raises(ValueError):
        base32.decode("MZXW6===!")


def test_decode_padding_in_middle_raises():
    with pytest.raises(ValueError):
        base32.decode("MZX======"[:4] + "====" + "MZ==")


def test_encode_rejects_non_bytes():
    with pytest.raises(TypeError):
        base32.encode("foo")
