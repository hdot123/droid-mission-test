import pytest

from lengthconv import convert


def test_km_to_m():
    assert convert(1, "km", "m") == 1000.0


def test_m_to_mm():
    assert convert(1, "m", "mm") == 1000.0


def test_cm_to_m():
    assert convert(100, "cm", "m") == 1.0


def test_in_to_ft():
    assert convert(12, "in", "ft") == 1.0


def test_mi_to_km():
    assert convert(1, "mi", "km") == pytest.approx(1.609344, abs=1e-9)


def test_ft_to_mi():
    assert convert(5280, "ft", "mi") == 1.0


def test_yd_to_m():
    assert convert(1, "yd", "m") == pytest.approx(0.9144, abs=1e-9)


def test_cm_to_in():
    assert convert(2.54, "cm", "in") == 1.0


def test_m_to_m_identity():
    assert convert(1, "m", "m") == 1.0


def test_zero_conversion():
    assert convert(0, "km", "mi") == 0.0


def test_ft_to_in():
    assert convert(3, "ft", "in") == 36.0


def test_yd_to_mi():
    assert convert(1760, "yd", "mi") == 1.0


def test_unknown_target_unit():
    with pytest.raises(ValueError):
        convert(1, "m", "parsec")


def test_unknown_source_unit():
    with pytest.raises(ValueError):
        convert(1, "furlong", "m")


def test_non_numeric_value():
    with pytest.raises(TypeError):
        convert("1", "m", "km")


def test_bool_value_rejected():
    with pytest.raises(TypeError):
        convert(True, "m", "km")
