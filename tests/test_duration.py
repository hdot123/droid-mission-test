"""Tests for duration.py (parse_duration and format_duration)."""

import pytest

import duration
from duration import format_duration, parse_duration


# --- body examples: parse_duration ---

def test_parse_1h30m():
    assert parse_duration("1h30m") == 5400


def test_parse_45s():
    assert parse_duration("45s") == 45


def test_parse_2d():
    assert parse_duration("2d") == 172800


# --- body examples: format_duration ---

def test_format_5400():
    assert format_duration(5400) == "1h30m"


def test_format_3661():
    assert format_duration(3661) == "1h1m1s"


def test_format_0():
    assert format_duration(0) == "0s"


# --- descending-order rule ---

def test_units_must_be_descending():
    with pytest.raises(ValueError):
        parse_duration("30m1h")
    with pytest.raises(ValueError):
        parse_duration("5s30m")
    with pytest.raises(ValueError):
        parse_duration("1s1d")


def test_descending_order_accepted():
    assert parse_duration("1d") == 86400
    assert parse_duration("1d2h") == 93600
    assert parse_duration("1d2h3m4s") == 93784
    assert parse_duration("1h1m1s") == 3661


# --- at-most-once rule ---

def test_each_unit_at_most_once():
    with pytest.raises(ValueError):
        parse_duration("1h2h")
    with pytest.raises(ValueError):
        parse_duration("1m1m")
    with pytest.raises(ValueError):
        parse_duration("1d1d")


# --- invalid format -> ValueError ---

@pytest.mark.parametrize("bad", [
    "",
    "abc",
    "1h30",     # missing unit on second part
    "h",        # missing number
    "1x",       # unknown unit
    "1h30m ",   # trailing whitespace
    " 1h",      # leading whitespace
    "1h-30m",   # negative component
    "1.5h",     # fractional number not supported
    "1",        # bare number, no unit
    "-1s",      # negative sign not part of format
])
def test_invalid_format_raises_value_error(bad):
    with pytest.raises(ValueError):
        parse_duration(bad)


def test_parse_non_string_raises_value_error():
    with pytest.raises(ValueError):
        parse_duration(None)
    with pytest.raises(ValueError):
        parse_duration(5400)


# --- format_duration: zero-valued units omitted, negatives rejected ---

def test_format_omits_zero_units():
    assert format_duration(90) == "1m30s"
    assert format_duration(3600) == "1h"
    assert format_duration(86400) == "1d"
    assert format_duration(86400 + 3600 + 60 + 1) == "1d1h1m1s"
    assert format_duration(61) == "1m1s"


def test_format_negative_raises_value_error():
    with pytest.raises(ValueError):
        format_duration(-1)
    with pytest.raises(ValueError):
        format_duration(-5400)


# --- round trip ---

def test_parse_format_round_trip():
    for text in ("1h30m", "45s", "2d", "1d2h3m4s", "0s", "1m"):
        assert format_duration(parse_duration(text)) == text
