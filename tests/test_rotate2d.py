"""tests/test_rotate2d.py: rotate2d 的逐条验收要点测试。"""

import math

import pytest

from rotate2d import rotate_point, rotate_points

TOL = 1e-9


def assert_close(actual, expected):
    assert len(actual) == 2
    assert abs(actual[0] - expected[0]) <= TOL, (actual, expected)
    assert abs(actual[1] - expected[1]) <= TOL, (actual, expected)


def test_rotate_90_unit_x():
    assert_close(rotate_point(1, 0, 90), (0.0, 1.0))


def test_rotate_180_unit_x():
    assert_close(rotate_point(1, 0, 180), (-1.0, 0.0))


def test_rotate_neg90_unit_x():
    assert_close(rotate_point(1, 0, -90), (0.0, -1.0))


def test_rotate_360_unit_x():
    assert_close(rotate_point(1, 0, 360), (1.0, 0.0))


def test_rotate_zero_degrees():
    assert_close(rotate_point(3, 4, 0), (3.0, 4.0))


def test_rotate_origin_any_angle():
    assert_close(rotate_point(0, 0, 37), (0.0, 0.0))


def test_rotate_with_center():
    assert_close(rotate_point(2, 1, 90, center=(1, 1)), (1.0, 2.0))


def test_center_point_unmoved():
    assert_close(rotate_point(1, 1, 90, center=(1, 1)), (1.0, 1.0))


def test_rotate_unit_y_90():
    assert_close(rotate_point(0, 1, 90), (-1.0, 0.0))


def test_rotate_points_list():
    result = rotate_points([(1, 0), (0, 1)], 90)
    assert len(result) == 2
    assert_close(result[0], (0.0, 1.0))
    assert_close(result[1], (-1.0, 0.0))


def test_rotate_points_empty():
    assert rotate_points([], 90) == []


def test_bad_x_type():
    with pytest.raises(TypeError):
        rotate_point("1", 0, 90)


def test_bad_degrees_type():
    with pytest.raises(TypeError):
        rotate_point(1, 0, "90")


def test_center_wrong_length():
    with pytest.raises(TypeError):
        rotate_point(1, 0, 90, center=(1,))


def test_center_not_sequence():
    with pytest.raises(TypeError):
        rotate_point(1, 0, 90, center=5)


def test_points_element_wrong_length():
    with pytest.raises(TypeError):
        rotate_points([(1, 2, 3)], 90)


def test_points_not_sequence():
    with pytest.raises(TypeError):
        rotate_points("ab", 90)


# --- 补充覆盖：校验细则（bool 拒、数值类型、center 元素类型） ---


def test_bool_rejected():
    with pytest.raises(TypeError):
        rotate_point(True, 0, 90)
    with pytest.raises(TypeError):
        rotate_point(1, 0, False)


def test_center_element_not_number():
    with pytest.raises(TypeError):
        rotate_point(1, 0, 90, center=(1, "1"))


def test_y_not_number():
    with pytest.raises(TypeError):
        rotate_point(1, None, 90)


def test_points_element_not_sequence():
    with pytest.raises(TypeError):
        rotate_points([5], 90)


def test_returns_floats():
    result = rotate_point(1, 2, 45)
    assert isinstance(result, tuple)
    assert isinstance(result[0], float)
    assert isinstance(result[1], float)


def test_list_center_accepted():
    assert_close(rotate_point(1, 0, 90, center=[0, 0]), (0.0, 1.0))


def test_order_preserved_and_matches_rotate_point():
    points = [(1, 0), (2, 3), (-1, 4)]
    result = rotate_points(points, 30, center=(1, 1))
    assert len(result) == 3
    for got, pt in zip(result, points):
        assert_close(got, rotate_point(pt[0], pt[1], 30, center=(1, 1)))


def test_full_circle_identity():
    assert_close(rotate_point(3.5, -2.25, 360), (3.5, -2.25))
