"""tests for energyconv: 能量单位换算（第五十六轮 A 单验收要点逐条覆盖）。"""

import pytest

from energyconv import convert_energy

UNITS = ("J", "kJ", "cal", "kcal", "kWh", "BTU")

REL_TOL = 1e-9
KWH_TO_BTU_TOL = 5e-5


def close(actual, expected, rel=REL_TOL):
    """相对误差断言（0 用绝对比较）。"""
    if expected == 0.0:
        assert actual == 0.0
    else:
        assert abs(actual - expected) <= rel * abs(expected), (
            f"{actual!r} != {expected!r} (rel tol {rel})"
        )


# --- 验收要点 ---

def test_cal_to_j():
    close(convert_energy(1, "cal", "J"), 4.184)


def test_kcal_to_kj():
    close(convert_energy(1, "kcal", "kJ"), 4.184)


def test_kwh_to_kj():
    close(convert_energy(1, "kWh", "kJ"), 3600.0)


def test_kwh_to_btu():
    close(convert_energy(1, "kWh", "BTU"), 3412.1416, rel=KWH_TO_BTU_TOL)


def test_btu_to_kj():
    close(convert_energy(100, "BTU", "kJ"), 105.505585262)


def test_negative_value_allowed():
    close(convert_energy(-5, "kJ", "J"), -5000.0)


def test_zero_value():
    close(convert_energy(0, "BTU", "cal"), 0.0)


def test_identity_for_every_unit():
    for u in UNITS:
        close(convert_energy(1, u, u), 1.0)


def test_chain_consistency_via_kwh():
    for u in UNITS:
        direct = convert_energy(2.5, u, "J")
        via_kwh = (
            convert_energy(2.5, u, "kWh") * convert_energy(1, "kWh", "J")
        )
        close(direct, via_kwh)


def test_unknown_unit_raises_value_error():
    with pytest.raises(ValueError):
        convert_energy(1, "J", "erg")


def test_case_mismatch_raises_value_error():
    with pytest.raises(ValueError):
        convert_energy(1, "j", "J")
