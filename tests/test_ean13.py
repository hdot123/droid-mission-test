"""Tests for ean13 module (this file tests only ean13 behavior)."""

import pytest

import ean13


def test_check_digit_example():
    assert ean13.check_digit("400638133393") == 1


def test_is_valid_true():
    assert ean13.is_valid("4006381333931") is True


def test_is_valid_false():
    assert ean13.is_valid("4006381333932") is False


def test_check_digit_all_zero():
    assert ean13.check_digit("000000000000") == 0


def test_check_digit_weighting():
    # Even positions weighted 3, odd positions weighted 1.
    # "123456789012": sum = (1+3+5+7+9+1)*1 + (2+4+6+8+0+2)*3
    #              = 26 + 66 = 92 -> 92 % 10 = 2 -> 10 - 2 = 8
    assert ean13.check_digit("123456789012") == 8


def test_check_digit_result_ten_maps_to_zero():
    # Weighted sum = 1*1 + 3*3 = 10 -> 10 % 10 == 0 -> check digit 0.
    assert ean13.check_digit("000000000013") == 0


def test_check_digit_invalid_input_raises():
    with pytest.raises(ValueError):
        ean13.check_digit("40063813339")  # 11 digits
    with pytest.raises(ValueError):
        ean13.check_digit("4006381333931")  # 13 digits
    with pytest.raises(ValueError):
        ean13.check_digit("40063813339a")  # non-digit
    with pytest.raises(ValueError):
        ean13.check_digit(400638133393)  # not a string


def test_is_valid_malformed_returns_false():
    assert ean13.is_valid("400638133393") is False  # 12 digits
    assert ean13.is_valid("40063813339311") is False  # 14 digits
    assert ean13.is_valid("400638133393x") is False  # non-digit
    assert ean13.is_valid("") is False
    assert ean13.is_valid(None) is False
