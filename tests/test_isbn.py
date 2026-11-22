"""Tests for isbn.py only."""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import isbn  # noqa: E402

VALID_ISBN10 = ["0306406152", "080442957X"]
VALID_ISBN13 = ["9780306406157", "9780804429573"]


def test_valid_isbn10():
    for code in VALID_ISBN10:
        assert isbn.is_valid(code) is True


def test_valid_isbn13():
    for code in VALID_ISBN13:
        assert isbn.is_valid(code) is True


def test_hyphens_and_spaces_ignored():
    assert isbn.is_valid("0-306-40615-2") is True
    assert isbn.is_valid("0 306 40615 2") is True
    assert isbn.is_valid("978-0-306-40615-7") is True
    assert isbn.is_valid("--0 306 40615 2--") is True
    assert isbn.is_valid("0-8044-2957-X") is True


def test_x_check_digit_only_as_last_character():
    assert isbn.is_valid("080442957X") is True
    assert isbn.is_valid("080442957x") is False
    assert isbn.is_valid("X306406152") is False
    assert isbn.is_valid("0X06406152") is False


def test_illegal_characters_return_false():
    assert isbn.is_valid("030640615A") is False
    assert isbn.is_valid("0306406152!") is False
    assert isbn.is_valid("978030640615X") is False
    assert isbn.is_valid("abc") is False
    assert isbn.is_valid("0306-4061-5A") is False


def test_invalid_checksums_return_false():
    assert isbn.is_valid("0306406153") is False
    assert isbn.is_valid("9780306406158") is False


def test_invalid_length_returns_false():
    assert isbn.is_valid("") is False
    assert isbn.is_valid("123") is False
    assert isbn.is_valid("03064061520") is False
    assert isbn.is_valid("97803064061570") is False


def test_is_valid_none_raises_type_error():
    with pytest.raises(TypeError):
        isbn.is_valid(None)


def test_to_isbn13_conversion():
    assert isbn.to_isbn13("0306406152") == "9780306406157"
    assert isbn.to_isbn13("080442957X") == "9780804429573"
    assert isbn.to_isbn13("0-306-40615-2") == "9780306406157"
    assert isbn.to_isbn13("0 306 40615 2") == "9780306406157"


def test_to_isbn13_result_passes_is_valid():
    for code in VALID_ISBN10:
        assert isbn.is_valid(isbn.to_isbn13(code)) is True


@pytest.mark.parametrize(
    "bad",
    [
        "0306406153",  # bad ISBN-10 checksum
        "030640615A",  # illegal character
        "03064061520",  # wrong length
        "",  # empty
        "9780306406157",  # valid ISBN-13, not ISBN-10
        "X306406152",  # X in a non-final position
    ],
)
def test_to_isbn13_invalid_input_raises_value_error(bad):
    with pytest.raises(ValueError):
        isbn.to_isbn13(bad)


def test_to_isbn13_none_raises_type_error():
    with pytest.raises(TypeError):
        isbn.to_isbn13(None)
