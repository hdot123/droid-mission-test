"""tests/test_circle.py: 圆、扇形与弓形验收测试（第五十七轮 C 单）。"""

import math

import pytest

import circle


# --- circle_area ---

def test_circle_area_one_is_pi():
    assert circle.circle_area(1) == pytest.approx(3.141592653589793, rel=1e-9)


def test_circle_area_zero_is_zero():
    assert circle.circle_area(0) == pytest.approx(0.0, rel=1e-9)


# --- circle_circumference ---

def test_circle_circumference_one_is_two_pi():
    assert circle.circle_circumference(1) == pytest.approx(
        6.283185307179586, rel=1e-9
    )


# --- sector_area ---

def test_sector_area_two_radius_90_deg_is_pi():
    assert circle.sector_area(2, 90) == pytest.approx(3.141592653589793, rel=1e-9)


def test_sector_area_full_circle_is_circle_area():
    assert circle.sector_area(1, 360) == pytest.approx(3.141592653589793, rel=1e-9)


def test_sector_area_zero_angle_is_zero():
    assert circle.sector_area(3, 0) == pytest.approx(0.0, rel=1e-9)


# --- segment_area ---

def test_segment_area_90_deg_is_quarter_circle_minus_triangle():
    # π/4 − 1/2
    assert circle.segment_area(1, 90) == pytest.approx(
        0.2853981633974483, rel=1e-9
    )


def test_segment_area_180_deg_is_half_circle():
    # 半圆 π/2
    assert circle.segment_area(1, 180) == pytest.approx(
        1.5707963267948966, rel=1e-9
    )


def test_segment_area_360_deg_is_full_circle():
    assert circle.segment_area(1, 360) == pytest.approx(3.141592653589793, rel=1e-9)


def test_segment_area_zero_angle_is_zero():
    assert circle.segment_area(2, 0) == pytest.approx(0.0, rel=1e-9)


# --- 性质 ---

def test_sector_area_ratio_property():
    for r in (1, 2.5, 7):
        for a in (0, 30, 45, 90, 180, 270, 360):
            ratio = circle.sector_area(r, a) / circle.circle_area(r)
            assert ratio == pytest.approx(a / 360, rel=1e-9)


def test_segment_equals_sector_minus_triangle():
    for r in (1, 2, 3.5):
        for a in (0, 15, 90, 180, 270, 360):
            triangle = 0.5 * r * r * math.sin(math.radians(a))
            expected = circle.sector_area(r, a) - triangle
            assert circle.segment_area(r, a) == pytest.approx(expected, rel=1e-9)


# --- ValueError ---

def test_circle_area_negative_radius_raises_value_error():
    with pytest.raises(ValueError):
        circle.circle_area(-1)


def test_sector_area_angle_out_of_range_raises_value_error():
    with pytest.raises(ValueError):
        circle.sector_area(1, 361)


def test_segment_area_negative_angle_raises_value_error():
    with pytest.raises(ValueError):
        circle.segment_area(1, -10)


# --- TypeError ---

def test_circle_area_non_number_raises_type_error():
    with pytest.raises(TypeError):
        circle.circle_area("1")


def test_sector_area_bool_raises_type_error():
    with pytest.raises(TypeError):
        circle.sector_area(1, True)
