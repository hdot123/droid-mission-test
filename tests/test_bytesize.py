import pytest

from bytesize import format, parse


def test_format_zero_and_sub_kib():
    assert format(0) == "0 B"
    assert format(1023) == "1023 B"


def test_format_kib():
    assert format(1024) == "1.0 KiB"
    assert format(1536) == "1.5 KiB"


def test_format_mib():
    assert format(1048576) == "1.0 MiB"
    assert format(1234567) == "1.2 MiB"


def test_format_gib():
    assert format(1073741824) == "1.0 GiB"


def test_format_tib():
    assert format(1099511627776) == "1.0 TiB"


def test_parse_basic():
    assert parse("0 B") == 0
    assert parse("512 B") == 512


def test_parse_fractional_and_integer_scaled():
    assert parse("1.5 KiB") == 1536
    assert parse("2 KiB") == 2048
    assert parse("1.0 MiB") == 1048576


def test_format_negative_raises():
    with pytest.raises(ValueError):
        format(-1)


def test_parse_invalid_forms_raise():
    with pytest.raises(ValueError):
        parse("1.5KiB")
    with pytest.raises(ValueError):
        parse("1.5 KB")


def test_roundtrip_1536():
    n = 1536
    assert parse(format(n)) == n
