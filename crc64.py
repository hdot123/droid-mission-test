"""CRC-64/XZ (ECMA) checksum.

Reflected polynomial 0xC96C5795D7870F42, initial value
0xFFFFFFFFFFFFFFFF, final XOR 0xFFFFFFFFFFFFFFFF.
"""

_POLY = 0xC96C5795D7870F42
_INIT = 0xFFFFFFFFFFFFFFFF
_XOROUT = 0xFFFFFFFFFFFFFFFF


def _build_table() -> list[int]:
    table = []
    for i in range(256):
        crc = i
        for _ in range(8):
            crc = (crc >> 1) ^ (_POLY if crc & 1 else 0)
        table.append(crc & 0xFFFFFFFFFFFFFFFF)
    return table


_TABLE = _build_table()


def crc64(data: bytes) -> int:
    """Return the CRC-64/XZ checksum of *data* as an integer in [0, 2**64)."""
    if not isinstance(data, bytes):
        raise TypeError(f"data must be bytes, not {type(data).__name__}")
    crc = _INIT
    for byte in data:
        crc = (crc >> 8) ^ _TABLE[(crc ^ byte) & 0xFF]
    return (crc ^ _XOROUT) & 0xFFFFFFFFFFFFFFFF
