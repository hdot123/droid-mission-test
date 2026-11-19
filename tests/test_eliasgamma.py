"""Tests for eliasgamma — Elias gamma encoding (bit strings)."""

import pytest

import eliasgamma
from eliasgamma import elias_decode, elias_decode_list, elias_encode, elias_encode_list


# --- elias_encode: acceptance examples -------------------------------------

ENCODED = {
    1: "1",
    2: "010",
    3: "011",
    4: "00100",
    5: "00101",
    6: "00110",
    7: "00111",
    8: "0001000",
    9: "0001001",
    10: "0001010",
    15: "0001111",
    16: "000010000",
}


@pytest.mark.parametrize("n,expected", sorted(ENCODED.items()))
def test_encode_examples(n, expected):
    assert elias_encode(n) == expected


@pytest.mark.parametrize("n,expected", sorted(ENCODED.items()))
def test_examples_decode_back(n, expected):
    assert elias_decode(expected) == n


def test_round_trip_1_to_199():
    for n in range(1, 200):
        assert elias_decode(elias_encode(n)) == n


# --- list codecs ------------------------------------------------------------

def test_encode_list_example():
    assert elias_encode_list([1, 2, 3]) == "1010011"


def test_decode_list_example():
    assert elias_decode_list("1010011") == [1, 2, 3]


def test_decode_empty_list():
    assert elias_decode_list("") == []


def test_list_round_trip():
    nums = [5, 1, 9, 16]
    assert elias_decode_list(elias_encode_list(nums)) == nums


def test_encode_list_accepts_tuple():
    assert elias_encode_list((1, 2, 3)) == "1010011"


# --- elias_encode validation ------------------------------------------------

def test_encode_zero_raises_value_error():
    with pytest.raises(ValueError):
        elias_encode(0)


def test_encode_negative_raises_value_error():
    with pytest.raises(ValueError):
        elias_encode(-3)


def test_encode_float_raises_type_error():
    with pytest.raises(TypeError):
        elias_encode(2.0)


def test_encode_bool_rejected():
    with pytest.raises(TypeError):
        elias_encode(True)


# --- elias_decode validation ------------------------------------------------

@pytest.mark.parametrize("bad", ["", "0", "01", "0101", "012"])
def test_decode_invalid_bitstrings(bad):
    with pytest.raises(ValueError):
        elias_decode(bad)


def test_decode_non_str_raises_type_error():
    with pytest.raises(TypeError):
        elias_decode(10)


def test_decode_list_invalid_bits_raise_value_error():
    with pytest.raises(ValueError):
        elias_decode_list("0100")


def test_decode_list_non_str_raises_type_error():
    with pytest.raises(TypeError):
        elias_decode_list(10)


def test_encode_list_non_sequence_raises_type_error():
    with pytest.raises(TypeError):
        elias_encode_list("123")


def test_encode_list_element_validation():
    with pytest.raises(ValueError):
        elias_encode_list([1, 0])
    with pytest.raises(TypeError):
        elias_encode_list([1, 2.5])


def test_decode_list_midway_truncation_raises():
    # "1" decodes, then "00" is a truncated codeword.
    with pytest.raises(ValueError):
        elias_decode_list("100")


def test_decode_list_midway_illegal_char_raises():
    with pytest.raises(ValueError):
        elias_decode_list("10x1")


def test_module_exposes_expected_api():
    for name in ("elias_encode", "elias_decode", "elias_encode_list", "elias_decode_list"):
        assert hasattr(eliasgamma, name)
