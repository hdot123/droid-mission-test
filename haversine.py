"""haversine: 球面大圆距离（第四十一轮 · 常规组四）。

`haversine(lat1, lon1, lat2, lon2)` 返回两点间的大圆距离，单位 km，
地球半径 R = 6371.0 km。纬度超出 [-90, 90] 或经度超出 [-180, 180]
抛 ValueError。只依赖标准库 math。
"""

import math

_EARTH_RADIUS_KM = 6371.0


def _check_range(value, low, high, label):
    if not low <= value <= high:
        raise ValueError("%s out of range: %r" % (label, value))


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """两点间球面大圆距离（km），纬度越界或经度越界抛 ValueError。"""
    _check_range(lat1, -90.0, 90.0, "latitude")
    _check_range(lat2, -90.0, 90.0, "latitude")
    _check_range(lon1, -180.0, 180.0, "longitude")
    _check_range(lon2, -180.0, 180.0, "longitude")

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    sin_half_d_phi = math.sin(d_phi / 2.0)
    sin_half_d_lambda = math.sin(d_lambda / 2.0)
    a = (
        sin_half_d_phi * sin_half_d_phi
        + math.cos(phi1) * math.cos(phi2) * sin_half_d_lambda * sin_half_d_lambda
    )
    # 浮点误差下 a 可能略超出 [0, 1]，夹紧后再开方。
    if a < 0.0:
        a = 0.0
    elif a > 1.0:
        a = 1.0
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return _EARTH_RADIUS_KM * c
