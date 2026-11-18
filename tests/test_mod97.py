import pytest

from mod97 import is_valid_iban_numeric, remainder


def test_remainder_acceptance_values():
    assert remainder("97") == 0
    assert remainder("98") == 1
    assert remainder("100") == 3


def test_remainder_long_string_acceptance():
    # 20-digit example from the work order; spans multiple chunks (chunk=9),
    # so the chunked algorithm is what produces this value.
    assert remainder("12345678901234567890") == 3


def test_remainder_matches_big_int_reference():
    # Long input beyond any single chunk; cross-check against Python's
    # arbitrary-precision int as an independent oracle.
    digits = "1234567890" * 50  # 500 digits
    assert remainder(digits) == int(digits) % 97


def test_is_valid_iban_numeric_acceptance_values():
    assert is_valid_iban_numeric("98") is True
    assert is_valid_iban_numeric("97") is False


def test_remainder_empty_string_raises_value_error():
    with pytest.raises(ValueError):
        remainder("")


def test_remainder_non_digit_input_raises_value_error():
    with pytest.raises(ValueError):
        remainder("98a")
    with pytest.raises(ValueError):
        remainder("98 7")
    with pytest.raises(ValueError):
        remainder("98.0")
    with pytest.raises(ValueError):
        remainder("98\n")
    with pytest.raises(ValueError):
        remainder("１２")  # full-width digits are not ASCII digits
    with pytest.raises(ValueError):
        remainder(12345)  # wrong type is rejected too, not accepted silently


def test_is_valid_iban_numeric_invalid_input_returns_false():
    assert is_valid_iban_numeric("") is False
    assert is_valid_iban_numeric("98a") is False
    assert is_valid_iban_numeric("97-0") is False
    assert is_valid_iban_numeric(None) is False
    assert is_valid_iban_numeric(98) is False
