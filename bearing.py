"""Spherical initial bearing and destination point computation (great circle).

Earth radius is pinned at 6371.0088 km. Standard library only.
"""

import math

EARTH_RADIUS_KM = 6371.0088


def _validate_latitude(lat: float) -> None:
    if not -90.0 <= lat <= 90.0:
        raise ValueError(f"latitude out of range [-90, 90]: {lat}")


def _normalize_longitude(lon: float) -> float:
    """Normalize a longitude in degrees to [-180, 180)."""
    return (lon + 180.0) % 360.0 - 180.0


def initial_bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Spherical initial (forward) azimuth from point 1 to point 2 in degrees.

    Result is normalized to [0, 360). Identical points return 0.0.
    Raises ValueError if either latitude is outside +/-90.
    """
    _validate_latitude(lat1)
    _validate_latitude(lat2)
    if lat1 == lat2 and lon1 == lon2:
        return 0.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_lon = math.radians(lon2 - lon1)
    y = math.sin(delta_lon) * math.cos(phi2)
    x = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(delta_lon)
    theta = math.degrees(math.atan2(y, x))
    return theta % 360.0


def destination_point(
    lat: float, lon: float, bearing_deg: float, distance_km: float
) -> tuple[float, float]:
    """Endpoint (lat, lon) after traveling distance_km along bearing_deg.

    Earth radius is pinned at 6371.0088 km. The resulting longitude is
    normalized to [-180, 180). Raises ValueError if the latitude is outside
    +/-90 or distance_km is negative.
    """
    _validate_latitude(lat)
    if distance_km < 0:
        raise ValueError(f"distance_km must be non-negative: {distance_km}")
    angular = distance_km / EARTH_RADIUS_KM
    phi1 = math.radians(lat)
    lambda1 = math.radians(lon)
    theta = math.radians(bearing_deg)
    sin_phi2 = math.sin(phi1) * math.cos(angular) + math.cos(phi1) * math.sin(angular) * math.cos(theta)
    phi2 = math.asin(sin_phi2)
    lambda2 = lambda1 + math.atan2(
        math.sin(theta) * math.sin(angular) * math.cos(phi1),
        math.cos(angular) - math.sin(phi1) * sin_phi2,
    )
    return math.degrees(phi2), _normalize_longitude(math.degrees(lambda2))
