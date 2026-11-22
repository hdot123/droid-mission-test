import pytest

from baseconv import convert


def test_hex_to_dec_lower():
    assert convert("ff", 16, 10) == "255"


def test_hex_to_dec_upper_case_input():
    assert convert("FF", 16, 10) == "255"


def test_dec_to_hex_lowercase_output():
    assert convert("255", 10, 16) == "ff"


def test_bin_to_dec():
    assert convert("1010", 2, 10) == "10"


def test_dec_to_bin():
    assert convert("10", 10, 2) == "1010"


def test_base36_to_dec():
    assert convert("z", 36, 10) == "35"


def test_dec_to_base36():
    assert convert("35", 10, 36) == "z"


def test_negative_conversion():
    assert convert("-255", 10, 16) == "-ff"


def test_zero_output():
    assert convert("0", 10, 2) == "0"


def test_leading_zeros_stripped():
    assert convert("007", 10, 10) == "7"


def test_digit_out_of_range_for_from_base():
    with pytest.raises(ValueError):
        convert("2", 2, 10)


def test_from_base_out_of_range():
    with pytest.raises(ValueError):
        convert("10", 1, 10)


def test_to_base_out_of_range():
    with pytest.raises(ValueError):
        convert("10", 10, 37)


def test_empty_string():
    with pytest.raises(ValueError):
        convert("", 10, 10)
