"""Tests for bizdays (work order #730, process card bizdays)."""

from datetime import date, datetime

import pytest

from bizdays import add_business_days, business_days, is_business_day

# Anchors: 2026-01-01 is Thursday, 2026-01-05 is Monday.


class TestIsBusinessDay:
    def test_monday_is_business_day(self):
        assert is_business_day(date(2026, 1, 5)) is True

    def test_saturday_is_not(self):
        assert is_business_day(date(2026, 1, 3)) is False

    def test_sunday_is_not(self):
        assert is_business_day(date(2026, 1, 4)) is False

    def test_holiday_is_not(self):
        assert is_business_day(date(2026, 1, 1), {date(2026, 1, 1)}) is False

    def test_thursday_is_business_day(self):
        assert is_business_day(date(2026, 1, 1)) is True

    def test_datetime_rejected(self):
        with pytest.raises(TypeError):
            is_business_day(datetime(2026, 1, 5, 9, 0))


class TestBusinessDays:
    def test_half_open_range(self):
        assert business_days(date(2026, 1, 1), date(2026, 1, 6)) == 3

    def test_range_with_holiday(self):
        assert (
            business_days(date(2026, 1, 1), date(2026, 1, 6), {date(2026, 1, 1)})
            == 2
        )

    def test_reversed_range_is_negative(self):
        assert business_days(date(2026, 1, 6), date(2026, 1, 1)) == -3

    def test_empty_range(self):
        assert business_days(date(2026, 1, 5), date(2026, 1, 5)) == 0

    def test_weekend_span_is_zero(self):
        assert business_days(date(2026, 1, 3), date(2026, 1, 5)) == 0

    def test_two_weeks(self):
        assert business_days(date(2026, 1, 1), date(2026, 1, 13)) == 8

    def test_string_start_rejected(self):
        with pytest.raises(TypeError):
            business_days("2026-01-01", date(2026, 1, 6))

    def test_datetime_start_rejected(self):
        with pytest.raises(TypeError):
            business_days(datetime(2026, 1, 1, 9, 0), date(2026, 1, 6))

    def test_bad_holiday_rejected(self):
        with pytest.raises(TypeError):
            business_days(date(2026, 1, 1), date(2026, 1, 6), {"x"})


class TestAddBusinessDays:
    def test_forward_from_friday(self):
        assert add_business_days(date(2026, 1, 2), 1) == date(2026, 1, 5)

    def test_backward_from_monday(self):
        assert add_business_days(date(2026, 1, 5), -1) == date(2026, 1, 2)

    def test_forward_from_saturday_skips_weekend(self):
        assert add_business_days(date(2026, 1, 3), 1) == date(2026, 1, 5)

    def test_zero_returns_d_unchanged(self):
        assert add_business_days(date(2026, 1, 3), 0) == date(2026, 1, 3)

    def test_zero_on_weekend_non_business_day(self):
        assert add_business_days(date(2026, 1, 4), 0) == date(2026, 1, 4)

    def test_holiday_skipped(self):
        assert (
            add_business_days(date(2026, 1, 1), 1, {date(2026, 1, 2)})
            == date(2026, 1, 5)
        )

    def test_five_business_days(self):
        assert add_business_days(date(2026, 1, 1), 5) == date(2026, 1, 8)

    def test_non_int_n_rejected(self):
        with pytest.raises(TypeError):
            add_business_days(date(2026, 1, 5), 1.5)

    def test_bool_n_rejected(self):
        with pytest.raises(TypeError):
            add_business_days(date(2026, 1, 5), True)

    def test_datetime_d_rejected(self):
        with pytest.raises(TypeError):
            add_business_days(datetime(2026, 1, 5, 9, 0), 1)

    def test_bad_holiday_rejected(self):
        with pytest.raises(TypeError):
            add_business_days(date(2026, 1, 5), 1, {"x"})
