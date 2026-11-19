"""Tests for bizdays: business-day counting and stepping.

Every acceptance point from the work order has a dedicated test case.
Spec anchors: 2026-01-01 is a Thursday, 2026-01-05 is a Monday.
"""

from datetime import date, datetime

import pytest

from bizdays import add_business_days, business_days, is_business_day


def test_anchor_days_of_week():
    assert date(2026, 1, 1).weekday() == 3  # Thursday
    assert date(2026, 1, 5).weekday() == 0  # Monday


def test_is_business_day_monday():
    assert is_business_day(date(2026, 1, 5)) is True


def test_is_business_day_saturday():
    assert is_business_day(date(2026, 1, 3)) is False


def test_is_business_day_sunday():
    assert is_business_day(date(2026, 1, 4)) is False


def test_is_business_day_holiday():
    assert is_business_day(date(2026, 1, 1), {date(2026, 1, 1)}) is False


def test_is_business_day_accepts_iterable_holidays():
    assert is_business_day(date(2026, 1, 1), [date(2026, 1, 1)]) is False


def test_business_days_forward():
    assert business_days(date(2026, 1, 1), date(2026, 1, 6)) == 3


def test_business_days_with_holiday():
    assert (
        business_days(date(2026, 1, 1), date(2026, 1, 6), {date(2026, 1, 1)})
        == 2
    )


def test_business_days_reversed_is_negated():
    assert business_days(date(2026, 1, 6), date(2026, 1, 1)) == -3


def test_business_days_same_day_is_zero():
    assert business_days(date(2026, 1, 5), date(2026, 1, 5)) == 0


def test_business_days_weekend_only_interval_is_zero():
    assert business_days(date(2026, 1, 3), date(2026, 1, 5)) == 0


def test_business_days_two_calendar_weeks():
    assert business_days(date(2026, 1, 1), date(2026, 1, 13)) == 8


def test_business_days_returns_int():
    assert type(business_days(date(2026, 1, 1), date(2026, 1, 6))) is int


def test_add_business_days_forward():
    assert add_business_days(date(2026, 1, 2), 1) == date(2026, 1, 5)


def test_add_business_days_backward():
    assert add_business_days(date(2026, 1, 5), -1) == date(2026, 1, 2)


def test_add_business_days_from_weekend():
    assert add_business_days(date(2026, 1, 3), 1) == date(2026, 1, 5)


def test_add_business_days_zero_returns_same_day_even_if_weekend():
    result = add_business_days(date(2026, 1, 3), 0)
    assert result == date(2026, 1, 3)
    assert type(result) is date


def test_add_business_days_skips_holiday():
    assert (
        add_business_days(date(2026, 1, 1), 1, {date(2026, 1, 2)})
        == date(2026, 1, 5)
    )


def test_add_business_days_five():
    assert add_business_days(date(2026, 1, 1), 5) == date(2026, 1, 8)


def test_add_business_days_returns_date():
    assert type(add_business_days(date(2026, 1, 2), 1)) is date


def test_business_days_rejects_string_start():
    with pytest.raises(TypeError):
        business_days("2026-01-01", date(2026, 1, 6))


def test_is_business_day_rejects_datetime():
    with pytest.raises(TypeError):
        is_business_day(datetime(2026, 1, 5, 9, 0))


def test_add_business_days_rejects_float_n():
    with pytest.raises(TypeError):
        add_business_days(date(2026, 1, 5), 1.5)


def test_business_days_rejects_non_date_holiday():
    with pytest.raises(TypeError):
        business_days(date(2026, 1, 1), date(2026, 1, 6), {"x"})


def test_add_business_days_rejects_bool_n():
    with pytest.raises(TypeError):
        add_business_days(date(2026, 1, 5), True)


def test_holiday_element_rejects_datetime():
    with pytest.raises(TypeError):
        is_business_day(date(2026, 1, 5), {datetime(2026, 1, 5, 9, 0)})


def test_add_business_days_rejects_non_date_d():
    with pytest.raises(TypeError):
        add_business_days("2026-01-05", 1)
