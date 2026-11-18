"""hmsconv 的验收测试。"""

import pytest

from hmsconv import join_seconds, split_seconds


def test_split_3661():
    assert split_seconds(3661) == (1, 1, 1)


def test_split_zero():
    assert split_seconds(0) == (0, 0, 0)


def test_split_86399():
    assert split_seconds(86399) == (23, 59, 59)


def test_split_90061_hours_uncapped():
    assert split_seconds(90061) == (25, 1, 1)


def test_split_negative_raises():
    with pytest.raises(ValueError):
        split_seconds(-1)


def test_join_1_1_1():
    assert join_seconds(1, 1, 1) == 3661


def test_join_m_60_raises():
    with pytest.raises(ValueError):
        join_seconds(0, 60, 0)


def test_join_s_60_raises():
    with pytest.raises(ValueError):
        join_seconds(0, 0, 60)


def test_join_negative_raises():
    with pytest.raises(ValueError):
        join_seconds(-1, 0, 0)
    with pytest.raises(ValueError):
        join_seconds(0, -1, 0)
    with pytest.raises(ValueError):
        join_seconds(0, 0, -1)


@pytest.mark.parametrize("total", [0, 59, 3600, 90061])
def test_roundtrip_identity(total):
    assert join_seconds(*split_seconds(total)) == total
