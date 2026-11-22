import pytest

from duration import format, parse


def test_parse_basic():
    assert parse("1h30m") == 5400
    assert parse("45s") == 45
    assert parse("2h") == 7200
    assert parse("1h1m1s") == 3661


def test_parse_zero_and_single_units():
    assert parse("0s") == 0
    assert parse("0h0m0s") == 0
    assert parse("30m") == 1800
    assert parse("59s") == 59


def test_format_basic():
    assert format(5400) == "1h30m"
    assert format(3661) == "1h1m1s"
    assert format(0) == "0s"
    assert format(3600) == "1h"
    assert format(45) == "45s"
    assert format(1800) == "30m"


def test_roundtrip_7325():
    assert parse(format(7325)) == 7325
    assert format(7325) == "2h2m5s"


def test_roundtrip_values():
    for total in (0, 1, 59, 60, 61, 3599, 3600, 3661, 5400, 7325, 86399):
        assert parse(format(total)) == total


def test_parse_order_reversed():
    with pytest.raises(ValueError):
        parse("30m1h")


def test_parse_unknown_unit():
    with pytest.raises(ValueError):
        parse("1x")


def test_parse_empty():
    with pytest.raises(ValueError):
        parse("")


def test_parse_duplicate_unit():
    with pytest.raises(ValueError):
        parse("1h2h")
    with pytest.raises(ValueError):
        parse("10s30s")


def test_parse_digits_without_unit():
    with pytest.raises(ValueError):
        parse("45")


def test_parse_trailing_or_embedded_garbage():
    with pytest.raises(ValueError):
        parse("1h30m ")
    with pytest.raises(ValueError):
        parse("1h 30m")
    with pytest.raises(ValueError):
        parse("h")


def test_format_negative():
    with pytest.raises(ValueError):
        format(-1)
