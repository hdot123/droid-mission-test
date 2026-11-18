"""CRC-8/SMBUS checksum (polynomial 0x07, init 0x00, no reflection, no final XOR)."""

_POLYNOMIAL = 0x07


def crc8(data):
    """Return the CRC-8/SMBUS checksum of ``data`` as an int in 0-255."""
    crc = 0x00
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = ((crc << 1) ^ _POLYNOMIAL) & 0xFF
            else:
                crc = (crc << 1) & 0xFF
    return crc


def crc8_hex(data):
    """Return the CRC-8/SMBUS checksum of ``data`` as two uppercase hex chars."""
    return "%02X" % crc8(data)
