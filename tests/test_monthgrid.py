"""tests/test_monthgrid.py —— monthgrid 验收要点逐字覆盖。"""

import calendar

import pytest

from monthgrid import days_in_month, month_grid


# ---------------------------------------------------------------- days_in_month

def test_days_in_month_leap_and_common():
    assert days_in_month(2024, 2) == 29
    assert days_in_month(2023, 2) == 28
    assert days_in_month(2000, 2) == 29
    assert days_in_month(1900, 2) == 28
    assert days_in_month(2100, 2) == 28


def test_days_in_month_2026():
    assert days_in_month(2026, 1) == 31
    assert days_in_month(2026, 4) == 30


def test_days_in_month_matches_stdlib_monthrange():
    """全量对照口径：1999–2031 各年各月与 calendar.monthrange 一致。"""
    for year in range(1999, 2032):
        for month in range(1, 13):
            assert days_in_month(year, month) == calendar.monthrange(year, month)[1]


def test_days_in_month_invalid_month_raises():
    with pytest.raises(ValueError):
        days_in_month(2026, 13)
    with pytest.raises(ValueError):
        days_in_month(2026, 0)


# -------------------------------------------------------------------- month_grid

def test_month_grid_february_2026_monday_first():
    assert month_grid(2026, 2, 0) == [
        [None, None, None, None, None, None, 1],
        [2, 3, 4, 5, 6, 7, 8],
        [9, 10, 11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20, 21, 22],
        [23, 24, 25, 26, 27, 28, None],
    ]


def test_month_grid_february_2024_sunday_first_edges():
    assert month_grid(2024, 2, 6)[0] == [None, None, None, None, 1, 2, 3]
    assert month_grid(2024, 2, 6)[-1] == [25, 26, 27, 28, 29, None, None]


def test_month_grid_matches_stdlib_calendar():
    """全量对照口径：1999–2031 与标准库 calendar 月历逐格一致（0 填充换 None）。"""
    for year in range(1999, 2032):
        for month in range(1, 13):
            expected = [
                [day if day != 0 else None for day in row]
                for row in calendar.monthcalendar(year, month)
            ]
            assert month_grid(year, month, 0) == expected


def test_month_grid_structure_for_any_first_weekday():
    """任意 first_weekday：每行恰 7 格，展平后非 None 恰为 1..当月天数。"""
    for year in range(1999, 2032):
        for month in range(1, 13):
            ndays = days_in_month(year, month)
            for first_weekday in range(7):
                grid = month_grid(year, month, first_weekday)
                assert all(len(row) == 7 for row in grid)
                flat = [cell for row in grid for cell in row]
                non_none = [cell for cell in flat if cell is not None]
                assert non_none == list(range(1, ndays + 1))


def test_month_grid_invalid_args_raise():
    with pytest.raises(ValueError):
        month_grid(2026, 1, 7)
    with pytest.raises(ValueError):
        month_grid(2026, 1, -1)
    with pytest.raises(ValueError):
        month_grid(2026, 13, 0)
    with pytest.raises(ValueError):
        month_grid(2026, 0, 0)
