"""Tests for pressureconv.convert (round 46-D)."""

import pytest

from pressureconv import convert


def test_atm_to_pa():
    assert convert(1, "atm", "Pa") == 101325.0


def test_atm_to_psi():
    assert convert(1, "atm", "psi") == pytest.approx(14.69594877551422, abs=1e-9)


def test_bar_to_kpa():
    assert convert(1, "bar", "kPa") == 100.0


def test_mmhg_to_atm_loose_tolerance():
    # 760 mmHg differs from standard atmosphere by ~1.4e-7 relative.
    assert convert(760, "mmHg", "atm") == pytest.approx(1.0, abs=1e-6)


def test_psi_to_kpa():
    assert convert(1, "psi", "kPa") == pytest.approx(6.894757293168, abs=1e-9)


def test_bar_to_psi():
    assert convert(2.5, "bar", "psi") == pytest.approx(36.25943443255421, abs=1e-9)


def test_inhg_to_pa():
    assert convert(30, "inHg", "Pa") == pytest.approx(101591.67, abs=1e-9)


def test_torr_to_mmhg():
    assert convert(1, "torr", "mmHg") == 1.0


def test_pa_to_atm():
    assert convert(101325, "Pa", "atm") == 1.0


def test_kpa_identity():
    assert convert(7, "kPa", "kPa") == 7.0


def test_unknown_to_unit_raises_value_error():
    with pytest.raises(ValueError):
        convert(1, "Pa", "lb")


def test_unknown_from_unit_raises_value_error():
    with pytest.raises(ValueError):
        convert(1, "kg", "Pa")


def test_string_value_raises_type_error():
    with pytest.raises(TypeError):
        convert("1", "Pa", "kPa")


def test_none_value_raises_type_error():
    with pytest.raises(TypeError):
        convert(None, "Pa", "kPa")


def test_bool_value_raises_type_error():
    with pytest.raises(TypeError):
        convert(True, "Pa", "kPa")
