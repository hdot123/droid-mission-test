"""tests for manchester: IEEE 802.3 曼彻斯特编解码。"""

import pytest

import manchester


def test_encode_examples():
    assert manchester.encode("1") == "10"
    assert manchester.encode("0") == "01"
    assert manchester.encode("1011") == "10011010"
    assert manchester.encode("") == ""


def test_decode_examples():
    assert manchester.decode("10011010") == "1011"
    assert manchester.decode("10") == "1"
    assert manchester.decode("01") == "0"
    assert manchester.decode("") == ""


def test_encode_rejects_non_bit_characters():
    with pytest.raises(ValueError):
        manchester.encode("10a")
    with pytest.raises(ValueError):
        manchester.encode("2")
    with pytest.raises(ValueError):
        manchester.encode(" ")


def test_decode_rejects_odd_length():
    with pytest.raises(ValueError):
        manchester.decode("1")
    with pytest.raises(ValueError):
        manchester.decode("100")


def test_decode_rejects_illegal_pairs():
    with pytest.raises(ValueError):
        manchester.decode("00")
    with pytest.raises(ValueError):
        manchester.decode("11")
    with pytest.raises(ValueError):
        manchester.decode("1011")
    with pytest.raises(ValueError):
        manchester.decode("10a1")


def test_roundtrip():
    bits = "1011001110"
    assert manchester.decode(manchester.encode(bits)) == bits
