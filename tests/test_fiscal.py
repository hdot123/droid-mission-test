from datetime import date

import pytest

from fiscal import fiscal_label, fiscal_quarter, fiscal_start, fiscal_year


# --- fiscal_year with start_month=4 ---

def test_year_start_month_4_may():
    assert fiscal_year(date(2026, 5, 1), 4) == 2027


def test_year_start_month_4_january():
    assert fiscal_year(date(2026, 1, 15), 4) == 2026


def test_year_start_month_4_april_1():
    assert fiscal_year(date(2025, 4, 1), 4) == 2026


def test_year_start_month_4_march_31():
    assert fiscal_year(date(2026, 3, 31), 4) == 2026


# --- fiscal_quarter with start_month=4 ---

def test_quarter_start_month_4_may():
    assert fiscal_quarter(date(2026, 5, 1), 4) == 1


def test_quarter_start_month_4_january():
    assert fiscal_quarter(date(2026, 1, 15), 4) == 4


def test_quarter_start_month_4_march_31():
    assert fiscal_quarter(date(2026, 3, 31), 4) == 4


# --- fiscal_label with start_month=4 ---

def test_label_start_month_4_may():
    assert fiscal_label(date(2026, 5, 1), 4) == "FY2027-Q1"


def test_label_start_month_4_january():
    assert fiscal_label(date(2026, 1, 15), 4) == "FY2026-Q4"


# --- fiscal_start with start_month=4 ---

def test_start_start_month_4_may():
    assert fiscal_start(date(2026, 5, 1), 4) == date(2026, 4, 1)


def test_start_start_month_4_january():
    assert fiscal_start(date(2026, 1, 15), 4) == date(2025, 4, 1)


# --- other start months ---

def test_year_start_month_1():
    assert fiscal_year(date(2026, 6, 15), 1) == 2026


def test_quarter_start_month_1():
    assert fiscal_quarter(date(2026, 6, 15), 1) == 2


def test_year_start_month_10_november():
    assert fiscal_year(date(2026, 11, 1), 10) == 2027


def test_year_start_month_10_september():
    assert fiscal_year(date(2026, 9, 30), 10) == 2026


def test_quarter_start_month_10_october():
    assert fiscal_quarter(date(2026, 10, 1), 10) == 1


def test_start_start_month_10_november():
    assert fiscal_start(date(2026, 11, 1), 10) == date(2026, 10, 1)


# --- errors ---

def test_year_start_month_zero_raises_value_error():
    with pytest.raises(ValueError):
        fiscal_year(date(2026, 5, 1), 0)


def test_year_start_month_13_raises_value_error():
    with pytest.raises(ValueError):
        fiscal_year(date(2026, 5, 1), 13)


def test_year_non_date_raises_type_error():
    with pytest.raises(TypeError):
        fiscal_year("2026-05-01", 4)
