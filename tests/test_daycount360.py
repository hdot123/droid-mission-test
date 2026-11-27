from datetime import date

import pytest

from daycount360 import days360


def test_half_year_span():
    assert days360(date(2024, 1, 15), date(2024, 7, 15)) == 180


def test_start_and_end_day_31():
    assert days360(date(2024, 1, 31), date(2024, 3, 31)) == 60


def test_start_day_30_end_day_31():
    assert days360(date(2024, 1, 30), date(2024, 3, 31)) == 60


def test_start_day_15_end_day_31():
    assert days360(date(2024, 1, 15), date(2024, 3, 31)) == 76


def test_common_year_february_end_triggers_rule_one():
    # 平年 2 月末触发规则①
    assert days360(date(2023, 2, 28), date(2023, 8, 28)) == 178


def test_leap_year_february_end_triggers_rule_one():
    # 闰年 2 月末触发规则①
    assert days360(date(2024, 2, 29), date(2024, 8, 29)) == 179


def test_both_ends_february_end_rules_one_and_two():
    # 两端同为 2 月末，规则①②齐触发
    assert days360(date(2023, 2, 28), date(2024, 2, 29)) == 360


def test_year_boundary_month_31():
    assert days360(date(2024, 12, 31), date(2025, 1, 31)) == 30


def test_same_day_is_zero():
    assert days360(date(2024, 3, 15), date(2024, 3, 15)) == 0


def test_full_year_june_30():
    assert days360(date(2020, 6, 30), date(2021, 6, 30)) == 360


def test_end_before_start_raises_value_error():
    with pytest.raises(ValueError):
        days360(date(2024, 7, 15), date(2024, 1, 15))


def test_string_start_raises_type_error():
    with pytest.raises(TypeError):
        days360("2024-01-15", date(2024, 7, 15))


def test_none_end_raises_type_error():
    with pytest.raises(TypeError):
        days360(date(2024, 1, 15), None)
