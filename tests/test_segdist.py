"""tests/test_segdist.py —— segdist.py 逐条验收要点（第五十六轮 B 单）。"""

import math

import pytest

from segdist import closest_point_on_segment, point_segment_distance

REL_TOL = 1e-9


def test_perpendicular_foot_inside_segment():
    # 垂足在线段内
    assert point_segment_distance(0, 3, -2, 0, 2, 0) == pytest.approx(3.0, rel=REL_TOL)


def test_beyond_endpoint_b():
    # 越过 b 端，取端点距离
    assert point_segment_distance(5, 0, 0, 0, 2, 0) == pytest.approx(3.0, rel=REL_TOL)


def test_beyond_endpoint_a():
    # 越过 a 端，取端点距离
    assert point_segment_distance(-4, 0, 0, 0, 2, 0) == pytest.approx(4.0, rel=REL_TOL)


def test_point_on_segment():
    # 点在线段上
    assert point_segment_distance(1, 0, 0, 0, 2, 0) == pytest.approx(0.0, rel=REL_TOL)


def test_point_at_endpoint_a():
    # 点在端点 a
    assert point_segment_distance(0, 0, 0, 0, 2, 0) == pytest.approx(0.0, rel=REL_TOL)


def test_degenerate_segment_point_distance():
    # 退化线段：点到点距离 3-4-5
    assert point_segment_distance(3, 4, 0, 0, 0, 0) == pytest.approx(5.0, rel=REL_TOL)


def test_degenerate_segment_sqrt2():
    # 退化线段，sqrt(2)
    assert point_segment_distance(0, 0, 1, 1, 1, 1) == pytest.approx(
        1.4142135623730951, rel=REL_TOL
    )


def test_point_on_diagonal_segment():
    # 点在斜线段上
    assert point_segment_distance(2, 2, 0, 0, 4, 4) == pytest.approx(0.0, rel=REL_TOL)


def test_distance_two_sqrt2():
    # 2*sqrt(2)
    assert point_segment_distance(0, 4, 0, 0, 4, 4) == pytest.approx(
        2.8284271247461903, rel=REL_TOL
    )


def test_distance_sqrt18():
    # sqrt(18)
    assert point_segment_distance(6, 3, 0, 0, 3, 0) == pytest.approx(
        4.242640687119286, rel=REL_TOL
    )


def test_closest_point_foot_inside():
    assert closest_point_on_segment(0, 3, -2, 0, 2, 0) == (0.0, 0.0)


def test_closest_point_clamped_to_b():
    # 钳制到 b 端
    assert closest_point_on_segment(5, 0, 0, 0, 2, 0) == (2.0, 0.0)


def test_closest_point_degenerate():
    # 退化线段返回 a
    assert closest_point_on_segment(3, 4, 0, 0, 0, 0) == (0.0, 0.0)


def test_closest_point_clamped_to_a():
    # 钳制到 a 端
    assert closest_point_on_segment(-4, 0, 0, 0, 2, 0) == (0.0, 0.0)


def test_closest_point_on_diagonal():
    assert closest_point_on_segment(0, 4, 0, 0, 4, 4) == (2.0, 2.0)


def test_distance_consistent_with_closest_point():
    # 距离 = 点到最近点的欧氏距离（一致性）
    cases = [
        (0, 3, -2, 0, 2, 0),
        (5, 0, 0, 0, 2, 0),
        (3, 4, 0, 0, 0, 0),
        (0, 4, 0, 0, 4, 4),
        (6, 3, 0, 0, 3, 0),
    ]
    for px, py, ax, ay, bx, by in cases:
        cx, cy = closest_point_on_segment(px, py, ax, ay, bx, by)
        expected = math.hypot(px - cx, py - cy)
        assert point_segment_distance(px, py, ax, ay, bx, by) == pytest.approx(
            expected, rel=REL_TOL
        )


def test_closest_point_lies_on_segment():
    # 最近点必须落在线段参数区间 [0, 1] 上
    for t in (0.0, 0.25, 0.5, 0.75, 1.0, -0.5, 1.5):
        ax, ay, bx, by = 1.0, 2.0, 5.0, 8.0
        px = ax + t * (bx - ax) + 0.3
        py = ay + t * (by - ay) - 0.7
        cx, cy = closest_point_on_segment(px, py, ax, ay, bx, by)
        seg_len_sq = (bx - ax) ** 2 + (by - ay) ** 2
        proj = ((cx - ax) * (bx - ax) + (cy - ay) * (by - ay)) / seg_len_sq
        assert -REL_TOL <= proj <= 1.0 + REL_TOL
