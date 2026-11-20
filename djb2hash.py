"""djb2 string hashing with 32-bit wraparound.

Standard library only; no cross-module imports.
"""

__all__ = ["djb2", "djb2_bytes"]

_MASK = 0xFFFFFFFF


def djb2(text: str) -> int:
    """Hash a string by iterating over its UTF-8 bytes.

    h starts at 5381; for each byte: h = (h * 33 + byte) & 0xFFFFFFFF.
    Non-str input raises TypeError.
    """
    if not isinstance(text, str):
        raise TypeError(f"text must be str, not {type(text).__name__}")
    return djb2_bytes(text.encode("utf-8"))


def djb2_bytes(data: bytes) -> int:
    """Apply the djb2 algorithm directly to a byte sequence.

    Accepts bytes or bytearray; anything else raises TypeError.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError(
            f"data must be bytes or bytearray, not {type(data).__name__}"
        )
    h = 5381
    for byte in data:
        h = ((h * 33) + byte) & _MASK
    return h
