"""CRC-16/CCITT-FALSE checksum (polynomial 0x1021, init 0xFFFF)."""

_POLY = 0x1021
_INIT = 0xFFFF


def crc16(data: bytes) -> int:
    """Return the CRC-16/CCITT-FALSE checksum of ``data`` as 0..65535."""
    crc = _INIT
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ _POLY) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc
