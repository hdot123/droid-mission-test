import pytest

from rotate2d import rotate_point, rotate_points

TOL = 1e-9


def assert_close(actual, expected):
    assert len(actual) == len(expected)
    for a, e in zip(actual, expected):
        assert abs(a - e) < TOL, (actual, expected)


def test_rotate_point_90_degrees():
    rx, ry = rotate_point(1, 0, 90)
    assert abs(rx - 0.0) < TOL
    assert abs(ry - 1.0) < TOL


def test_rotate_point_180_degrees():
    assert_close(rotate_point(1, 0, 180), (-1.0, 0.0))


def test_rotate_point_minus_90_degrees():
    assert_close(rotate_point(1, 0, -90), (0.0, -1.0))


def test_rotate_point_360_degrees():
    assert_close(rotate_point(1, 0, 360), (1.0, 0.0))


def test_rotate_point_zero_degrees():
    assert_close(rotate_point(3, 4, 0), (3.0, 4.0))


def test_rotate_point_origin_is_fixed():
    assert_close(rotate_point(0, 0, 37), (0.0, 0.0))


def test_rotate_point_around_center():
    assert_close(rotate_point(2, 1, 90, center=(1, 1)), (1.0, 2.0))


def test_rotate_point_center_stays_fixed():
    assert_close(rotate_point(1, 1, 90, center=(1, 1)), (1.0, 1.0))


def test_rotate_point_y_axis_by_90():
    assert_close(rotate_point(0, 1, 90), (-1.0, 0.0))


def test_rotate_points_list():
    result = rotate_points([(1, 0), (0, 1)], 90)
    assert len(result) == 2
    assert_close(result[0], (0.0, 1.0))
    assert_close(result[1], (-1.0, 0.0))


def test_rotate_points_empty():
    assert rotate_points([], 90) == []


def test_rotate_point_rejects_string_xy():
    with pytest.raises(TypeError):
        rotate_point("1", 0, 90)


def test_rotate_point_rejects_string_degrees():
    with pytest.raises(TypeError):
        rotate_point(1, 0, "90")


def test_rotate_point_rejects_short_center():
    with pytest.raises(TypeError):
        rotate_point(1, 0, 90, center=(1,))


def test_rotate_point_rejects_non_sequence_center():
    with pytest.raises(TypeError):
        rotate_point(1, 0, 90, center=5)


def test_rotate_points_rejects_wrong_length_point():
    with pytest.raises(TypeError):
        rotate_points([(1, 2, 3)], 90)


def test_rotate_points_rejects_non_sequence():
    with pytest.raises(TypeError):
        rotate_points("ab", 90)
