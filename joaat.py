"""Jenkins one-at-a-time (joaat) 32-bit hash.

Algorithm, verbatim:
  h starts at 0; for each byte b: h += b, h += h << 10, h ^= h >> 6;
  finalization: h += h << 3, h ^= h >> 11, h += h << 15.
Every step wraps to 32 bits (& 0xFFFFFFFF) throughout; the result is in
[0, 2**32).
"""

__all__ = ["joaat_hash"]

_MASK = 0xFFFFFFFF


def joaat_hash(data: bytes) -> int:
    """Return the Jenkins one-at-a-time 32-bit hash of ``data``.

    ``data`` must be exactly bytes; anything else (str, int, list,
    bytearray, ...) raises TypeError.
    """
    if not isinstance(data, bytes):
        raise TypeError(
            "joaat_hash() requires bytes, got %s" % type(data).__name__
        )
    h = 0
    for b in data:
        h = (h + b) & _MASK
        h = (h + (h << 10)) & _MASK
        h = (h ^ (h >> 6)) & _MASK
    # Finalization: the three steps below must not be omitted, and the
    # wrap must happen step by step (truncating only at the end differs).
    h = (h + (h << 3)) & _MASK
    h = (h ^ (h >> 11)) & _MASK
    h = (h + (h << 15)) & _MASK
    return h
