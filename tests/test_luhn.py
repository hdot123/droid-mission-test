import pytest

import luhn


def test_check_digit_examples():
    assert luhn.check_digit("7992739871") == "3"
    assert luhn.check_digit("424242424242424") == "2"


def test_is_valid_examples():
    assert luhn.is_valid("79927398713") is True
    assert luhn.is_valid("79927398714") is False
    assert luhn.is_valid("7992739871a") is False


def test_check_digit_empty_raises():
    with pytest.raises(ValueError):
        luhn.check_digit("")


def test_check_digit_non_digit_raises():
    with pytest.raises(ValueError):
        luhn.check_digit("12a")


def test_is_valid_empty_returns_false():
    assert luhn.is_valid("") is False


def test_is_valid_non_numeric_returns_false():
    assert luhn.is_valid("7992739871a") is False
    assert luhn.is_valid("abc") is False
