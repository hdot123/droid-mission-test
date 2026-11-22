"""crc32: CRC-32/IEEE 校验（自实现，不依赖 zlib.crc32）。

多项式 0xEDB88320（反射式）、初值 0xFFFFFFFF、末异或 0xFFFFFFFF。
"""

_TABLE = []
for _i in range(256):
    _crc = _i
    for _ in range(8):
        _crc = (_crc >> 1) ^ (0xEDB88320 if _crc & 1 else 0)
    _TABLE.append(_crc)


def crc32(data: bytes) -> int:
    """计算 CRC-32/IEEE 校验值，返回 0–4294967295 的整数。

    非 bytes 输入抛 TypeError。
    """
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes, got %s" % type(data).__name__)
    crc = 0xFFFFFFFF
    for byte in data:
        crc = _TABLE[(crc ^ byte) & 0xFF] ^ (crc >> 8)
    return (crc ^ 0xFFFFFFFF) & 0xFFFFFFFF
