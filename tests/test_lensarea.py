"""tests/test_lensarea.py：双圆交叠（透镜）面积 lensarea 的验收测试。

覆盖验收要点的每一项：具体数值、边界归属（外切/分离/内切/包含）、
对称性、两弓形合成与 Simpson 数值积分两路一致、入参约定（负值
ValueError、非数值含 bool TypeError）、半径为 0 合法。
"""

import math
import random

import pytest

from lensarea import lens_area

REL_TOL = 1e-9
SIMPSON_PANELS = 8000
SIMPSON_TOL = 1e-4


# --- 独立参考实现：两弓形（扇形 − 三角）合成 ---------------------------------

def _segments(r1, r2, d):
    """两弓形（扇形 − 三角形）合成的独立参考实现（与被测闭式同源但独立）。"""
    r1 = float(r1)
    r2 = float(r2)
    d = float(d)
    if d >= r1 + r2:
        return 0.0
    if d <= abs(r1 - r2):
        return math.pi * min(r1, r2) ** 2
    d2 = d * d
    a2 = r1 * r1
    b2 = r2 * r2
    cos1 = (d2 + a2 - b2) / (2.0 * d * r1)
    cos2 = (d2 + b2 - a2) / (2.0 * d * r2)
    cos1 = max(-1.0, min(1.0, cos1))
    cos2 = max(-1.0, min(1.0, cos2))
    ang1 = math.acos(cos1)
    ang2 = math.acos(cos2)
    # 每侧弓形 = 扇形（半角 ang，圆心角 2·ang） − 等腰三角形
    sector1 = a2 * ang1
    sector2 = b2 * ang2
    triangle1 = a2 * math.sin(ang1) * math.cos(ang1)  # = ½·r1²·sin(2·ang1)
    triangle2 = b2 * math.sin(ang2) * math.cos(ang2)
    return (sector1 - triangle1) + (sector2 - triangle2)


# --- 独立参考实现：Simpson 数值积分 -----------------------------------------

def _simpson(r1, r2, d, panels=SIMPSON_PANELS):
    """对竖直条带高度 2·min(√(r1²−x²), √(r2²−(x−d)²)) 做复合 Simpson 积分。"""
    x_lo = max(-r1, d - r2)
    x_hi = min(r1, d + r2)
    if x_hi <= x_lo:
        return 0.0

    def height(x):
        a = r1 * r1 - x * x
        b = r2 * r2 - (x - d) * (x - d)
        if a <= 0.0 or b <= 0.0:
            return 0.0
        return 2.0 * min(math.sqrt(a), math.sqrt(b))

    if panels % 2:
        panels += 1
    h = (x_hi - x_lo) / panels
    total = height(x_lo) + height(x_hi)
    for i in range(1, panels):
        total += (4.0 if i % 2 else 2.0) * height(x_lo + i * h)
    return total * h / 3.0


# --- 验收要点：具体数值 -----------------------------------------------------

def test_lens_area_equilateral_overlap():
    # lens_area(1, 1, 1) ≈ 2π/3 − √3/2
    got = lens_area(1, 1, 1)
    expected = 2.0 * math.pi / 3.0 - math.sqrt(3.0) / 2.0
    assert expected == pytest.approx(1.2283696986087567, rel=REL_TOL)
    assert got == pytest.approx(expected, rel=REL_TOL)


def test_lens_area_concentric_equal_circles():
    # lens_area(2, 2, 0) ≈ 4π
    got = lens_area(2, 2, 0)
    assert got == pytest.approx(4.0 * math.pi, rel=REL_TOL)
    assert got == pytest.approx(12.566370614359172, rel=REL_TOL)


def test_lens_area_containment_small_circle_full_area():
    # 包含：恰为小圆全面积 π
    got = lens_area(3, 1, 1.5)
    assert got == pytest.approx(math.pi, rel=REL_TOL)
    assert got == pytest.approx(3.141592653589793, rel=REL_TOL)


def test_lens_area_internal_tangency():
    # 内切（d == |r1 − r2|）：恰为小圆全面积 π，不得是近似小量或 NaN
    got = lens_area(3, 1, 2.0)
    assert not math.isnan(got)
    assert got == pytest.approx(math.pi, rel=REL_TOL)
    assert got == pytest.approx(3.141592653589793, rel=REL_TOL)


def test_lens_area_external_tangency_is_exactly_zero():
    # 外切（d == r1 + r2）：恰 0.0
    got = lens_area(1, 1, 2)
    assert got == 0.0
    assert isinstance(got, float)


def test_lens_area_separated_is_exactly_zero():
    # 分离：恰 0.0
    got = lens_area(1, 1, 2.5)
    assert got == 0.0
    assert isinstance(got, float)


def test_lens_area_zero_radius_is_legal():
    # 半径为 0 合法，面积 0.0
    assert lens_area(0, 5, 1) == 0.0
    assert lens_area(5, 0, 0) == 0.0


# --- 验收要点：对称性 -------------------------------------------------------

def test_lens_area_symmetric_under_radius_swap():
    rng = random.Random(5803)
    for _ in range(40):
        r1 = rng.uniform(0.1, 6.0)
        r2 = rng.uniform(0.1, 6.0)
        d = rng.uniform(0.0, (r1 + r2) * 1.2)
        a = lens_area(r1, r2, d)
        b = lens_area(r2, r1, d)
        assert a == pytest.approx(b, rel=REL_TOL, abs=1e-12)


# --- 验收要点：与两弓形合成、Simpson 积分两路一致 ---------------------------

def test_lens_area_agrees_with_two_segment_composition():
    rng = random.Random(5803)
    checked = 0
    while checked < 60:
        r1 = rng.uniform(0.3, 5.0)
        r2 = rng.uniform(0.3, 5.0)
        d = rng.uniform(0.0, (r1 + r2) * 0.999)  # 仅重叠区
        if d >= r1 + r2 or d <= abs(r1 - r2):
            continue
        got = lens_area(r1, r2, d)
        ref = _segments(r1, r2, d)
        assert got == pytest.approx(ref, rel=REL_TOL)
        checked += 1


def test_lens_area_agrees_with_simpson_integration():
    rng = random.Random(5803)
    checked = 0
    while checked < 15:
        r1 = rng.uniform(0.3, 5.0)
        r2 = rng.uniform(0.3, 5.0)
        d = rng.uniform(0.0, (r1 + r2) * 0.999)  # 仅重叠区
        if d >= r1 + r2 or d <= abs(r1 - r2):
            continue
        got = lens_area(r1, r2, d)
        ref = _simpson(r1, r2, d, SIMPSON_PANELS)
        assert got == pytest.approx(ref, rel=0.0, abs=SIMPSON_TOL)
        checked += 1


# --- 验收要点：入参约定 -----------------------------------------------------

def test_lens_area_negative_r1_raises_value_error():
    with pytest.raises(ValueError):
        lens_area(-1, 2, 1)


def test_lens_area_negative_d_raises_value_error():
    with pytest.raises(ValueError):
        lens_area(1, 2, -0.5)


def test_lens_area_negative_r2_raises_value_error():
    with pytest.raises(ValueError):
        lens_area(2, -3, 1)


def test_lens_area_string_raises_type_error():
    with pytest.raises(TypeError):
        lens_area("1", 2, 1)


def test_lens_area_bool_raises_type_error():
    with pytest.raises(TypeError):
        lens_area(1, True, 1)


def test_lens_area_rejects_other_non_numeric():
    with pytest.raises(TypeError):
        lens_area(None, 1, 1)
    with pytest.raises(TypeError):
        lens_area(1, 1, "x")
    with pytest.raises(TypeError):
        lens_area([1], 1, 1)
