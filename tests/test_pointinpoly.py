"""Tests for pointinpoly.point_in_polygon — every acceptance point covered."""

import pytest

from pointinpoly import point_in_polygon

SQ = [(0, 0), (10, 0), (10, 10), (0, 10)]          # square, CCW
SQ_CW = list(reversed(SQ))                          # same square, CW
TRI = [(0, 0), (6, 0), (0, 6)]                      # right triangle
L = [(0, 0), (4, 0), (4, 2), (2, 2), (2, 4), (0, 4)]  # concave L-shape


# ---- square: inside / outside ----

def test_square_inside():
    assert point_in_polygon(5, 5, SQ) == "inside"


def test_square_outside_right():
    assert point_in_polygon(15, 5, SQ) == "outside"


def test_square_outside_below_left():
    assert point_in_polygon(-1, -1, SQ) == "outside"


# ---- square: boundary (edge and vertices) ----

def test_square_boundary_left_edge():
    assert point_in_polygon(0, 5, SQ) == "boundary"


def test_square_boundary_bottom_edge():
    assert point_in_polygon(5, 0, SQ) == "boundary"


def test_square_boundary_origin_vertex():
    assert point_in_polygon(0, 0, SQ) == "boundary"


def test_square_boundary_opposite_vertex():
    assert point_in_polygon(10, 10, SQ) == "boundary"


# ---- square CW (reversed) judged the same ----

def test_square_cw_inside():
    assert point_in_polygon(5, 5, SQ_CW) == "inside"


def test_square_cw_outside():
    assert point_in_polygon(20, 5, SQ_CW) == "outside"


# ---- triangle TRI = [(0, 0), (6, 0), (0, 6)] ----

def test_triangle_inside_near_origin():
    assert point_in_polygon(1, 1, TRI) == "inside"


def test_triangle_inside():
    assert point_in_polygon(2, 2, TRI) == "inside"


def test_triangle_boundary_on_hypotenuse():
    # (3, 3) lies on x + y = 6, the hypotenuse
    assert point_in_polygon(3, 3, TRI) == "boundary"


def test_triangle_outside():
    assert point_in_polygon(4, 4, TRI) == "outside"


def test_triangle_boundary_on_leg():
    assert point_in_polygon(0, 3, TRI) == "boundary"


# ---- concave L polygon ----

def test_concave_bottom_left_inside():
    assert point_in_polygon(1, 1, L) == "inside"


def test_concave_top_left_inside():
    assert point_in_polygon(1, 3, L) == "inside"


def test_concave_bottom_right_inside():
    assert point_in_polygon(3, 1, L) == "inside"


def test_concave_notch_outside():
    # (3, 3) sits inside the missing quadrant (the notch)
    assert point_in_polygon(3, 3, L) == "outside"


def test_concave_boundary_vertical_edge():
    assert point_in_polygon(2, 3, L) == "boundary"


def test_concave_boundary_concave_vertex():
    assert point_in_polygon(2, 2, L) == "boundary"


def test_concave_boundary_notch_bottom_edge():
    assert point_in_polygon(3, 2, L) == "boundary"


def test_concave_far_outside():
    assert point_in_polygon(5, 1, L) == "outside"


# ---- input validation: fewer than 3 vertices -> ValueError ----

def test_too_few_vertices_raises():
    with pytest.raises(ValueError):
        point_in_polygon(0, 0, [(0, 0), (1, 1)])


def test_empty_polygon_raises():
    with pytest.raises(ValueError):
        point_in_polygon(0, 0, [])
