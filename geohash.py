"""geohash: Geohash 编解码（纬经交织二分，每 5 比特一字）。

字母表逐字为 ``0123456789bcdefghjkmnpqrstuvwxyz``（无 a、i、l、o）。
编码时经度比特居先交错；坐标恰在区间中点时取上半区（>= 中点记 1）。
解码返回单元中心 (lat, lon)，而非编码时的原坐标——原坐标只保证落在
本单元内。本模块只用标准库。
"""

_BASE32 = "0123456789bcdefghjkmnpqrstuvwxyz"
_ALPHABET = frozenset(_BASE32)
_INDEX = {ch: i for i, ch in enumerate(_BASE32)}

_LAT_MIN, _LAT_MAX = -90.0, 90.0
_LON_MIN, _LON_MAX = -180.0, 180.0
_MIN_PRECISION = 1
_MAX_PRECISION = 12


def _is_number(v):
    """数值判定：bool 不算数值（bool 是 int 子类，须显式排除）。"""
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def geohash_encode(lat, lon, precision=12) -> str:
    """把 (lat, lon) 编码为 precision 个字符的 geohash。

    经度区间 [-180, 180]、纬度区间 [-90, 90]，逐比特二分、经度比特
    居先交错，每 5 比特成一个字符。lat/lon 越界或 precision 不在
    [1, 12] 抛 ValueError；lat/lon 非数值、precision 非 int（含 bool）
    抛 TypeError。
    """
    if not _is_number(lat) or not _is_number(lon):
        raise TypeError(
            "lat/lon must be numeric, got %r, %r" % (lat, lon)
        )
    if isinstance(precision, bool) or not isinstance(precision, int):
        raise TypeError("precision must be int, got %r" % (precision,))
    if not (_LAT_MIN <= lat <= _LAT_MAX):
        raise ValueError("lat out of range [-90, 90]: %r" % (lat,))
    if not (_LON_MIN <= lon <= _LON_MAX):
        raise ValueError("lon out of range [-180, 180]: %r" % (lon,))
    if not (_MIN_PRECISION <= precision <= _MAX_PRECISION):
        raise ValueError(
            "precision out of range [%d, %d]: %r"
            % (_MIN_PRECISION, _MAX_PRECISION, precision)
        )

    lat_lo, lat_hi = _LAT_MIN, _LAT_MAX
    lon_lo, lon_hi = _LON_MIN, _LON_MAX
    total_bits = 5 * precision
    bits = []
    for i in range(total_bits):
        if i % 2 == 0:
            # 经度比特居先
            mid = (lon_lo + lon_hi) / 2.0
            if lon >= mid:  # 恰在中点取上半区
                bits.append(1)
                lon_lo = mid
            else:
                bits.append(0)
                lon_hi = mid
        else:
            mid = (lat_lo + lat_hi) / 2.0
            if lat >= mid:
                bits.append(1)
                lat_lo = mid
            else:
                bits.append(0)
                lat_hi = mid

    out = []
    for start in range(0, total_bits, 5):
        idx = 0
        for b in bits[start:start + 5]:
            idx = (idx << 1) | b
        out.append(_BASE32[idx])
    return "".join(out)


def geohash_decode(code: str) -> tuple[float, float]:
    """解 geohash 串，返回该单元中心 (lat, lon)。

    code 非 str（含 bool）抛 TypeError；空串或含字母表外字符抛
    ValueError。
    """
    if isinstance(code, bool) or not isinstance(code, str):
        raise TypeError("code must be str, got %r" % (code,))
    if not code:
        raise ValueError("code must be non-empty")
    if any(ch not in _ALPHABET for ch in code):
        raise ValueError(
            "code contains character outside geohash alphabet: %r" % (code,)
        )

    nbits = 5 * len(code)
    lon_bits = (nbits + 1) // 2  # 经度比特居先，奇数位时经度多一比特
    lat_bits = nbits // 2
    lat_i = 0
    lon_i = 0
    for pos, ch in enumerate(code):
        v = _INDEX[ch]
        for j in range(5):
            bit = (v >> (4 - j)) & 1
            k = pos * 5 + j
            if k % 2 == 0:
                lon_i = (lon_i << 1) | bit
            else:
                lat_i = (lat_i << 1) | bit

    lat = _LAT_MIN + (lat_i + 0.5) * 180.0 / (1 << lat_bits)
    lon = _LON_MIN + (lon_i + 0.5) * 360.0 / (1 << lon_bits)
    return (lat, lon)
