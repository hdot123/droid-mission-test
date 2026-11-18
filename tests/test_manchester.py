"""Tests for manchester.py (IEEE 802.3 Manchester coding)."""

import pytest

import manchester


def test_encode_1010():
    assert manchester.encode("1010") == "01100110"


def test_encode_single_zero():
    assert manchester.encode("0") == "10"


def test_encode_single_one():
    assert manchester.encode("1") == "01"


def test_decode_01100110():
    assert manchester.decode("01100110") == "1010"


def test_decode_00_raises():
    with pytest.raises(ValueError):
        manchester.decode("00")


def test_roundtrip_11001010():
    s = "11001010"
    assert manchester.decode(manchester.encode(s)) == s


def test_encode_invalid_char_raises():
    with pytest.raises(ValueError):
        manchester.encode("01x")


def test_encode_empty_returns_empty():
    assert manchester.encode("") == ""


def test_decode_empty_returns_empty():
    assert manchester.decode("") == ""


def test_decode_odd_length_raises():
    with pytest.raises(ValueError):
        manchester.decode("01100")


def test_decode_illegal_pair_11_raises():
    with pytest.raises(ValueError):
        manchester.decode("0111")
