"""MurmurHash3 32-bit x86 variant (standard library only)."""

__all__ = ["murmur3_32"]

_MASK = 0xFFFFFFFF
_C1 = 0xCC9E2D51
_C2 = 0x1B873593
_F1 = 0x85EBCA6B
_F2 = 0xC2B2AE35


def _rotl(x: int, r: int) -> int:
    x &= _MASK
    return ((x << r) | (x >> (32 - r))) & _MASK


def _fmix32(h: int) -> int:
    h &= _MASK
    h ^= h >> 16
    h = (h * _F1) & _MASK
    h ^= h >> 13
    h = (h * _F2) & _MASK
    h ^= h >> 16
    return h & _MASK


def murmur3_32(data: bytes, seed: int = 0) -> int:
    """Compute the MurmurHash3 x86_32 hash of *data* with *seed*.

    Returns an int in 0-4294967295.

    Raises TypeError for non-bytes data or non-int seed, and ValueError for
    a seed outside 0-4294967295.
    """
    if not isinstance(data, bytes):
        raise TypeError(
            "data must be bytes, not %s" % type(data).__name__
        )
    if not isinstance(seed, int):
        raise TypeError(
            "seed must be int, not %s" % type(seed).__name__
        )
    if seed < 0 or seed > _MASK:
        raise ValueError("seed must be in range 0-4294967295")

    length = len(data)
    h = seed & _MASK
    nblocks = length // 4

    for i in range(nblocks):
        k = int.from_bytes(data[i * 4 : i * 4 + 4], "little")
        k = (k * _C1) & _MASK
        k = _rotl(k, 15)
        k = (k * _C2) & _MASK
        h ^= k
        h = _rotl(h, 13)
        h = (h * 5 + 0xE6546B64) & _MASK

    tail = data[nblocks * 4 :]
    if tail:
        k = int.from_bytes(tail, "little")
        k = (k * _C1) & _MASK
        k = _rotl(k, 15)
        k = (k * _C2) & _MASK
        h ^= k

    h ^= length
    return _fmix32(h)
