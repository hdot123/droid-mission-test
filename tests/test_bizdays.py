"""tests/test_bizdays.py —— bizdays 模块验收测试。"""

from datetime import date, datetime

import pytest

from bizdays import add_business_days, business_days, is_business_day


class TestIsBusinessDay:
    def test_monday_is_business_day(self):
        assert is_business_day(date(2026, 1, 5)) is True

    def test_saturday_is_not_business_day(self):
        assert is_business_day(date(2026, 1, 3)) is False

    def test_sunday_is_not_business_day(self):
        assert is_business_day(date(2026, 1, 4)) is False

    def test_holiday_is_not_business_day(self):
        assert is_business_day(date(2026, 1, 1), {date(2026, 1, 1)}) is False


class TestBusinessDays:
    def test_half_open_interval(self):
        assert business_days(date(2026, 1, 1), date(2026, 1, 6)) == 3

    def test_holiday_excluded(self):
        assert (
            business_days(date(2026, 1, 1), date(2026, 1, 6), {date(2026, 1, 1)})
            == 2
        )

    def test_reversed_interval_is_negative(self):
        assert business_days(date(2026, 1, 6), date(2026, 1, 1)) == -3

    def test_equal_bounds_zero(self):
        assert business_days(date(2026, 1, 5), date(2026, 1, 5)) == 0

    def test_weekend_only_span_zero(self):
        assert business_days(date(2026, 1, 3), date(2026, 1, 5)) == 0

    def test_two_week_span(self):
        assert business_days(date(2026, 1, 1), date(2026, 1, 13)) == 8


class TestAddBusinessDays:
    def test_forward_across_weekend(self):
        assert add_business_days(date(2026, 1, 2), 1) == date(2026, 1, 5)

    def test_backward(self):
        assert add_business_days(date(2026, 1, 5), -1) == date(2026, 1, 2)

    def test_start_on_weekend_steps_to_monday(self):
        assert add_business_days(date(2026, 1, 3), 1) == date(2026, 1, 5)

    def test_zero_returns_input_even_if_not_business_day(self):
        assert add_business_days(date(2026, 1, 3), 0) == date(2026, 1, 3)

    def test_holiday_skipped(self):
        assert (
            add_business_days(date(2026, 1, 1), 1, {date(2026, 1, 2)})
            == date(2026, 1, 5)
        )

    def test_five_business_days(self):
        assert add_business_days(date(2026, 1, 1), 5) == date(2026, 1, 8)


class TestTypeErrors:
    def test_business_days_rejects_non_date_start(self):
        with pytest.raises(TypeError):
            business_days("2026-01-01", date(2026, 1, 6))

    def test_is_business_day_rejects_datetime(self):
        with pytest.raises(TypeError):
            is_business_day(datetime(2026, 1, 5, 9, 0))

    def test_add_business_days_rejects_non_int_n(self):
        with pytest.raises(TypeError):
            add_business_days(date(2026, 1, 5), 1.5)

    def test_business_days_rejects_bad_holiday_element(self):
        with pytest.raises(TypeError):
            business_days(date(2026, 1, 1), date(2026, 1, 6), {"x"})

    def test_add_business_days_rejects_bool_n(self):
        with pytest.raises(TypeError):
            add_business_days(date(2026, 1, 5), True)

    def test_is_business_day_rejects_bad_holiday_element(self):
        with pytest.raises(TypeError):
            is_business_day(date(2026, 1, 5), {"x"})
