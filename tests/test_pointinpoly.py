import pytest

from pointinpoly import point_in_polygon

SQ = [(0, 0), (10, 0), (10, 10), (0, 10)]
TRI = [(0, 0), (6, 0), (0, 6)]
L = [(0, 0), (4, 0), (4, 2), (2, 2), (2, 4), (0, 4)]


def test_square_inside_outside():
    assert point_in_polygon(5, 5, SQ) == "inside"
    assert point_in_polygon(15, 5, SQ) == "outside"
    assert point_in_polygon(-1, -1, SQ) == "outside"


def test_square_boundary_edges_and_vertices():
    assert point_in_polygon(0, 5, SQ) == "boundary"
    assert point_in_polygon(5, 0, SQ) == "boundary"
    assert point_in_polygon(0, 0, SQ) == "boundary"
    assert point_in_polygon(10, 10, SQ) == "boundary"


def test_square_cw_reversed_same_judgement():
    sq_cw = list(reversed(SQ))
    assert point_in_polygon(5, 5, sq_cw) == "inside"
    assert point_in_polygon(20, 5, sq_cw) == "outside"


def test_triangle_inside_outside_boundary():
    assert point_in_polygon(1, 1, TRI) == "inside"
    assert point_in_polygon(2, 2, TRI) == "inside"
    assert point_in_polygon(3, 3, TRI) == "boundary"  # on the hypotenuse
    assert point_in_polygon(4, 4, TRI) == "outside"
    assert point_in_polygon(0, 3, TRI) == "boundary"


def test_concave_inside():
    assert point_in_polygon(1, 1, L) == "inside"
    assert point_in_polygon(1, 3, L) == "inside"
    assert point_in_polygon(3, 1, L) == "inside"


def test_concave_outside():
    assert point_in_polygon(3, 3, L) == "outside"  # inside the notch
    assert point_in_polygon(5, 1, L) == "outside"


def test_concave_boundary():
    assert point_in_polygon(2, 3, L) == "boundary"
    assert point_in_polygon(2, 2, L) == "boundary"  # concave vertex
    assert point_in_polygon(3, 2, L) == "boundary"


def test_too_few_vertices_raises():
    with pytest.raises(ValueError):
        point_in_polygon(0, 0, [(0, 0), (1, 1)])
    with pytest.raises(ValueError):
        point_in_polygon(0, 0, [])
