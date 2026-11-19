"""djb2 string hashing with 32-bit wraparound.

djb2 is a simple non-cryptographic hash: start with h = 5381, then for each
byte b of the input compute h = (h * 33 + b) mod 2**32. Only the standard
library is used; this module does not import from any other deliverable.
"""

_MASK = 0xFFFFFFFF  # 2**32 - 1, keeps the hash within 32 bits.


def _djb2_from_bytes(data) -> int:
    h = 5381
    for byte in data:
        h = ((h * 33) + byte) & _MASK
    return h


def djb2(text: str) -> int:
    """Hash ``text`` by feeding its UTF-8 bytes through djb2 (32-bit)."""
    if not isinstance(text, str):
        raise TypeError(f"expected str, got {type(text).__name__}")
    return _djb2_from_bytes(text.encode("utf-8"))


def djb2_bytes(data) -> int:
    """Hash a bytes-like sequence directly with djb2 (32-bit)."""
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError(f"expected bytes or bytearray, got {type(data).__name__}")
    return _djb2_from_bytes(data)
