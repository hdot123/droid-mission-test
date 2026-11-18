"""Tests for duration_parse: parse_duration and format_duration."""

import pytest

from duration_parse import format_duration, parse_duration


# --- parse_duration: worked examples ---

def test_parse_1h30m():
    assert parse_duration("1h30m") == 5400


def test_parse_45s():
    assert parse_duration("45s") == 45


def test_parse_2d_3h_with_space():
    assert parse_duration("2d 3h") == 183600


# --- parse_duration: other valid inputs ---

def test_parse_zero():
    assert parse_duration("0s") == 0
    assert parse_duration("0d0h0m0s") == 0


def test_parse_single_units():
    assert parse_duration("1d") == 86400
    assert parse_duration("1h") == 3600
    assert parse_duration("1m") == 60
    assert parse_duration("1s") == 1


def test_parse_leading_and_trailing_spaces():
    assert parse_duration("  1h  ") == 3600
    assert parse_duration("   2d 3h   ") == 183600


def test_parse_all_units_with_spaces():
    assert parse_duration("1d 2h 3m 4s") == 93784


def test_parse_multi_digit_numbers():
    assert parse_duration("10h20m") == 37200


def test_parse_roundtrip_with_format():
    assert parse_duration(format_duration(183600)) == 183600
    assert parse_duration(format_duration(5400)) == 5400


# --- parse_duration: error cases ---

def test_parse_empty_string_raises():
    with pytest.raises(ValueError):
        parse_duration("")


def test_parse_whitespace_only_raises():
    with pytest.raises(ValueError):
        parse_duration("   ")


def test_parse_pure_digits_no_unit_raises():
    with pytest.raises(ValueError):
        parse_duration("45")


def test_parse_repeated_unit_raises():
    with pytest.raises(ValueError):
        parse_duration("1h2h")
    with pytest.raises(ValueError):
        parse_duration("2h 1h")
    with pytest.raises(ValueError):
        parse_duration("1d1d")


def test_parse_unknown_unit_raises():
    with pytest.raises(ValueError):
        parse_duration("1x")
    with pytest.raises(ValueError):
        parse_duration("1hour")


def test_parse_decimal_raises():
    with pytest.raises(ValueError):
        parse_duration("1.5h")


def test_parse_negative_sign_raises():
    with pytest.raises(ValueError):
        parse_duration("-1h")


def test_parse_missing_unit_segment_raises():
    with pytest.raises(ValueError):
        parse_duration("1h5")
    with pytest.raises(ValueError):
        parse_duration("5 1h")


def test_parse_unit_before_number_raises():
    with pytest.raises(ValueError):
        parse_duration("h1")


# --- format_duration: worked examples ---

def test_format_5400():
    assert format_duration(5400) == "1h30m"


def test_format_183600():
    assert format_duration(183600) == "2d3h"


def test_format_zero():
    assert format_duration(0) == "0s"


def test_format_roundtrip():
    assert parse_duration(format_duration(183600)) == 183600


# --- format_duration: other valid inputs ---

def test_format_single_units():
    assert format_duration(45) == "45s"
    assert format_duration(60) == "1m"
    assert format_duration(3600) == "1h"
    assert format_duration(86400) == "1d"


def test_format_omits_zero_units():
    assert format_duration(90) == "1m30s"
    assert format_duration(3660) == "1h1m"
    assert format_duration(90061) == "1d1h1m1s"


def test_format_large_value():
    assert format_duration(172800) == "2d"


# --- format_duration: error cases ---

def test_format_negative_raises():
    with pytest.raises(ValueError):
        format_duration(-1)
    with pytest.raises(ValueError):
        format_duration(-5400)
