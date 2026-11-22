import pytest

from volconv import convert

TOL = 1e-9


def _assert_close(actual, expected):
    assert abs(actual - expected) <= TOL, "{} !~ {} (tol {})".format(
        actual, expected, TOL
    )


def test_gal_to_l_exact():
    assert convert(1, "gal", "L") == 3.785411784


def test_gal_to_qt():
    _assert_close(convert(1, "gal", "qt"), 4.0)


def test_l_to_floz():
    _assert_close(convert(1, "L", "floz"), 33.814022701843)


def test_ml_to_cup():
    _assert_close(convert(500, "mL", "cup"), 2.1133764188651876)


def test_cup_to_ml():
    _assert_close(convert(2, "cup", "mL"), 473.176473)


def test_m3_to_l_exact():
    assert convert(1, "m3", "L") == 1000.0


def test_tsp_to_tbsp():
    _assert_close(convert(3, "tsp", "tbsp"), 1.0)


def test_qt_to_pt_exact():
    assert convert(1, "qt", "pt") == 2.0


def test_cm3_to_ml_exact():
    assert convert(100, "cm3", "mL") == 100.0


def test_floz_to_tbsp():
    _assert_close(convert(1, "floz", "tbsp"), 2.0)


def test_identity_l_to_l():
    assert convert(5, "L", "L") == 5.0


def test_unknown_units_raise_value_error():
    with pytest.raises(ValueError):
        convert(1, "L", "oz")
    with pytest.raises(ValueError):
        convert(1, "foo", "L")


def test_bad_value_types_raise_type_error():
    with pytest.raises(TypeError):
        convert("1", "L", "mL")
    with pytest.raises(TypeError):
        convert(True, "L", "mL")
