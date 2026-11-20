import pytest

from rotate2d import rotate_point, rotate_points

TOL = 1e-9


def _assert_close(actual, expected):
    """分量逐一比较，容差 1e-9。"""
    assert isinstance(actual, tuple)
    assert len(actual) == 2
    ax, ay = actual
    ex, ey = expected
    assert abs(ax - ex) <= TOL, (ax, ex)
    assert abs(ay - ey) <= TOL, (ay, ey)


# ---- rotate_point 正例（每个验收要点一条用例） ----


def test_rotate_point_90():
    _assert_close(rotate_point(1, 0, 90), (0.0, 1.0))


def test_rotate_point_180():
    _assert_close(rotate_point(1, 0, 180), (-1.0, 0.0))


def test_rotate_point_minus_90():
    _assert_close(rotate_point(1, 0, -90), (0.0, -1.0))


def test_rotate_point_360():
    _assert_close(rotate_point(1, 0, 360), (1.0, 0.0))


def test_rotate_point_zero_degrees_identity():
    _assert_close(rotate_point(3, 4, 0), (3.0, 4.0))


def test_rotate_point_origin_any_angle():
    _assert_close(rotate_point(0, 0, 37), (0.0, 0.0))


def test_rotate_point_with_center():
    _assert_close(rotate_point(2, 1, 90, center=(1, 1)), (1.0, 2.0))


def test_rotate_point_center_is_fixed():
    _assert_close(rotate_point(1, 1, 90, center=(1, 1)), (1.0, 1.0))


def test_rotate_point_y_axis_90():
    _assert_close(rotate_point(0, 1, 90), (-1.0, 0.0))


# ---- rotate_points 正例 ----


def test_rotate_points_list():
    result = rotate_points([(1, 0), (0, 1)], 90)
    assert isinstance(result, list)
    assert len(result) == 2
    _assert_close(result[0], (0.0, 1.0))
    _assert_close(result[1], (-1.0, 0.0))


def test_rotate_points_empty():
    assert rotate_points([], 90) == []


# ---- 校验：TypeError ----


def test_rotate_point_x_not_number():
    with pytest.raises(TypeError):
        rotate_point("1", 0, 90)


def test_rotate_point_degrees_not_number():
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


# ---- 校验补充：bool 拒、y 非数值、center 元素非数值、points 元素非序列 ----


def test_rotate_point_bool_rejected():
    with pytest.raises(TypeError):
        rotate_point(True, 0, 90)
    with pytest.raises(TypeError):
        rotate_point(1, False, 90)
    with pytest.raises(TypeError):
        rotate_point(1, 0, True)


def test_rotate_point_y_not_number():
    with pytest.raises(TypeError):
        rotate_point(1, "0", 90)


def test_rotate_point_center_element_not_number():
    with pytest.raises(TypeError):
        rotate_point(1, 0, 90, center=(1, "1"))
    with pytest.raises(TypeError):
        rotate_point(1, 0, 90, center=["0", 0])


def test_rotate_points_element_not_sequence():
    with pytest.raises(TypeError):
        rotate_points([5, (1, 0)], 90)


def test_rotate_points_degrees_not_number():
    with pytest.raises(TypeError):
        rotate_points([(1, 0)], "90")


def test_rotate_points_center_invalid():
    with pytest.raises(TypeError):
        rotate_points([(1, 0)], 90, center=(0,))
