"""Tests for solids.py — volume and surface area of common solids."""

import math

import pytest

from solids import (
    box_surface,
    box_volume,
    cone_surface,
    cone_volume,
    cylinder_surface,
    cylinder_volume,
    pyramid_surface,
    pyramid_volume,
    sphere_surface,
    sphere_volume,
)

TOL = 1e-9


# --- sphere ---------------------------------------------------------------

def test_sphere_volume_1():
    assert sphere_volume(1) == pytest.approx(4.1887902047863905, abs=TOL)


def test_sphere_surface_1():
    assert sphere_surface(1) == pytest.approx(12.566370614359172, abs=TOL)


def test_sphere_volume_3():
    assert sphere_volume(3) == pytest.approx(113.09733552923255, abs=TOL)


def test_sphere_surface_2():
    assert sphere_surface(2) == pytest.approx(50.26548245743669, abs=TOL)


def test_sphere_volume_formula():
    assert sphere_volume(2) == pytest.approx(4.0 * math.pi * 8.0 / 3.0, abs=TOL)


# --- cylinder -------------------------------------------------------------

def test_cylinder_volume_1_1():
    assert cylinder_volume(1, 1) == pytest.approx(3.141592653589793, abs=TOL)


def test_cylinder_volume_2_5():
    assert cylinder_volume(2, 5) == pytest.approx(62.83185307179586, abs=TOL)


def test_cylinder_surface_1_1():
    assert cylinder_surface(1, 1) == pytest.approx(12.566370614359172, abs=TOL)


def test_cylinder_surface_2_5():
    assert cylinder_surface(2, 5) == pytest.approx(87.96459430051421, abs=TOL)


# --- cone -----------------------------------------------------------------

def test_cone_volume_3_4():
    assert cone_volume(3, 4) == pytest.approx(37.69911184307752, abs=TOL)


def test_cone_volume_1_1():
    assert cone_volume(1, 1) == pytest.approx(1.0471975511965976, abs=TOL)


def test_cone_surface_3_4():
    assert cone_surface(3, 4) == pytest.approx(75.39822368615504, abs=TOL)


def test_cone_surface_1_1():
    assert cone_surface(1, 1) == pytest.approx(7.584475591748159, abs=TOL)


# --- box ------------------------------------------------------------------

def test_box_volume_2_3_4():
    assert box_volume(2, 3, 4) == 24


def test_box_surface_2_3_4():
    assert box_surface(2, 3, 4) == 52


# --- square pyramid -------------------------------------------------------

def test_pyramid_volume_2_3():
    assert pyramid_volume(2, 3) == 4


def test_pyramid_volume_6_4():
    assert pyramid_volume(6, 4) == 48


def test_pyramid_surface_6_4():
    assert pyramid_surface(6, 4) == 96


def test_pyramid_surface_2_3():
    assert pyramid_surface(2, 3) == pytest.approx(16.64911064067352, abs=TOL)


# --- dimension validation: ValueError for non-positive ---------------------

def test_sphere_volume_zero():
    with pytest.raises(ValueError):
        sphere_volume(0)


def test_sphere_volume_negative():
    with pytest.raises(ValueError):
        sphere_volume(-1)


def test_cylinder_volume_zero_height():
    with pytest.raises(ValueError):
        cylinder_volume(1, 0)


def test_box_volume_negative_width():
    with pytest.raises(ValueError):
        box_volume(2, -3, 4)


def test_cone_volume_zero_radius():
    with pytest.raises(ValueError):
        cone_volume(0, 1)


# --- dimension validation: TypeError for non-numeric / bool ---------------

def test_cone_surface_string_dimension():
    with pytest.raises(TypeError):
        cone_surface("3", 4)


def test_pyramid_volume_bool_dimension():
    with pytest.raises(TypeError):
        pyramid_volume(True, 3)


def test_sphere_surface_none():
    with pytest.raises(TypeError):
        sphere_surface(None)


def test_bool_rejected_across_functions():
    with pytest.raises(TypeError):
        sphere_volume(True)
    with pytest.raises(TypeError):
        cylinder_surface(False, 1)
    with pytest.raises(TypeError):
        box_surface(1, 1, True)
    with pytest.raises(TypeError):
        pyramid_surface(2, False)


def test_non_numeric_rejected_across_functions():
    with pytest.raises(TypeError):
        sphere_surface("1")
    with pytest.raises(TypeError):
        cylinder_volume(None, 1)
    with pytest.raises(TypeError):
        box_volume(2, [3], 4)
    with pytest.raises(TypeError):
        pyramid_volume(2, "3")


def test_non_positive_other_dimensions():
    with pytest.raises(ValueError):
        sphere_surface(-2)
    with pytest.raises(ValueError):
        cylinder_volume(0, 5)
    with pytest.raises(ValueError):
        cone_surface(3, -4)
    with pytest.raises(ValueError):
        box_surface(-1, 2, 3)
    with pytest.raises(ValueError):
        pyramid_surface(6, 0)


def test_results_are_float():
    assert isinstance(sphere_volume(1), float)
    assert isinstance(cylinder_surface(1, 1), float)
    assert isinstance(cone_volume(1, 1), float)
    assert isinstance(box_volume(2, 3, 4), float)
    assert isinstance(pyramid_surface(6, 4), float)
