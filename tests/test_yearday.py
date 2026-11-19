"""Tests for yearday: 年内日序号互转（第四十六轮 · A 单）。"""

import pytest

from yearday import from_yearday, to_yearday


# --- 验收要点 1–8: to_yearday 基本值 ---

def test_to_yearday_mar1_leap():
    assert to_yearday(2024, 3, 1) == 61


def test_to_yearday_mar1_common():
    assert to_yearday(2023, 3, 1) == 60


def test_to_yearday_dec31_leap():
    assert to_yearday(2024, 12, 31) == 366


def test_to_yearday_dec31_common():
    assert to_yearday(2023, 12, 31) == 365


def test_to_yearday_2000_feb29():
    assert to_yearday(2000, 2, 29) == 60


def test_to_yearday_1900_mar1_not_leap():
    assert to_yearday(1900, 3, 1) == 60


def test_to_yearday_jan1():
    assert to_yearday(2024, 1, 1) == 1


def test_to_yearday_2024_feb29():
    assert to_yearday(2024, 2, 29) == 60


# --- 验收要点 9–14: from_yearday 基本值 ---

def test_from_yearday_2024_60():
    assert from_yearday(2024, 60) == (2, 29)


def test_from_yearday_2023_60():
    assert from_yearday(2023, 60) == (3, 1)


def test_from_yearday_2024_366():
    assert from_yearday(2024, 366) == (12, 31)


def test_from_yearday_2023_365():
    assert from_yearday(2023, 365) == (12, 31)


def test_from_yearday_2000_60():
    assert from_yearday(2000, 60) == (2, 29)


def test_from_yearday_1900_60():
    assert from_yearday(1900, 60) == (3, 1)


# --- 验收要点 15: 往返 ---

@pytest.mark.parametrize(
    "y, m, d",
    [
        (2024, 5, 17),
        (2023, 11, 30),
        (2000, 2, 29),
        (1900, 7, 4),
        (2026, 1, 1),
    ],
)
def test_round_trip(y, m, d):
    assert from_yearday(y, to_yearday(y, m, d)) == (m, d)


# --- 验收要点 16: to_yearday ValueError ---

def test_to_yearday_feb29_common_year():
    with pytest.raises(ValueError):
        to_yearday(2023, 2, 29)


def test_to_yearday_month_13():
    with pytest.raises(ValueError):
        to_yearday(2024, 13, 1)


def test_to_yearday_day_31_april():
    with pytest.raises(ValueError):
        to_yearday(2024, 4, 31)


def test_to_yearday_month_0():
    with pytest.raises(ValueError):
        to_yearday(2024, 0, 10)


# --- 验收要点 17: from_yearday ValueError ---

def test_from_yearday_2023_366():
    with pytest.raises(ValueError):
        from_yearday(2023, 366)


def test_from_yearday_2024_0():
    with pytest.raises(ValueError):
        from_yearday(2024, 0)


def test_from_yearday_2024_367():
    with pytest.raises(ValueError):
        from_yearday(2024, 367)


# --- 验收要点 18: to_yearday TypeError ---

def test_to_yearday_year_str():
    with pytest.raises(TypeError):
        to_yearday("2024", 1, 1)


def test_to_yearday_year_float():
    with pytest.raises(TypeError):
        to_yearday(2024.0, 1, 1)


def test_to_yearday_year_bool():
    with pytest.raises(TypeError):
        to_yearday(True, 1, 1)


# --- 其他类型错误（按规范补测） ---

def test_to_yearday_month_str():
    with pytest.raises(TypeError):
        to_yearday(2024, "1", 1)


def test_to_yearday_day_float():
    with pytest.raises(TypeError):
        to_yearday(2024, 1, 1.5)


def test_from_yearday_year_str():
    with pytest.raises(TypeError):
        from_yearday("2024", 1)


def test_from_yearday_year_float():
    with pytest.raises(TypeError):
        from_yearday(2024.0, 1)


def test_from_yearday_year_bool():
    with pytest.raises(TypeError):
        from_yearday(True, 1)


def test_from_yearday_n_str():
    with pytest.raises(TypeError):
        from_yearday(2024, "60")


def test_from_yearday_n_float():
    with pytest.raises(TypeError):
        from_yearday(2024, 60.0)


def test_from_yearday_n_bool():
    with pytest.raises(TypeError):
        from_yearday(2024, True)


# --- year < 1 按规范 ---

def test_to_yearday_year_zero():
    with pytest.raises(ValueError):
        to_yearday(0, 1, 1)


def test_to_yearday_year_negative():
    with pytest.raises(ValueError):
        to_yearday(-5, 1, 1)


def test_from_yearday_year_zero():
    with pytest.raises(ValueError):
        from_yearday(0, 1)


def test_from_yearday_year_negative():
    with pytest.raises(ValueError):
        from_yearday(-5, 1)
