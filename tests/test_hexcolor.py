"""Tests for hexcolor module only."""

import pytest

from hexcolor import is_valid, parse, to_hex


def test_parse_short_form_spec_example():
    assert parse("#f80") == (255, 136, 0)


def test_parse_long_form_spec_example():
    assert parse("#FF8800") == (255, 136, 0)


def test_to_hex_spec_example():
    assert to_hex(255, 136, 0) == "#FF8800"


def test_parse_case_insensitive_long_form():
    assert parse("#ff8800") == (255, 136, 0)
    assert parse("#AbCdEf") == (171, 205, 239)


def test_parse_short_form_expands_digits():
    assert parse("#000") == (0, 0, 0)
    assert parse("#fff") == (255, 255, 255)
    assert parse("#AbC") == (170, 187, 204)


def test_parse_missing_hash_raises():
    with pytest.raises(ValueError):
        parse("f80")


def test_parse_wrong_length_raises():
    with pytest.raises(ValueError):
        parse("#ff")
    with pytest.raises(ValueError):
        parse("#ff88000")


def test_parse_non_hex_chars_raises():
    with pytest.raises(ValueError):
        parse("#gg0000")
    with pytest.raises(ValueError):
        parse("#fg0")


def test_to_hex_components_out_of_range_raise():
    with pytest.raises(ValueError):
        to_hex(-1, 0, 0)
    with pytest.raises(ValueError):
        to_hex(0, 256, 0)
    with pytest.raises(ValueError):
        to_hex(0, 0, 300)


def test_to_hex_non_int_components_raise():
    with pytest.raises(ValueError):
        to_hex("255", 0, 0)
    with pytest.raises(ValueError):
        to_hex(12.5, 0, 0)
    with pytest.raises(ValueError):
        to_hex(True, 0, 0)


def test_to_hex_bounds():
    assert to_hex(0, 0, 0) == "#000000"
    assert to_hex(255, 255, 255) == "#FFFFFF"


def test_is_valid_true_cases():
    assert is_valid("#f80") is True
    assert is_valid("#FF8800") is True


def test_is_valid_false_cases_without_raising():
    assert is_valid("f80") is False
    assert is_valid("#ff") is False
    assert is_valid("#gg0000") is False
    assert is_valid("") is False
    assert is_valid(None) is False
