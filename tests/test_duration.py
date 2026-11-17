"""Tests for duration.py (parse and format)."""

import pytest

import duration


# --- parse: given examples and unit totals ---

def test_parse_examples():
    assert duration.parse("1h30m") == 5400
    assert duration.parse("45s") == 45
    assert duration.parse("2d 3h") == 2 * 86400 + 3 * 3600


def test_parse_unit_totals():
    assert duration.parse("1d") == 86400
    assert duration.parse("1h") == 3600
    assert duration.parse("1m") == 60
    assert duration.parse("1s") == 1
    assert duration.parse("1d1h1m1s") == 86400 + 3600 + 60 + 1


def test_parse_arbitrary_order_and_spacing():
    assert duration.parse("30m1h") == 5400
    assert duration.parse("1h30m") == duration.parse("30m1h")
    assert duration.parse("2d 3h") == duration.parse("3h 2d")
    assert duration.parse("  45s  ") == 45
    assert duration.parse("1d  2h   3m 4s") == 86400 + 7200 + 180 + 4


# --- parse: error cases ---

def test_parse_duplicate_unit_raises_value_error():
    with pytest.raises(ValueError):
        duration.parse("1h1h")
    with pytest.raises(ValueError):
        duration.parse("1m 2m")
    with pytest.raises(ValueError):
        duration.parse("1d2d3d")


def test_parse_empty_string_raises_value_error():
    with pytest.raises(ValueError):
        duration.parse("")
    with pytest.raises(ValueError):
        duration.parse("   ")


def test_parse_malformed_input_raises_value_error():
    with pytest.raises(ValueError):
        duration.parse("1x")        # unknown unit
    with pytest.raises(ValueError):
        duration.parse("1h30")      # missing trailing unit
    with pytest.raises(ValueError):
        duration.parse("hm")        # missing number
    with pytest.raises(ValueError):
        duration.parse("h30m")      # leading unit with no number


def test_parse_none_raises_type_error():
    with pytest.raises(TypeError):
        duration.parse(None)


# --- format: simplest form ---

def test_format_zero():
    assert duration.format(0) == "0s"


def test_format_exact_division():
    assert duration.format(86400) == "1d"
    assert duration.format(3600) == "1h"
    assert duration.format(60) == "1m"
    assert duration.format(1) == "1s"


def test_format_composite_and_greedy():
    assert duration.format(90) == "1m30s"
    assert duration.format(5400) == "1h30m"
    assert duration.format(90061) == "1d1h1m1s"
    assert duration.format(93784) == "1d2h3m4s"


def test_format_round_trip_with_parse():
    for text in ("1h30m", "45s", "2d 3h", "1d1h1m1s", "0s"):
        seconds = duration.parse(text)
        assert duration.parse(duration.format(seconds)) == seconds


def test_format_negative_raises_value_error():
    with pytest.raises(ValueError):
        duration.format(-1)
    with pytest.raises(ValueError):
        duration.format(-60)


def test_format_none_raises_type_error():
    with pytest.raises(TypeError):
        duration.format(None)
