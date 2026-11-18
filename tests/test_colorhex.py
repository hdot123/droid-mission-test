import pytest

from colorhex import format, parse


def test_parse_six_digit():
    assert parse("#FF8000") == (255, 128, 0)
    assert parse("#000000") == (0, 0, 0)
    assert parse("#123456") == (18, 52, 86)


def test_parse_three_digit():
    assert parse("#f80") == (255, 136, 0)
    assert parse("#fff") == (255, 255, 255)


def test_format():
    assert format(255, 128, 0) == "#FF8000"
    assert format(0, 0, 0) == "#000000"
    assert format(18, 52, 86) == "#123456"


def test_parse_invalid():
    for bad in ("FF8000", "#FF80", "", "#", "#GGGGGG", "#12 456", "#ff800g"):
        with pytest.raises(ValueError):
            parse(bad)


def test_format_invalid_channel():
    with pytest.raises(ValueError):
        format(256, 0, 0)
    with pytest.raises(ValueError):
        format(0, -1, 0)
    with pytest.raises(ValueError):
        format(0, 0, 300)


def test_roundtrip():
    assert parse(format(18, 52, 86)) == (18, 52, 86)
    for triple in ((255, 128, 0), (0, 0, 0), (255, 255, 255), (18, 52, 86)):
        assert parse(format(*triple)) == triple
