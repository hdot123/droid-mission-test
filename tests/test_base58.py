"""Tests for base58 byte codec (work order #407, sub-issue #417)."""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base58 import b58decode, b58encode

ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def test_alphabet_is_bitcoin_style_without_zero_o_i_l():
    assert len(ALPHABET) == 58
    assert len(set(ALPHABET)) == 58
    for ch in "0OIl":
        assert ch not in ALPHABET


# --- acceptance items ---

def test_encode_empty_bytes():
    assert b58encode(b"") == ""


def test_encode_single_zero_byte():
    assert b58encode(b"\x00") == "1"


def test_encode_hello():
    assert b58encode(b"hello") == "Cn8eVZg"


def test_encode_leading_zeros():
    assert b58encode(b"\x00\x00\x0f") == "11G"


def test_decode_hello():
    assert b58decode("Cn8eVZg") == b"hello"


def test_decode_empty_string():
    assert b58decode("") == b""


def test_decode_leading_ones():
    assert b58decode("11G") == b"\x00\x00\x0f"


def test_decode_out_of_alphabet_raises_value_error():
    with pytest.raises(ValueError):
        b58decode("0OIl!")


def test_roundtrip_hello():
    data = b"hello"
    assert b58decode(b58encode(data)) == data


def test_roundtrip_leading_zeros():
    data = b"\x00\x00\x0f"
    assert b58decode(b58encode(data)) == data


# --- additional coverage ---

def test_roundtrip_various():
    for data in (
        b"",
        b"\x00",
        b"\x00\x00\x00",
        b"\xff",
        b"\x00hello\x00",
        bytes(range(256)),
        b"a" * 100,
    ):
        assert b58decode(b58encode(data)) == data


def test_all_single_byte_values_roundtrip():
    for i in range(256):
        data = bytes([i])
        assert b58decode(b58encode(data)) == data


def test_known_encoding_values():
    assert b58encode(b"\x00\x00") == "11"
    assert b58encode(bytes([1])) == "2"
    assert b58encode(bytes([57])) == "z"
    assert b58encode(bytes([58])) == "21"


def test_type_errors():
    with pytest.raises(TypeError):
        b58encode("hello")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        b58decode(b"Cn8eVZg")  # type: ignore[arg-type]
