import pytest

from isoweek import from_iso_week, to_iso_week


def test_to_iso_week_basic():
    assert to_iso_week(2026, 1, 1) == (2026, 1, 4)
    assert to_iso_week(2025, 12, 29) == (2026, 1, 1)
    assert to_iso_week(2026, 11, 19) == (2026, 47, 4)


def test_to_iso_week_week_53_year_boundary():
    assert to_iso_week(2026, 12, 31) == (2026, 53, 4)
    assert to_iso_week(2027, 1, 1) == (2026, 53, 5)
    assert to_iso_week(2020, 12, 31) == (2020, 53, 4)


def test_to_iso_week_week_52_boundary():
    assert to_iso_week(2019, 12, 29) == (2019, 52, 7)
    assert to_iso_week(2019, 12, 30) == (2020, 1, 1)


def test_from_iso_week_week_1():
    assert from_iso_week(2026, 1, 4) == (2026, 1, 1)
    assert from_iso_week(2026, 1, 1) == (2025, 12, 29)


def test_from_iso_week_week_53():
    assert from_iso_week(2026, 53, 4) == (2026, 12, 31)
    assert from_iso_week(2020, 53, 4) == (2020, 12, 31)


def test_from_iso_week_week_52():
    assert from_iso_week(2019, 52, 7) == (2019, 12, 29)


def test_from_iso_week_nonexistent_week():
    with pytest.raises(ValueError):
        from_iso_week(2026, 54, 1)
    with pytest.raises(ValueError):
        from_iso_week(2021, 53, 1)


def test_from_iso_week_weekday_out_of_range():
    with pytest.raises(ValueError):
        from_iso_week(2026, 1, 0)
    with pytest.raises(ValueError):
        from_iso_week(2026, 1, 8)


def test_to_iso_week_invalid_date():
    with pytest.raises(ValueError):
        to_iso_week(2026, 2, 29)


def test_to_iso_week_non_int_inputs():
    with pytest.raises(TypeError):
        to_iso_week("2026", 1, 1)
    with pytest.raises(TypeError):
        to_iso_week(2026, "1", 1)
    with pytest.raises(TypeError):
        to_iso_week(2026, 1, 1.0)


def test_from_iso_week_non_int_inputs():
    with pytest.raises(TypeError):
        from_iso_week("2026", 1, 1)
    with pytest.raises(TypeError):
        from_iso_week(2026, "1", 1)
    with pytest.raises(TypeError):
        from_iso_week(2026, 1, None)


def test_roundtrip_against_datetime():
    from datetime import date, timedelta

    day = date(2015, 1, 1)
    while day <= date(2035, 12, 31):
        iso_year, iso_week, iso_weekday = to_iso_week(day.year, day.month, day.day)
        assert from_iso_week(iso_year, iso_week, iso_weekday) == (
            day.year,
            day.month,
            day.day,
        )
        day += timedelta(days=1)
