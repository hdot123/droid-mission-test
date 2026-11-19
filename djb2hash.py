"""djb2 string hashing with 32-bit wraparound (standard library only)."""

__all__ = ["djb2", "djb2_bytes"]

_MASK = 0xFFFFFFFF
_SEED = 5381


def _hash_bytes(data) -> int:
    h = _SEED
    for byte in data:
        h = (h * 33 + byte) & _MASK
    return h


def djb2(text: str) -> int:
    """Return the 32-bit djb2 hash of ``text``'s UTF-8 bytes.

    h starts at 5381; for each byte, h = (h * 33 + byte) mod 2**32.

    Raises TypeError if ``text`` is not a str.
    """
    if not isinstance(text, str):
        raise TypeError(
            f"djb2() expected str, got {type(text).__name__}"
        )
    return _hash_bytes(text.encode("utf-8"))


def djb2_bytes(data: bytes) -> int:
    """Return the 32-bit djb2 hash applied directly to a byte sequence.

    Raises TypeError if ``data`` is not bytes or bytearray.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError(
            f"djb2_bytes() expected bytes or bytearray, got {type(data).__name__}"
        )
    return _hash_bytes(data)
