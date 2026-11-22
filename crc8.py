"""crc8: CRC-8/SMBUS 校验和。

多项式 0x07、初值 0x00、无反射、无末异或（CRC-8/SMBUS，又称 CRC-8/ITU 或
CRC-8/0x07）。仅用标准库实现，不依赖仓库内其他模块。
"""

_POLY = 0x07


def crc8(data: bytes) -> int:
    """计算 CRC-8/SMBUS 校验和，返回 0-255 的整数。

    对 ``b"123456789"`` 返回 0xF4；空串返回 0。
    """
    crc = 0
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = ((crc << 1) ^ _POLY) & 0xFF
            else:
                crc = (crc << 1) & 0xFF
    return crc
