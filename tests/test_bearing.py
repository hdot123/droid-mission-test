"""Tests for bearing.py: spherical initial bearing and destination point."""

import math

import pytest

from bearing import EARTH_RADIUS_KM, destination_point, initial_bearing

REL_TOL = 1e-6


def haversine_distance_km(lat1, lon1, lat2, lon2):
    """Great-circle distance in km using the haversine formula (independent check)."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))


class TestInitialBearing:
    def test_north_is_zero(self):
        assert initial_bearing(0, 0, 1, 0) == 0.0

    def test_east_is_90(self):
        assert initial_bearing(0, 0, 0, 1) == pytest.approx(90.0, rel=REL_TOL)

    def test_south_is_180(self):
        assert initial_bearing(0, 0, -1, 0) == pytest.approx(180.0, rel=REL_TOL)

    def test_west_is_270(self):
        assert initial_bearing(0, 0, 0, -1) == pytest.approx(270.0, rel=REL_TOL)

    def test_identical_points_return_zero(self):
        assert initial_bearing(40.0, -73.0, 40.0, -73.0) == 0.0

    def test_london_to_paris(self):
        # Known city pair: absolute tolerance 0.02 degrees.
        assert initial_bearing(51.5074, -0.1278, 48.8566, 2.3522) == pytest.approx(
            148.55, abs=0.02
        )

    def test_new_york_to_london(self):
        # Known city pair: absolute tolerance 0.05 degrees.
        assert initial_bearing(40.7128, -74.0060, 51.5074, -0.1278) == pytest.approx(
            51.7, abs=0.05
        )

    def test_latitude_above_90_raises(self):
        with pytest.raises(ValueError):
            initial_bearing(91, 0, 0, 0)

    def test_latitude_below_neg90_raises(self):
        with pytest.raises(ValueError):
            initial_bearing(0, 0, -90.5, 0)


class TestDestinationPoint:
    def test_quarter_turn_east_equator(self):
        lat, lon = destination_point(0, 0, 90, EARTH_RADIUS_KM * math.pi / 2)
        assert lat == pytest.approx(0.0, rel=REL_TOL, abs=1e-9)
        assert lon == pytest.approx(90.0, rel=REL_TOL)

    def test_longitude_crosses_180_to_negative_side(self):
        _, lon = destination_point(0, 179.0, 90, 300.0)
        # Crosses the antimeridian: normalized to the negative side of [-180, 180).
        assert -180.0 <= lon < 0.0

    def test_negative_distance_raises(self):
        with pytest.raises(ValueError):
            destination_point(0, 0, 0, -1)

    def test_latitude_out_of_range_raises(self):
        with pytest.raises(ValueError):
            destination_point(91, 0, 0, 0)

    @pytest.mark.parametrize(
        "lat,lon,bearing,distance",
        [
            (0.0, 0.0, 0.0, 1000.0),
            (51.5074, -0.1278, 148.55, 343.5),
            (-33.8688, 151.2093, 275.0, 12000.0),
            (40.7128, -74.0060, 51.7, 5570.0),
            (89.0, 45.0, 135.0, 6371.0088),
        ],
    )
    def test_round_trip_distance_and_bearing(self, lat, lon, bearing, distance):
        dest_lat, dest_lon = destination_point(lat, lon, bearing, distance)
        # Great-circle distance recovers the original distance.
        recovered = haversine_distance_km(lat, lon, dest_lat, dest_lon)
        assert recovered == pytest.approx(distance, rel=REL_TOL)
        # Bearing recomputed from start to destination recovers the original bearing.
        recovered_bearing = initial_bearing(lat, lon, dest_lat, dest_lon)
        assert recovered_bearing == pytest.approx(bearing % 360.0, rel=REL_TOL)

    def test_zero_distance_returns_same_point(self):
        lat, lon = destination_point(12.34, 56.78, 45.0, 0.0)
        assert lat == pytest.approx(12.34, rel=REL_TOL)
        assert lon == pytest.approx(56.78, rel=REL_TOL)
