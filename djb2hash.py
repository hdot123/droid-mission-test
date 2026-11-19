"""djb2 string hashing with 32-bit wraparound."""

__all__ = ["djb2", "djb2_bytes"]

_MASK32 = 0xFFFFFFFF
_INITIAL = 5381


def _hash_bytes(data) -> int:
    h = _INITIAL
    for byte in data:
        h = ((h * 33) + byte) & _MASK32
    return h


def djb2(text: str) -> int:
    """Hash ``text`` with djb2 over its UTF-8 bytes, wrapping at 32 bits.

    Raises TypeError if ``text`` is not a ``str``.
    """
    if not isinstance(text, str):
        raise TypeError("text must be str, got %s" % type(text).__name__)
    return _hash_bytes(text.encode("utf-8"))


def djb2_bytes(data: bytes) -> int:
    """Hash a byte sequence directly with the djb2 algorithm.

    Accepts ``bytes`` or ``bytearray``; anything else (including ``str``)
    raises TypeError.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError(
            "data must be bytes or bytearray, got %s" % type(data).__name__
        )
    return _hash_bytes(data)
