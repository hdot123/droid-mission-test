"""Tests for isbn13 (round 40 · unit D)."""

import pytest

from isbn13 import check_digit, is_valid


def test_check_digit_known_value():
    assert check_digit("978030640615") == 7


def test_is_valid_true():
    assert is_valid("9780306406157") is True


def test_is_valid_with_hyphens():
    assert is_valid("978-0-306-40615-7") is True


def test_is_valid_wrong_check_digit():
    assert is_valid("9780306406158") is False


def test_check_digit_second_known_value():
    assert check_digit("978013468599") == 1


def test_is_valid_second_known_value():
    assert is_valid("9780134685991") is True


def test_check_digit_rejects_wrong_length():
    with pytest.raises(ValueError):
        check_digit("97803064061")


def test_is_valid_rejects_wrong_length():
    with pytest.raises(ValueError):
        is_valid("978030640615")
