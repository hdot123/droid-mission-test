"""Tests for polygonarea: shoelace area and closed perimeter."""

import pytest

from polygonarea import polygon_area, polygon_perimeter


# --- polygon_area acceptance points ---

def test_area_unit_square_ccw():
    assert polygon_area([(0, 0), (1, 0), (1, 1), (0, 1)]) == 1.0


def test_area_unit_square_cw():
    assert polygon_area([(0, 0), (0, 1), (1, 1), (1, 0)]) == -1.0


def test_area_triangle():
    assert polygon_area([(0, 0), (4, 0), (0, 3)]) == 6.0


def test_area_rectangle():
    assert polygon_area([(0, 0), (3, 0), (3, 2), (0, 2)]) == 6.0


def test_area_collinear_zero():
    assert polygon_area([(0, 0), (1, 1), (2, 2)]) == 0.0


def test_area_too_few_points():
    with pytest.raises(ValueError):
        polygon_area([(0, 0), (1, 0)])


def test_area_non_numeric_input():
    with pytest.raises(TypeError):
        polygon_area("x")


# --- polygon_perimeter acceptance points ---

def test_perimeter_unit_square():
    assert polygon_perimeter([(0, 0), (1, 0), (1, 1), (0, 1)]) == 4.0


def test_perimeter_triangle():
    assert polygon_perimeter([(0, 0), (4, 0), (0, 3)]) == 12.0


def test_perimeter_rectangle():
    assert polygon_perimeter([(0, 0), (3, 0), (3, 2), (0, 2)]) == 10.0


def test_perimeter_too_few_points():
    with pytest.raises(ValueError):
        polygon_perimeter([(0, 0)])


def test_perimeter_non_numeric_point():
    with pytest.raises(TypeError):
        polygon_perimeter([(0, 0), ("a", 1)])
