"""Tests for base45.py (RFC 9285)."""

import pytest

from base45 import base45_encode, base45_decode


# --- Acceptance items 1-5: encode ---

def test_encode_rfc_example_ab():
    assert base45_encode(b"AB") == "BB8"


def test_encode_rfc_example_hello():
    assert base45_encode(b"Hello!!") == "%69 VD92EX0"


def test_encode_empty():
    assert base45_encode(b"") == ""


def test_encode_null_byte():
    assert base45_encode(b"\x00") == "00"


def test_encode_0xff():
    assert base45_encode(b"\xff") == "U5"


# --- Acceptance items 6-9: decode ---

def test_decode_rfc_example_ab():
    assert base45_decode("BB8") == b"AB"


def test_decode_rfc_example_hello():
    assert base45_decode("%69 VD92EX0") == b"Hello!!"


def test_decode_empty():
    assert base45_decode("") == b""


def test_decode_0xff():
    assert base45_decode("U5") == b"\xff"


# --- Acceptance item 10: round-trips ---

@pytest.mark.parametrize(
    "data",
    [
        b"hello world",
        b"\x00\x01\x02\xff\xfe",
        b"1234567890",
        bytes(range(256)),
    ],
)
def test_roundtrip(data):
    assert base45_decode(base45_encode(data)) == data


# --- Acceptance item 11: length mod 3 == 1 -> ValueError ---

def test_decode_length_mod3_1_single_char():
    with pytest.raises(ValueError):
        base45_decode("A")


def test_decode_length_mod3_1_four_chars():
    with pytest.raises(ValueError):
        base45_decode("BB8B")


# --- Acceptance item 12: character outside alphabet ---

def test_decode_invalid_character():
    with pytest.raises(ValueError):
        base45_decode("A!")


# --- Acceptance item 13: two-char group decodes > 255 ---

def test_decode_two_char_overflow():
    # 'Z' = 35 -> 35 + 45*35 = 1610 > 255
    with pytest.raises(ValueError):
        base45_decode("ZZ")


def test_decode_two_char_overflow_edge():
    # Max two-char value from valid decode path: 44 + 45*44 = 2024 > 255
    with pytest.raises(ValueError):
        base45_decode(":X")  # ':' = 44, 'X' = 33 -> 44 + 45*33 = 1529 > 255


# --- Additional overflow coverage: three-char group > 65535 ---

def test_decode_three_char_overflow():
    # x = v0 + 45*v1 + 2025*v2; ':'=44, ':'=44, ':'=44 -> 44+1980+89100 = 91124 > 65535
    with pytest.raises(ValueError):
        base45_decode(":::")


# --- Acceptance items 14-15: TypeError ---

def test_encode_non_bytes_type_error():
    with pytest.raises(TypeError):
        base45_encode("AB")


def test_decode_non_str_type_error():
    with pytest.raises(TypeError):
        base45_decode(b"BB8")
