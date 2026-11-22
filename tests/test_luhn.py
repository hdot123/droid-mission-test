import pytest

from luhn import check_digit, is_valid


def test_valid_number():
    assert is_valid("79927398713") is True


def test_invalid_check_digit():
    assert is_valid("79927398710") is False


def test_check_digit_value():
    assert check_digit("7992739871") == 3


def test_single_zero_is_valid():
    assert is_valid("0") is True


def test_empty_string_is_invalid():
    assert is_valid("") is False


def test_non_digit_characters_are_invalid():
    assert is_valid("7992a398713") is False


def test_check_digit_empty_prefix_raises():
    with pytest.raises(ValueError):
        check_digit("")


def test_check_digit_non_digit_prefix_raises():
    with pytest.raises(ValueError):
        check_digit("7992a39871")


def test_check_digit_round_trip():
    prefix = "7992739871"
    digit = check_digit(prefix)
    assert is_valid(prefix + str(digit)) is True


def test_check_digit_range():
    for prefix in ("1", "9", "500000000000000"):
        assert 0 <= check_digit(prefix) <= 9
