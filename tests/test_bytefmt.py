import pytest

from bytefmt import format_bytes


def test_zero_bytes():
    assert format_bytes(0) == "0 B"


def test_sub_kib_integer_bytes():
    assert format_bytes(512) == "512 B"


def test_one_point_five_kib():
    assert format_bytes(1536) == "1.5 KiB"


def test_one_point_zero_mib():
    assert format_bytes(1048576) == "1.0 MiB"


def test_one_point_five_mib():
    assert format_bytes(1536 * 1024) == "1.5 MiB"


def test_negative_raises_value_error():
    with pytest.raises(ValueError):
        format_bytes(-1)
