"""Tests for luhn.is_valid (Luhn checksum validation)."""

import pytest

from luhn import is_valid


def test_valid_numbers():
    assert is_valid("79927398713")
    assert is_valid("4532015112830366")
    assert is_valid("1234567890123452")


def test_invalid_numbers():
    assert not is_valid("79927398714")
    assert not is_valid("4532015112830367")
    assert not is_valid("1234567890123456")


def test_separators_ignored():
    assert is_valid("4532 0151 1283 0366")
    assert is_valid("4532-0151-1283-0366")
    assert is_valid(" 4532-0151 1283-0366 ")
    # Separator-only input leaves fewer than 2 digits -> rejected.
    with pytest.raises(ValueError):
        is_valid(" -  ")
    with pytest.raises(ValueError):
        is_valid("--")


def test_rejects_non_digit_content():
    with pytest.raises(ValueError):
        is_valid("4532a15112830366")
    with pytest.raises(ValueError):
        is_valid("4532.015112830366")
    with pytest.raises(ValueError):
        is_valid("4532_015112830366")
    with pytest.raises(ValueError):
        is_valid("453201511283036!")


def test_rejects_length_below_two():
    with pytest.raises(ValueError):
        is_valid("")
    with pytest.raises(ValueError):
        is_valid("0")
    with pytest.raises(ValueError):
        is_valid("7")
    with pytest.raises(ValueError):
        is_valid(" ")
