import pytest

from weekday import is_leap_year, weekday


def test_is_leap_year_examples():
    assert is_leap_year(2000) is True
    assert is_leap_year(1900) is False
    assert is_leap_year(2024) is True
    assert is_leap_year(2026) is False


def test_is_leap_year_general_rule():
    assert is_leap_year(4) is True
    assert is_leap_year(100) is False
    assert is_leap_year(400) is True
    assert is_leap_year(1) is False
    assert is_leap_year(2100) is False
    assert is_leap_year(2400) is True


def test_weekday_examples():
    assert weekday(1, 1, 1) == 0
    assert weekday(2000, 1, 1) == 5
    assert weekday(2024, 2, 29) == 3
    assert weekday(2026, 11, 18) == 2


def test_weekday_known_dates():
    # 1970-01-01 was a Thursday (weekday 3).
    assert weekday(1970, 1, 1) == 3
    # 2000-01-01 was a Saturday (weekday 5).
    assert weekday(2000, 1, 1) == 5
    # 1899-12-31 was a Sunday (weekday 6).
    assert weekday(1899, 12, 31) == 6


def test_weekday_invalid_year():
    with pytest.raises(ValueError):
        weekday(0, 1, 1)
    with pytest.raises(ValueError):
        weekday(-5, 1, 1)


def test_weekday_invalid_month():
    with pytest.raises(ValueError):
        weekday(2026, 0, 1)
    with pytest.raises(ValueError):
        weekday(2026, 13, 1)


def test_weekday_invalid_day():
    with pytest.raises(ValueError):
        weekday(2026, 1, 0)
    with pytest.raises(ValueError):
        weekday(2026, 1, 32)
    with pytest.raises(ValueError):
        weekday(2026, 2, 30)
    # Feb 29 in a non-leap year is invalid.
    with pytest.raises(ValueError):
        weekday(2026, 2, 29)
    with pytest.raises(ValueError):
        weekday(1900, 2, 29)
    with pytest.raises(ValueError):
        weekday(2026, 4, 31)
