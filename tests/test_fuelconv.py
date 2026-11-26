"""fuelconv 验收测试：燃油消耗倒数式换算。"""

import itertools

import pytest

from fuelconv import convert_fuel

UNITS = ["L/100km", "mpgUS", "mpgImp", "km/L"]


# --- 验收要点：逐个数值点 ---


def test_l100km_to_mpgus():
    # convert_fuel(10, "L/100km", "mpgUS") ≈ 23.5215 (容差 5e-5)
    assert convert_fuel(10, "L/100km", "mpgUS") == pytest.approx(23.5215, abs=5e-5)


def test_mpgus_to_l100km_30():
    # convert_fuel(30, "mpgUS", "L/100km") ≈ 7.8405 (容差 5e-5)
    assert convert_fuel(30, "mpgUS", "L/100km") == pytest.approx(7.8405, abs=5e-5)


def test_mpgimp_to_l100km_40():
    # convert_fuel(40, "mpgImp", "L/100km") ≈ 7.0620 (容差 5e-5)
    assert convert_fuel(40, "mpgImp", "L/100km") == pytest.approx(7.0620, abs=5e-5)


def test_l100km_to_kmpl():
    # convert_fuel(10, "L/100km", "km/L") ≈ 10.0
    assert convert_fuel(10, "L/100km", "km/L") == pytest.approx(10.0, rel=1e-9)


def test_kmpl_to_l100km():
    # convert_fuel(15, "km/L", "L/100km") ≈ 6.666666666666667
    assert convert_fuel(15, "km/L", "L/100km") == pytest.approx(
        6.666666666666667, rel=1e-9
    )


def test_mpgus_one_to_l100km():
    # convert_fuel(1, "mpgUS", "L/100km") ≈ 235.2145833
    assert convert_fuel(1, "mpgUS", "L/100km") == pytest.approx(235.2145833, rel=1e-9)


# --- 验收要点：因子由定义值导出（相对误差 1e-9）---


def test_mpgus_factor_derived_from_definitions():
    expected = 100.0 * 3.785411784 / 1.609344  # 235.214583…
    assert convert_fuel(1, "mpgUS", "L/100km") == pytest.approx(expected, rel=1e-9)


def test_mpgimp_factor_derived_from_definitions():
    expected = 100.0 * 4.54609 / 1.609344  # 282.480936…
    assert convert_fuel(1, "mpgImp", "L/100km") == pytest.approx(expected, rel=1e-9)


def test_mpgus_and_mpgimp_factors_differ():
    # 加仑定义不同，两因子不得混用
    us = convert_fuel(10, "L/100km", "mpgUS")
    imp = convert_fuel(10, "L/100km", "mpgImp")
    assert us != pytest.approx(imp, rel=1e-9)
    assert us == pytest.approx(23.521458333333336, rel=1e-9)
    assert imp == pytest.approx(28.24809363291741, rel=1e-9)


# --- 验收要点：倒数式方向（油耗越大越费油、mpg 越大越省油）---


def test_reciprocal_direction_not_linear_scaling():
    low = convert_fuel(10, "L/100km", "mpgUS")
    high = convert_fuel(20, "L/100km", "mpgUS")
    # 油耗翻倍 → mpg 减半（倒数式），而非翻倍（线性缩放）
    assert high < low
    assert high == pytest.approx(low / 2.0, rel=1e-9)


# --- 验收要点：往返性与恒等 ---


def test_roundtrip_all_unit_pairs():
    for u, v in itertools.product(UNITS, repeat=2):
        back = convert_fuel(convert_fuel(8.4, u, v), v, u)
        assert back == pytest.approx(8.4, rel=1e-9), (u, v)


def test_identity_all_units():
    for u in UNITS:
        assert convert_fuel(8.4, u, u) == pytest.approx(8.4, rel=1e-9), u


# --- 验收要点：入参错误约定 ---


def test_non_positive_value_raises_value_error():
    with pytest.raises(ValueError):
        convert_fuel(0, "L/100km", "mpgUS")
    with pytest.raises(ValueError):
        convert_fuel(-3, "mpgUS", "km/L")


def test_unknown_unit_raises_value_error():
    with pytest.raises(ValueError):
        convert_fuel(5, "mpg", "km/L")


def test_non_numeric_value_raises_type_error():
    with pytest.raises(TypeError):
        convert_fuel("5", "mpgUS", "km/L")


def test_bool_value_raises_type_error():
    # bool 属于“非数值（含 bool）”
    with pytest.raises(TypeError):
        convert_fuel(True, "L/100km", "mpgUS")
