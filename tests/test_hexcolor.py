"""Tests for hexcolor module only."""

import pytest

from hexcolor import is_valid, parse, to_hex


def test_parse_short_form_example():
    assert parse("#f80") == (255, 136, 0)


def test_parse_long_form_example():
    assert parse("#FF8800") == (255, 136, 0)


def test_to_hex_example():
    assert to_hex(255, 136, 0) == "#FF8800"


def test_parse_case_insensitive_long():
    assert parse("#ff8800") == (255, 136, 0)
    assert parse("#Ff8800") == (255, 136, 0)


def test_parse_case_insensitive_short():
    assert parse("#F80") == (255, 136, 0)


def test_parse_short_doubling():
    assert parse("#000") == (0, 0, 0)
    assert parse("#fff") == (255, 255, 255)
    assert parse("#123") == (17, 34, 51)


def test_parse_missing_hash_raises():
    with pytest.raises(ValueError):
        parse("f80")


def test_parse_wrong_length_raises():
    with pytest.raises(ValueError):
        parse("#ff88")
    with pytest.raises(ValueError):
        parse("#ff88000")
    with pytest.raises(ValueError):
        parse("#")


def test_parse_non_hex_chars_raises():
    with pytest.raises(ValueError):
        parse("#xyz")
    with pytest.raises(ValueError):
        parse("#gg0000")
    with pytest.raises(ValueError):
        parse("#f8g")


def test_to_hex_roundtrip():
    assert to_hex(0, 0, 0) == "#000000"
    assert to_hex(255, 255, 255) == "#FFFFFF"
    assert to_hex(*parse("#f80")) == "#FF8800"


def test_to_hex_invalid_range_raises():
    with pytest.raises(ValueError):
        to_hex(256, 0, 0)
    with pytest.raises(ValueError):
        to_hex(0, -1, 0)
    with pytest.raises(ValueError):
        to_hex(0, 0, 300)


def test_to_hex_invalid_type_raises():
    with pytest.raises(ValueError):
        to_hex("255", 0, 0)
    with pytest.raises(ValueError):
        to_hex(1.0, 0, 0)
    with pytest.raises(ValueError):
        to_hex(True, 0, 0)


def test_is_valid_true():
    assert is_valid("#f80") is True
    assert is_valid("#FF8800") is True
    assert is_valid("#000") is True


def test_is_valid_false_never_raises():
    assert is_valid("f80") is False
    assert is_valid("#ff88") is False
    assert is_valid("#xyz") is False
    assert is_valid("") is False
    assert is_valid(None) is False
    assert is_valid(123) is False
