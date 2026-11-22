from datetime import date, datetime

import pytest

from bizdays import add_business_days, business_days, is_business_day


def test_is_business_day_weekday_and_weekend():
    assert is_business_day(date(2026, 1, 5)) is True
    assert is_business_day(date(2026, 1, 3)) is False  # Saturday
    assert is_business_day(date(2026, 1, 4)) is False  # Sunday


def test_is_business_day_holiday():
    assert is_business_day(date(2026, 1, 1), {date(2026, 1, 1)}) is False


def test_is_business_day_holidays_default_empty():
    assert is_business_day(date(2026, 1, 1)) is True


def test_business_days_forward():
    assert business_days(date(2026, 1, 1), date(2026, 1, 6)) == 3


def test_business_days_with_holiday():
    assert business_days(date(2026, 1, 1), date(2026, 1, 6), {date(2026, 1, 1)}) == 2


def test_business_days_reversed_is_negative():
    assert business_days(date(2026, 1, 6), date(2026, 1, 1)) == -3


def test_business_days_empty_interval():
    assert business_days(date(2026, 1, 5), date(2026, 1, 5)) == 0


def test_business_days_weekend_only_interval_is_zero():
    assert business_days(date(2026, 1, 3), date(2026, 1, 5)) == 0


def test_business_days_longer_span():
    assert business_days(date(2026, 1, 1), date(2026, 1, 13)) == 8


def test_add_business_days_forward_from_friday():
    assert add_business_days(date(2026, 1, 2), 1) == date(2026, 1, 5)


def test_add_business_days_backward_from_monday():
    assert add_business_days(date(2026, 1, 5), -1) == date(2026, 1, 2)


def test_add_business_days_starting_on_weekend():
    assert add_business_days(date(2026, 1, 3), 1) == date(2026, 1, 5)


def test_add_business_days_zero_returns_input_unchanged():
    assert add_business_days(date(2026, 1, 3), 0) == date(2026, 1, 3)
    weekend = date(2026, 1, 3)
    result = add_business_days(weekend, 0)
    assert result == weekend
    assert result is weekend


def test_add_business_days_skips_holiday():
    assert add_business_days(date(2026, 1, 1), 1, {date(2026, 1, 2)}) == date(2026, 1, 5)


def test_add_business_days_five_forward():
    assert add_business_days(date(2026, 1, 1), 5) == date(2026, 1, 8)


def test_business_days_rejects_non_date_start():
    with pytest.raises(TypeError):
        business_days("2026-01-01", date(2026, 1, 6))


def test_is_business_day_rejects_datetime():
    with pytest.raises(TypeError):
        is_business_day(datetime(2026, 1, 5, 9, 0))


def test_add_business_days_rejects_non_int_n():
    with pytest.raises(TypeError):
        add_business_days(date(2026, 1, 5), 1.5)


def test_business_days_rejects_non_date_holidays():
    with pytest.raises(TypeError):
        business_days(date(2026, 1, 1), date(2026, 1, 6), {"x"})


def test_business_days_rejects_non_date_end():
    with pytest.raises(TypeError):
        business_days(date(2026, 1, 1), "2026-01-06")


def test_is_business_day_rejects_non_date():
    with pytest.raises(TypeError):
        is_business_day("2026-01-05")


def test_add_business_days_rejects_non_date():
    with pytest.raises(TypeError):
        add_business_days("2026-01-05", 1)


def test_add_business_days_rejects_bool_n():
    with pytest.raises(TypeError):
        add_business_days(date(2026, 1, 5), True)


def test_rejects_bool_as_date():
    with pytest.raises(TypeError):
        is_business_day(True)
    with pytest.raises(TypeError):
        business_days(True, date(2026, 1, 6))


def test_rejects_holiday_iterable_of_non_dates():
    with pytest.raises(TypeError):
        is_business_day(date(2026, 1, 5), ["2026-01-01"])
    with pytest.raises(TypeError):
        add_business_days(date(2026, 1, 5), 1, {datetime(2026, 1, 1, 9, 0)})


def test_rejects_non_iterable_holidays():
    with pytest.raises(TypeError):
        business_days(date(2026, 1, 1), date(2026, 1, 6), 5)


def test_anchor_days():
    assert date(2026, 1, 1).weekday() == 3  # Thursday
    assert date(2026, 1, 5).weekday() == 0  # Monday


def test_business_days_tuple_and_frozenset_holidays_accepted():
    assert business_days(date(2026, 1, 1), date(2026, 1, 6), (date(2026, 1, 1),)) == 2
    assert (
        business_days(date(2026, 1, 1), date(2026, 1, 6), frozenset({date(2026, 1, 1)}))
        == 2
    )


def test_add_business_days_large_negative_and_positive():
    assert add_business_days(date(2026, 1, 8), -5) == date(2026, 1, 1)
    assert add_business_days(date(2026, 1, 1), 0) == date(2026, 1, 1)
    # Round trip: forward then backward returns the original date.
    assert add_business_days(add_business_days(date(2026, 1, 1), 7), -7) == date(2026, 1, 1)


def test_business_days_holiday_on_weekend_not_counted_twice():
    # 2026-01-03 is Saturday: excluding it must not change the count.
    assert business_days(date(2026, 1, 1), date(2026, 1, 6), {date(2026, 1, 3)}) == 3


def test_business_days_multiple_holidays():
    assert (
        business_days(
            date(2026, 1, 1),
            date(2026, 1, 6),
            {date(2026, 1, 1), date(2026, 1, 2), date(2026, 1, 5)},
        )
        == 0
    )
