"""Tests for rotate2d: 2D point rotation."""

import pytest

from rotate2d import rotate_point, rotate_points

TOL = 1e-9


def _assert_close(actual, expected, tol=TOL):
    assert len(actual) == 2
    assert abs(actual[0] - expected[0]) <= tol, f"x: {actual[0]} !~ {expected[0]}"
    assert abs(actual[1] - expected[1]) <= tol, f"y: {actual[1]} !~ {expected[1]}"


# --- rotate_point acceptance points ---


def test_rotate_90():
    _assert_close(rotate_point(1, 0, 90), (0.0, 1.0))


def test_rotate_180():
    _assert_close(rotate_point(1, 0, 180), (-1.0, 0.0))


def test_rotate_negative_90():
    _assert_close(rotate_point(1, 0, -90), (0.0, -1.0))


def test_rotate_360():
    _assert_close(rotate_point(1, 0, 360), (1.0, 0.0))


def test_rotate_0_degrees_identity():
    _assert_close(rotate_point(3, 4, 0), (3.0, 4.0))


def test_rotate_origin_stays_origin():
    _assert_close(rotate_point(0, 0, 37), (0.0, 0.0))


def test_rotate_around_center():
    _assert_close(rotate_point(2, 1, 90, center=(1, 1)), (1.0, 2.0))


def test_center_stays_fixed():
    _assert_close(rotate_point(1, 1, 90, center=(1, 1)), (1.0, 1.0))


def test_rotate_0_1_by_90():
    _assert_close(rotate_point(0, 1, 90), (-1.0, 0.0))


# --- rotate_points acceptance points ---


def test_rotate_points_list():
    result = rotate_points([(1, 0), (0, 1)], 90)
    assert len(result) == 2
    _assert_close(result[0], (0.0, 1.0))
    _assert_close(result[1], (-1.0, 0.0))


def test_rotate_points_empty():
    assert rotate_points([], 90) == []


# --- TypeError acceptance points ---


def test_rotate_point_non_numeric_x():
    with pytest.raises(TypeError):
        rotate_point("1", 0, 90)


def test_rotate_point_non_numeric_degrees():
    with pytest.raises(TypeError):
        rotate_point(1, 0, "90")


def test_rotate_point_center_wrong_length():
    with pytest.raises(TypeError):
        rotate_point(1, 0, 90, center=(1,))


def test_rotate_point_center_not_sequence():
    with pytest.raises(TypeError):
        rotate_point(1, 0, 90, center=5)


def test_rotate_points_element_wrong_length():
    with pytest.raises(TypeError):
        rotate_points([(1, 2, 3)], 90)


def test_rotate_points_not_sequence():
    with pytest.raises(TypeError):
        rotate_points("ab", 90)


# --- additional validation (bool rejected, y non-numeric, center element type) ---


def test_rotate_point_bool_rejected():
    with pytest.raises(TypeError):
        rotate_point(True, 0, 90)
    with pytest.raises(TypeError):
        rotate_point(1, 0, True)


def test_rotate_point_non_numeric_y():
    with pytest.raises(TypeError):
        rotate_point(1, "0", 90)


def test_rotate_point_center_element_non_numeric():
    with pytest.raises(TypeError):
        rotate_point(1, 0, 90, center=(1, "1"))


def test_rotate_points_preserves_order_and_type():
    result = rotate_points([(1, 0), (0, 1), (2, 0)], 180)
    assert isinstance(result, list)
    assert all(isinstance(pt, tuple) for pt in result)
    _assert_close(result[0], (-1.0, 0.0))
    _assert_close(result[1], (0.0, -1.0))
    _assert_close(result[2], (-2.0, 0.0))


def test_rotate_points_accepts_list_points_and_center():
    result = rotate_points([[1, 0]], 90, center=[0, 0])
    _assert_close(result[0], (0.0, 1.0))


def test_rotate_point_returns_float_tuple():
    res = rotate_point(1, 0, 90)
    assert isinstance(res, tuple)
    assert isinstance(res[0], float) and isinstance(res[1], float)
