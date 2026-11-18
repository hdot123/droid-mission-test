"""Tests for monthshift: month and date shifting along the timeline."""

import pytest

from monthshift import add_months, add_months_to_date


class TestAddMonths:
    def test_positive_delta_across_year(self):
        assert add_months(2026, 11, 3) == (2027, 2)

    def test_negative_delta(self):
        assert add_months(2026, 1, -2) == (2025, 11)

    def test_year_rollover_forward(self):
        assert add_months(2026, 12, 1) == (2027, 1)

    def test_zero_delta(self):
        assert add_months(2026, 7, 0) == (2026, 7)

    def test_same_year_shift(self):
        assert add_months(2026, 3, 4) == (2026, 7)

    def test_large_negative_delta(self):
        assert add_months(2026, 6, -24) == (2024, 6)

    def test_invalid_month_zero(self):
        with pytest.raises(ValueError):
            add_months(2026, 0, 1)

    def test_invalid_month_too_large(self):
        with pytest.raises(ValueError):
            add_months(2026, 13, 1)

    def test_invalid_month_negative(self):
        with pytest.raises(ValueError):
            add_months(2026, -1, 1)

    def test_shifted_year_below_one(self):
        with pytest.raises(ValueError):
            add_months(1, 1, -1)

    def test_shifted_year_below_one_large_negative(self):
        with pytest.raises(ValueError):
            add_months(1, 12, -24)


class TestAddMonthsToDate:
    def test_clamp_jan31_to_february_common_year(self):
        assert add_months_to_date(2026, 1, 31, 1) == (2026, 2, 28)

    def test_clamp_jan31_to_february_leap_year(self):
        assert add_months_to_date(2024, 1, 31, 1) == (2024, 2, 29)

    def test_negative_delta_clamps_to_february(self):
        assert add_months_to_date(2026, 3, 31, -1) == (2026, 2, 28)

    def test_no_clamp_needed(self):
        assert add_months_to_date(2026, 5, 15, 2) == (2026, 7, 15)

    def test_day_preserved_across_year(self):
        assert add_months_to_date(2026, 12, 31, 1) == (2027, 1, 31)

    def test_zero_delta(self):
        assert add_months_to_date(2026, 1, 31, 0) == (2026, 1, 31)

    def test_clamp_apr30_to_february(self):
        assert add_months_to_date(2026, 4, 30, -2) == (2026, 2, 28)

    def test_invalid_month(self):
        with pytest.raises(ValueError):
            add_months_to_date(2026, 13, 1, 1)

    def test_invalid_day_zero(self):
        with pytest.raises(ValueError):
            add_months_to_date(2026, 1, 0, 1)

    def test_day_too_large_for_month(self):
        with pytest.raises(ValueError):
            add_months_to_date(2026, 2, 30, 1)

    def test_non_leap_february_29(self):
        with pytest.raises(ValueError):
            add_months_to_date(2026, 2, 29, 1)

    def test_leap_february_29_valid(self):
        assert add_months_to_date(2024, 2, 29, 12) == (2025, 2, 28)

    def test_shifted_year_below_one(self):
        with pytest.raises(ValueError):
            add_months_to_date(1, 1, 1, -1)
