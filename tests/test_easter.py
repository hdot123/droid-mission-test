from datetime import date

import pytest

from easter import easter_date


def test_known_years():
    assert easter_date(2024) == date(2024, 3, 31)
    assert easter_date(2025) == date(2025, 4, 20)
    assert easter_date(2026) == date(2026, 4, 5)
    assert easter_date(2023) == date(2023, 4, 9)
    assert easter_date(2000) == date(2000, 4, 23)
    assert easter_date(1900) == date(1900, 4, 15)
    assert easter_date(1999) == date(1999, 4, 4)
    assert easter_date(2019) == date(2019, 4, 21)
    assert easter_date(2030) == date(2030, 4, 21)
    assert easter_date(2100) == date(2100, 3, 28)
    assert easter_date(1583) == date(1583, 4, 10)
    assert easter_date(4099) == date(4099, 4, 19)


def test_out_of_range_raises_value_error():
    with pytest.raises(ValueError):
        easter_date(1582)
    with pytest.raises(ValueError):
        easter_date(4100)


def test_non_int_raises_type_error():
    with pytest.raises(TypeError):
        easter_date(2026.0)
    with pytest.raises(TypeError):
        easter_date("2026")
    with pytest.raises(TypeError):
        easter_date(True)
