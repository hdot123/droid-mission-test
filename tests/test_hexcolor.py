"""Tests for the hexcolor module."""

import pytest

from hexcolor import parse, to_hex, is_valid


def test_parse_short_form():
    assert parse("#f80") == (255, 136, 0)


def test_parse_long_form():
    assert parse("#FF8800") == (255, 136, 0)


def test_to_hex_example():
    assert to_hex(255, 136, 0) == "#FF8800"


def test_parse_case_insensitive():
    assert parse("#ABCDEF") == parse("#abcdef")
    assert parse("#FfAa00") == (255, 170, 0)


def test_parse_short_form_doubles_digits():
    assert parse("#fff") == (255, 255, 255)
    assert parse("#000") == (0, 0, 0)


def test_parse_invalid_missing_hash():
    with pytest.raises(ValueError):
        parse("f80")


def test_parse_invalid_length():
    with pytest.raises(ValueError):
        parse("#ff")
    with pytest.raises(ValueError):
        parse("#ff880")


def test_parse_invalid_characters():
    with pytest.raises(ValueError):
        parse("#gg0000")
    with pytest.raises(ValueError):
        parse("#xyz")


def test_to_hex_components_out_of_range():
    with pytest.raises(ValueError):
        to_hex(256, 0, 0)
    with pytest.raises(ValueError):
        to_hex(0, -1, 0)


def test_to_hex_component_must_be_int():
    with pytest.raises(ValueError):
        to_hex(1.5, 0, 0)
    with pytest.raises(ValueError):
        to_hex("0", 0, 0)


def test_to_hex_roundtrip():
    assert parse(to_hex(1, 2, 3)) == (1, 2, 3)
    assert parse(to_hex(255, 136, 0)) == (255, 136, 0)


def test_is_valid_boolean():
    assert is_valid("#f80") is True
    assert is_valid("#FF8800") is True
    assert is_valid("f80") is False
    assert is_valid("#gg0000") is False
    assert is_valid("#ff") is False
