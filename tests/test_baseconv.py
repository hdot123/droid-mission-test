"""Tests for the baseconv module."""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from baseconv import convert


def test_convert_ff_hex_to_dec():
    assert convert("ff", 16, 10) == "255"


def test_convert_negative_binary_to_dec():
    assert convert("-101", 2, 10) == "-5"


def test_convert_dec_to_hex():
    assert convert("255", 10, 16) == "ff"


def test_zero_returns_zero():
    assert convert("0", 10, 2) == "0"
    assert convert("000", 10, 16) == "0"
    assert convert("0", 36, 2) == "0"


def test_negative_zero_value():
    assert convert("-0", 10, 2) == "0"


def test_no_leading_zeros_in_output():
    assert convert("007", 10, 10) == "7"
    assert convert("000255", 10, 16) == "ff"


def test_case_insensitive_letters():
    assert convert("FF", 16, 10) == "255"
    assert convert("Ff", 16, 10) == "255"
    assert convert("AbC", 36, 10) == "13368"


def test_same_base_identity():
    assert convert("123", 10, 10) == "123"
    assert convert("-abc", 36, 36) == "-abc"


def test_boundary_base_2():
    assert convert("1010", 2, 10) == "10"
    assert convert("10", 10, 2) == "1010"


def test_boundary_base_36():
    assert convert("z", 36, 10) == "35"
    assert convert("35", 10, 36) == "z"
    assert convert("10", 36, 10) == "36"


def test_large_number_roundtrip():
    s = "123456789012345678901234567890"
    assert convert(s, 10, 36) != ""
    assert convert(convert(s, 10, 36), 36, 10) == s


def test_base_out_of_range_low():
    with pytest.raises(ValueError):
        convert("10", 1, 10)
    with pytest.raises(ValueError):
        convert("10", 10, 1)


def test_base_out_of_range_high():
    with pytest.raises(ValueError):
        convert("10", 37, 10)
    with pytest.raises(ValueError):
        convert("10", 10, 37)


def test_empty_string():
    with pytest.raises(ValueError):
        convert("", 10, 16)


def test_character_beyond_source_base():
    with pytest.raises(ValueError):
        convert("ff", 10, 16)
    with pytest.raises(ValueError):
        convert("2", 2, 10)


def test_invalid_characters():
    with pytest.raises(ValueError):
        convert("12a", 10, 16)
    with pytest.raises(ValueError):
        convert("10 2", 10, 16)
    with pytest.raises(ValueError):
        convert("1.0", 10, 16)


def test_sign_only_string():
    with pytest.raises(ValueError):
        convert("-", 10, 16)
