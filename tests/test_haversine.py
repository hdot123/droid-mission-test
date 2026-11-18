import pytest

from haversine import haversine


def test_same_point_is_zero():
    assert haversine(0, 0, 0, 0) == 0.0


def test_one_degree_longitude_at_equator():
    assert abs(haversine(0, 0, 0, 1) - 111.1949266) < 0.001


def test_one_degree_latitude_at_meridian():
    assert abs(haversine(0, 0, 1, 0) - 111.1949266) < 0.001


def test_half_world_along_equator():
    assert abs(haversine(0, 0, 0, 180) - 20015.0867960) < 0.001


def test_pole_to_equator():
    assert abs(haversine(90, 0, 0, 0) - 10007.5433980) < 0.001


def test_antipodal_diagonal():
    assert abs(haversine(45, 0, -45, 180) - 20015.0867960) < 0.001


def test_quarter_world_along_equator():
    assert abs(haversine(0, 0, 0, 90) - 10007.5433980) < 0.001


def test_new_york_to_london():
    assert abs(haversine(40.7128, -74.0060, 51.5074, -0.1278) - 5570.2221797) < 0.01


def test_sydney_to_tokyo():
    assert abs(haversine(-33.8688, 151.2093, 35.6762, 139.6503) - 7825.8186165) < 0.01


def test_latitude_out_of_range_raises():
    with pytest.raises(ValueError):
        haversine(91, 0, 0, 0)
    with pytest.raises(ValueError):
        haversine(-91, 0, 0, 0)


def test_longitude_out_of_range_raises():
    with pytest.raises(ValueError):
        haversine(0, 181, 0, 0)
    with pytest.raises(ValueError):
        haversine(0, 0, 0, -181)
