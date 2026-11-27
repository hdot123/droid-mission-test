"""Tests for bezier.py — Bezier curve point/curve evaluation."""

import math
import random

import pytest

from bezier import bezier_curve, bezier_point

TOL = 1e-9


def assert_point_close(actual, expected):
    ax, ay = actual
    ex, ey = expected
    assert ax == pytest.approx(ex, rel=TOL, abs=TOL)
    assert ay == pytest.approx(ey, rel=TOL, abs=TOL)


def assert_curve_close(actual, expected):
    assert len(actual) == len(expected)
    for a, e in zip(actual, expected):
        assert_point_close(a, e)


def bernstein_point(points, t):
    """Independent reference: Bernstein basis sum."""
    n = len(points) - 1
    x = 0.0
    y = 0.0
    for i, (px, py) in enumerate(points):
        weight = math.comb(n, i) * (t ** i) * ((1.0 - t) ** (n - i))
        x += px * weight
        y += py * weight
    return (x, y)


# --- Acceptance examples: bezier_point -------------------------------

def test_point_line_start():
    assert bezier_point([(0, 0), (3, 4)], 0.0) == (0.0, 0.0)


def test_point_line_end():
    assert bezier_point([(0, 0), (3, 4)], 1.0) == (3.0, 4.0)


def test_point_quadratic_midpoint():
    assert_point_close(
        bezier_point([(0, 0), (0, 1), (1, 1)], 0.5), (0.25, 0.75)
    )


def test_point_line_quarter():
    assert_point_close(bezier_point([(0, 0), (2, 2)], 0.25), (0.5, 0.5))


def test_point_endpoints_land_exactly():
    # t = 0 / t 1 must be exact on first / last control point.
    points = [(1.5, -2.5), (3.25, 0.0), (-4.0, 7.5)]
    assert bezier_point(points, 0.0) == (1.5, -2.5)
    assert bezier_point(points, 1.0) == (-4.0, 7.5)


def test_point_accepts_list_and_tuple_points():
    assert_point_close(bezier_point([[0, 0], [3, 4]], 0.5), (1.5, 2.0))
    assert_point_close(bezier_point([(0, 0), (2, 2)], 0.5), (1.0, 1.0))


# --- Acceptance example: bezier_curve --------------------------------

def test_curve_five_samples():
    assert_curve_close(
        bezier_curve([(0, 0), (1, 2), (2, 0)], 5),
        [
            (0.0, 0.0),
            (0.5, 0.75),
            (1.0, 1.0),
            (1.5, 0.75),
            (2.0, 0.0),
        ],
    )


def test_curve_endpoints_and_count():
    points = [(0, 0), (1, 3), (4, 0)]
    curve = bezier_curve(points, 7)
    assert len(curve) == 7
    assert curve[0] == (0.0, 0.0)
    assert curve[-1] == (4.0, 0.0)


def test_curve_samples_match_point_at_same_t():
    points = [(-1.0, 2.0), (0.5, -0.5), (3.0, 1.0), (5.0, 0.0)]
    samples = 9
    curve = bezier_curve(points, samples)
    for i, expected in enumerate(curve):
        actual = bezier_point(points, i / (samples - 1))
        assert_point_close(actual, expected)


# --- Property: de Casteljau vs Bernstein -----------------------------

def test_property_de_casteljau_matches_bernstein():
    rng = random.Random(20261127)
    for _ in range(60):
        degree = rng.randint(1, 6)  # degree 1..6 => 2..7 control points
        points = [
            (rng.uniform(-10, 10), rng.uniform(-10, 10))
            for _ in range(degree + 1)
        ]
        for _ in range(6):
            t = rng.random()
            actual = bezier_point(points, t)
            expected = bernstein_point(points, t)
            assert_point_close(actual, expected)


def test_property_endpoints_exact_for_random_polygons():
    rng = random.Random(961)
    for _ in range(30):
        n = rng.randint(2, 7)
        points = [
            (rng.uniform(-5, 5), rng.uniform(-5, 5)) for _ in range(n)
        ]
        assert bezier_point(points, 0.0) == (float(points[0][0]), float(points[0][1]))
        assert bezier_point(points, 1.0) == (float(points[-1][0]), float(points[-1][1]))


# --- ValueError cases ------------------------------------------------

def test_value_error_too_few_points():
    with pytest.raises(ValueError):
        bezier_point([(0, 0)], 0.5)


def test_value_error_t_above_one():
    with pytest.raises(ValueError):
        bezier_point([(0, 0), (1, 1)], 1.5)


def test_value_error_t_below_zero():
    with pytest.raises(ValueError):
        bezier_point([(0, 0), (1, 1)], -0.1)


def test_value_error_samples_below_two():
    with pytest.raises(ValueError):
        bezier_curve([(0, 0), (1, 1)], 1)


# --- TypeError cases --------------------------------------------------

def test_type_error_points_not_list():
    with pytest.raises(TypeError):
        bezier_point("ab", 0.5)


def test_type_error_bad_coordinate():
    with pytest.raises(TypeError):
        bezier_point([(0, 0), (1, "a")], 0.5)


def test_type_error_t_not_numeric():
    with pytest.raises(TypeError):
        bezier_point([(0, 0), (1, 1)], "0.5")


def test_type_error_samples_not_int():
    with pytest.raises(TypeError):
        bezier_curve([(0, 0), (1, 1)], 2.5)


def test_type_error_samples_bool():
    with pytest.raises(TypeError):
        bezier_curve([(0, 0), (1, 1)], True)


def test_type_error_points_not_list_containers():
    with pytest.raises(TypeError):
        bezier_point((0, 0), 0.5)
    with pytest.raises(TypeError):
        bezier_point({"p": (0, 0)}, 0.5)


def test_type_error_malformed_point_shapes():
    with pytest.raises(TypeError):
        bezier_point([(0, 0), (1,)], 0.5)
    with pytest.raises(TypeError):
        bezier_point([(0, 0), (1, 2, 3)], 0.5)
    with pytest.raises(TypeError):
        bezier_point([(0, 0), "ab"], 0.5)


def test_type_error_t_bool():
    with pytest.raises(TypeError):
        bezier_point([(0, 0), (1, 1)], True)
