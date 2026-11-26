"""line2d 验收测试：二维直线方程、点线距离与交点。"""

import math

import pytest

from line2d import line_from_points, lines_intersection, point_line_distance

# 浮点验收相对误差。
RTOL = 1e-9


def relclose(got, want, tol=RTOL):
    """逐分量可用的相对误差比较（want 为 0 时退化为绝对误差 tol）。"""
    return abs(got - want) <= tol * max(1.0, abs(want))


# ---------------------------------------------------------------------------
# line_from_points
# ---------------------------------------------------------------------------


def test_diagonal_unit_normal_form():
    a, b, c = line_from_points((0, 0), (1, 1))
    assert relclose(a, 0.7071067811865476)
    assert relclose(b, -0.7071067811865476)
    assert relclose(c, 0.0)


def test_vertical_line_x3_form():
    a, b, _c = line_from_points((3, 0), (3, 5))
    assert abs(abs(a) - 1.0) <= RTOL
    assert relclose(b, 0.0)


def test_coincident_points_raise_valueerror():
    with pytest.raises(ValueError):
        line_from_points((1, 1), (1, 1))


def test_bad_point_types_raise_typeerror():
    with pytest.raises(TypeError):
        line_from_points((1, "a"), (2, 3))
    with pytest.raises(TypeError):
        line_from_points((1, True), (2, 3))
    with pytest.raises(TypeError):
        line_from_points((1,), (2, 3))


def test_bad_second_point_raises_typeerror():
    with pytest.raises(TypeError):
        line_from_points((1, 2), (2, 3.5, 0))
    with pytest.raises(TypeError):
        line_from_points((1, 2), "ab")


# ---------------------------------------------------------------------------
# point_line_distance
# ---------------------------------------------------------------------------


def test_distance_origin_to_antidiagonal():
    line = line_from_points((0, 1), (1, 0))
    assert relclose(point_line_distance((0, 0), line), 0.7071067811865476)  # sqrt(2)/2


def test_distance_point_2_2_to_antidiagonal():
    line = line_from_points((0, 1), (1, 0))
    assert relclose(point_line_distance((2, 2), line), 2.1213203435596424)  # 3*sqrt(2)/2


def test_distance_to_vertical_line_x3():
    line = line_from_points((3, 0), (3, 5))
    assert relclose(point_line_distance((0, 0), line), 3.0)


def test_distance_accepts_unnormalized_line():
    # 2y - 2 = 0 即 y = 1，未归一化也应算对。
    assert relclose(point_line_distance((0, 0), (0, 2, -2)), 1.0)
    assert relclose(point_line_distance((5, 3), (0, 2, -2)), 2.0)


def test_point_line_distance_bad_point_inputs():
    line = line_from_points((0, 1), (1, 0))
    with pytest.raises(TypeError):
        point_line_distance((True, 0), line)
    with pytest.raises(TypeError):
        point_line_distance((0, "a"), line)
    with pytest.raises(TypeError):
        point_line_distance((0,), line)


def test_point_line_distance_bad_line_inputs():
    with pytest.raises(TypeError):
        point_line_distance((0, 0), (1, 2))
    with pytest.raises(TypeError):
        point_line_distance((0, 0), (1, "a", 0))
    with pytest.raises(TypeError):
        point_line_distance((0, 0), (True, 1, 0))


# ---------------------------------------------------------------------------
# lines_intersection
# ---------------------------------------------------------------------------


def test_intersection_of_diagonals_is_exact_half():
    l1 = line_from_points((0, 0), (1, 1))
    l2 = line_from_points((0, 1), (1, 0))
    assert lines_intersection(l1, l2) == (0.5, 0.5)


def test_parallel_distinct_lines_return_none():
    l1 = line_from_points((0, 0), (1, 0))
    l2 = line_from_points((0, 1), (1, 1))
    assert lines_intersection(l1, l2) is None


def test_coincident_lines_return_none():
    l1 = line_from_points((0, 0), (2, 2))
    l2 = line_from_points((1, 1), (3, 3))
    assert lines_intersection(l1, l2) is None


def test_intersection_bad_line_inputs():
    good = line_from_points((0, 0), (1, 1))
    with pytest.raises(TypeError):
        lines_intersection(good, (1, 2))
    with pytest.raises(TypeError):
        lines_intersection((1, "a", 0), good)


# ---------------------------------------------------------------------------
# 性质测试
# ---------------------------------------------------------------------------

SAMPLE_POINTS = [
    (0, 0),
    (1, 1),
    (0, 1),
    (1, 0),
    (3, 0),
    (0, 5),
    (-2, 3),
    (2, -1),
    (7, 7),
    (5, -4),
    (3, 5),
    (-1, -1),
]


def _distinct_pairs():
    for i, p in enumerate(SAMPLE_POINTS):
        for q in SAMPLE_POINTS[i + 1 :]:
            if p != q:
                yield p, q


def test_property_unit_normal():
    for p, q in _distinct_pairs():
        a, b, _c = line_from_points(p, q)
        assert abs(a * a + b * b - 1.0) <= 1e-12, (p, q, a, b)


def test_property_defining_points_substitute_back():
    for p, q in _distinct_pairs():
        line = line_from_points(p, q)
        assert abs(point_line_distance(p, line)) <= 1e-9, (p, q)
        assert abs(point_line_distance(q, line)) <= 1e-9, (p, q)


def test_property_intersection_substitutes_back():
    line_pairs = [
        (((0, 0), (1, 1)), ((0, 1), (1, 0))),
        (((0, 0), (1, 0)), ((0, 0), (0, 1))),
        (((0, 0), (2, 1)), ((0, 1), (3, 0))),
        ((SAMPLE_POINTS[4], SAMPLE_POINTS[5]), (SAMPLE_POINTS[6], SAMPLE_POINTS[7])),
        ((SAMPLE_POINTS[8], SAMPLE_POINTS[9]), (SAMPLE_POINTS[10], SAMPLE_POINTS[11])),
    ]
    for (p, q), (r, s) in line_pairs:
        l1 = line_from_points(p, q)
        l2 = line_from_points(r, s)
        point = lines_intersection(l1, l2)
        assert point is not None, ((p, q), (r, s))
        assert abs(point_line_distance(point, l1)) <= 1e-9, ((p, q), (r, s))
        assert abs(point_line_distance(point, l2)) <= 1e-9, ((p, q), (r, s))


def test_sign_pinning_not_negated_form():
    """同一条直线只收 (A, B, C)，(−A, −B, −C) 不是返回形态。"""
    a, b, _c = line_from_points((0, 1), (1, 0))
    assert a > 0 or (a == 0 and b > 0)
    a, b, _c = line_from_points((1, 1), (0, 0))  # 反向取点不改变符号钉死
    assert a > 0
    assert relclose(a, 0.7071067811865476)
    assert relclose(b, -0.7071067811865476)
