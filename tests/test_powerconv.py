"""powerconv 的验收测试：逐条覆盖工作单验收要点。"""

import math

import pytest

from powerconv import convert_power

# 单位集（钉死，基准 W）——与实现同源但独立复算，防实现漂移。
FACTORS = {
    "W": 1.0,
    "kW": 1000.0,
    "hp": 745.699872,
    "PS": 735.49875,
    "BTU/h": 1055.05585262 / 3600.0,
    "ftlbf/s": 1.3558179483314004,
}

UNITS = sorted(FACTORS)


def _rel_close(actual, expected, rel=1e-9):
    """相对误差断言（expected 为 0 时退化为绝对相等）。"""
    if expected == 0.0:
        assert actual == 0.0
        return
    assert math.isclose(actual, expected, rel_tol=rel, abs_tol=0.0), (
        "expected %r, got %r (rel err %g)"
        % (expected, actual, abs(actual - expected) / abs(expected))
    )


def test_hp_to_w():
    # 验收要点 1：convert_power(1, "hp", "W") ≈ 745.699872
    _rel_close(convert_power(1, "hp", "W"), 745.699872)


def test_ps_to_w():
    # 验收要点 2：convert_power(1, "PS", "W") ≈ 735.49875
    _rel_close(convert_power(1, "PS", "W"), 735.49875)


def test_hp_to_ftlbf_s_cross_check():
    # 验收要点 3：convert_power(1, "hp", "ftlbf/s") ≈ 550.0（容差 1e-6，两钉死常数互证点）
    assert math.isclose(convert_power(1, "hp", "ftlbf/s"), 550.0, rel_tol=0, abs_tol=1e-6)


def test_kw_to_hp():
    # 验收要点 4：convert_power(1, "kW", "hp") ≈ 1.3410220896
    _rel_close(convert_power(1, "kW", "hp"), 1.3410220896)


def test_w_to_btu_h():
    # 验收要点 5：convert_power(100, "W", "BTU/h") ≈ 341.2141633
    _rel_close(convert_power(100, "W", "BTU/h"), 341.2141633)


def test_zero_hp_to_kw():
    # 验收要点 6：convert_power(0, "hp", "kW") ≈ 0.0
    assert convert_power(0, "hp", "kW") == 0.0


def test_identity_and_hp_chain_for_every_unit():
    # 验收要点 7：对每个单位 u，convert_power(3.7, u, "W")，
    # 以及经 hp 中介换算到 PS 的链路，与直达换算一致（相对误差 1e-9 内）。
    for u in UNITS:
        direct_to_w = convert_power(3.7, u, "W")
        _rel_close(direct_to_w, 3.7 * FACTORS[u] / FACTORS["W"])

        direct_to_ps = convert_power(3.7, u, "PS")
        via_hp = convert_power(convert_power(3.7, u, "hp"), "hp", "PS")
        _rel_close(via_hp, direct_to_ps)


def test_unknown_unit_raises():
    # 验收要点 8：MW 不在单位集内，抛 ValueError。
    with pytest.raises(ValueError):
        convert_power(1, "W", "MW")
    with pytest.raises(ValueError):
        convert_power(1, "MW", "W")


def test_wrong_case_raises():
    # 验收要点 9：大小写不符（HP ≠ hp）抛 ValueError。
    with pytest.raises(ValueError):
        convert_power(1, "HP", "W")
    with pytest.raises(ValueError):
        convert_power(1, "W", "kw")


def test_unit_set_has_no_energy_units():
    # 本单是功率换算：BTU（能量）不在单位集内；单位集恰好为规格所列六个。
    assert set(FACTORS) == {"W", "kW", "hp", "PS", "BTU/h", "ftlbf/s"}
    with pytest.raises(ValueError):
        convert_power(1, "W", "BTU")


def test_hp_and_ps_are_distinct_constants():
    # hp 与 PS 是两个不同常数，不得混用。
    assert FACTORS["hp"] != FACTORS["PS"]
    _rel_close(convert_power(1, "hp", "PS"), FACTORS["hp"] / FACTORS["PS"])


def test_roundtrip_chain():
    # 换算链可逆：u → kw → u 与直达一致（相对误差 1e-9 内）。
    for u in UNITS:
        roundtrip = convert_power(convert_power(2.5, u, "kW"), "kW", u)
        _rel_close(roundtrip, 2.5)


def test_returns_float():
    assert isinstance(convert_power(1, "W", "kW"), float)
