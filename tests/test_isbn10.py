"""Tests for the isbn10 module."""

import pytest

import isbn10


class TestCheckDigit:
    def test_signature_and_type(self):
        result = isbn10.check_digit("030640615")
        assert isinstance(result, str)

    def test_example_030640615(self):
        assert isbn10.check_digit("030640615") == "2"

    def test_example_043942089(self):
        assert isbn10.check_digit("043942089") == "X"

    def test_check_value_zero(self):
        # Weighted sum 22 % 11 == 0
        assert isbn10.check_digit("000000000") == "0"

    @pytest.mark.parametrize(
        "bad",
        ["", "12345678", "1234567890", "12345678a", "12345678 ", " 123456789", "１２３４５６７８９", None, 123456789],
    )
    def test_non_9_digit_input_raises_value_error(self, bad):
        with pytest.raises(ValueError):
            isbn10.check_digit(bad)


class TestIsValid:
    def test_signature_and_returns_bool(self):
        result = isbn10.is_valid("0306406152")
        assert isinstance(result, bool)

    def test_example_valid_numeric(self):
        assert isbn10.is_valid("0306406152") is True

    def test_example_valid_x(self):
        assert isbn10.is_valid("043942089X") is True

    def test_example_wrong_check_char(self):
        assert isbn10.is_valid("0306406153") is False

    @pytest.mark.parametrize(
        "bad",
        [
            "",
            "030640615",       # too short
            "03064061522",     # too long
            "030640615X",      # wrong check char
            "030640615x",      # lowercase x not allowed
            "03064061a2",      # non-digit in first 9
            "abcdefghi2",      # non-digit in first 9
            "030640615!",      # bad last character
            "０３０６４０６１５２",  # fullwidth digits not allowed
            None,
            1234567890,
        ],
    )
    def test_malformed_input_returns_false_without_raising(self, bad):
        assert isbn10.is_valid(bad) is False
