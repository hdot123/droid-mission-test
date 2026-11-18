"""CRC-16/CCITT-FALSE checksum."""

_POLY = 0x1021
_INIT = 0xFFFF


def compute(data: bytes) -> int:
    """Compute CRC-16/CCITT-FALSE over ``data``.

    Parameters: polynomial 0x1021, initial value 0xFFFF, no reflection,
    output xor 0x0000. Empty input returns 0xFFFF.
    """
    crc = _INIT
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ _POLY) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc
