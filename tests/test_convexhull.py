import pytest

from convexhull import convex_hull


def test_square():
    assert convex_hull([(0, 0), (1, 0), (1, 1), (0, 1)]) == [
        (0, 0),
        (1, 0),
        (1, 1),
        (0, 1),
    ]


def test_square_with_interior_point():
    assert convex_hull(
        [(0, 0), (1, 0), (1, 1), (0, 1), (0.5, 0.5)]
    ) == [(0, 0), (1, 0), (1, 1), (0, 1)]


def test_square_with_edge_point():
    assert convex_hull(
        [(0, 0), (1, 0), (1, 1), (0, 1), (0.5, 0)]
    ) == [(0, 0), (1, 0), (1, 1), (0, 1)]


def test_triangle():
    assert convex_hull([(0, 0), (2, 0), (1, 2)]) == [(0, 0), (2, 0), (1, 2)]


def test_collinear_points_keep_endpoints_only():
    assert convex_hull([(0, 0), (1, 1), (2, 2), (3, 3)]) == [(0, 0), (3, 3)]


def test_duplicate_points_removed_first():
    assert convex_hull(
        [(0, 0), (0, 0), (1, 0), (1, 1), (0, 1)]
    ) == [(0, 0), (1, 0), (1, 1), (0, 1)]


def test_polygon_with_interior_point():
    assert convex_hull(
        [(0, 0), (2, 0), (3, 1), (1, 3), (-1, 1), (1, 1)]
    ) == [(-1, 1), (0, 0), (2, 0), (3, 1), (1, 3)]


def test_single_point():
    assert convex_hull([(5, 5)]) == [(5, 5)]


def test_two_points():
    assert convex_hull([(1, 2), (3, 4)]) == [(1, 2), (3, 4)]


def test_empty():
    assert convex_hull([]) == []


def test_float_coordinates():
    assert convex_hull(
        [(0.0, 0.0), (2.5, 0.0), (0.0, 2.5)]
    ) == [(0.0, 0.0), (2.5, 0.0), (0.0, 2.5)]


def test_fewer_than_three_returns_sorted_dedup():
    assert convex_hull([(3, 4), (1, 2)]) == [(1, 2), (3, 4)]
    assert convex_hull([(2, 2), (2, 2)]) == [(2, 2)]


def test_tuple_input_accepted():
    assert convex_hull(((0, 0), (1, 0), (0, 1))) == [(0, 0), (1, 0), (0, 1)]


def test_points_not_list_or_tuple_raises_type_error():
    with pytest.raises(TypeError):
        convex_hull("abc")
    with pytest.raises(TypeError):
        convex_hull(42)


def test_point_not_two_tuple_raises_value_error():
    with pytest.raises(ValueError):
        convex_hull([(0, 0, 0)])


def test_non_numeric_coordinate_raises_type_error():
    with pytest.raises(TypeError):
        convex_hull([(0, "a")])
    with pytest.raises(TypeError):
        convex_hull([(0.0, None)])


def test_bool_coordinate_raises_type_error():
    with pytest.raises(TypeError):
        convex_hull([(0, True)])
    with pytest.raises(TypeError):
        convex_hull([(False, 0)])
