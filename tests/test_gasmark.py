import pytest

from gasmark import celsius_to_gasmark, gasmark_to_celsius, gasmark_to_fahrenheit


def test_to_celsius_int_marks():
    assert gasmark_to_celsius(4) == 180
    assert gasmark_to_celsius(1) == 140
    assert gasmark_to_celsius(9) == 240


def test_to_fahrenheit_int_marks():
    assert gasmark_to_fahrenheit(4) == 350
    assert gasmark_to_fahrenheit(9) == 475


def test_to_celsius_fraction_str_marks():
    assert gasmark_to_celsius("1/4") == 110
    assert gasmark_to_celsius("1/2") == 120


def test_to_fahrenheit_fraction_str_marks():
    assert gasmark_to_fahrenheit("1/4") == 225
    assert gasmark_to_fahrenheit("1/2") == 250


def test_to_celsius_str_digit_marks():
    assert gasmark_to_celsius("6") == 200


def test_celsius_to_gasmark_exact():
    assert celsius_to_gasmark(180) == "4"
    assert celsius_to_gasmark(110) == "1/4"
    assert celsius_to_gasmark(200) == "6"


def test_celsius_to_gasmark_tie_takes_lower_mark():
    # 185 is equidistant from 180 (mark 4) and 190 (mark 5): take the lower mark.
    assert celsius_to_gasmark(185) == "4"


def test_celsius_to_gasmark_bounds():
    assert celsius_to_gasmark(0) == "1/4"
    assert celsius_to_gasmark(500) == "9"


def test_celsius_to_gasmark_nearest():
    assert celsius_to_gasmark(167) == "3"


def test_invalid_mark_value_raises_value_error():
    for bad in (0, 10, "3/4"):
        with pytest.raises(ValueError):
            gasmark_to_celsius(bad)


def test_invalid_mark_type_raises_type_error():
    for bad in (4.0, True):
        with pytest.raises(TypeError):
            gasmark_to_celsius(bad)
    with pytest.raises(TypeError):
        gasmark_to_fahrenheit(4.0)


def test_celsius_non_numeric_raises_type_error():
    for bad in ("180", True, None):
        with pytest.raises(TypeError):
            celsius_to_gasmark(bad)
