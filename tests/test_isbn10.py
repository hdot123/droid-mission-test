"""Tests for isbn10 ISBN-10 check digit validation."""

import pytest

from isbn10 import check_digit, is_valid


def test_check_digit_known_value():
    assert check_digit("030640615") == "2"


def test_is_valid_true():
    assert is_valid("0306406152") is True


def test_is_valid_false_wrong_check_digit():
    assert is_valid("0306406153") is False


def test_check_digit_x_result():
    assert check_digit("080442957") == "X"


def test_is_valid_x_check_digit():
    assert is_valid("080442957X") is True


def test_is_valid_lowercase_x_rejected():
    assert is_valid("080442957x") is False


def test_check_digit_wrong_length_raises():
    with pytest.raises(ValueError):
        check_digit("03064061")


def test_check_digit_non_digit_raises():
    with pytest.raises(ValueError):
        check_digit("03064061A")
    with pytest.raises(ValueError):
        check_digit("030640615X")


def test_check_digit_too_long_raises():
    with pytest.raises(ValueError):
        check_digit("0306406152")


def test_is_valid_length_and_format():
    assert is_valid("") is False
    assert is_valid("030640615") is False  # 9 chars
    assert is_valid("03064061523") is False  # 11 chars
    assert is_valid("030640615A") is False  # non-digit in body
    assert is_valid("X306406152") is False  # X not in last position
    assert is_valid("0306406152") is True


def test_is_valid_never_raises():
    for bad in (None, 1234567890, "short", "waytoolongstring"):
        assert is_valid(bad) is False  # type: ignore[arg-type]
