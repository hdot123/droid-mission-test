"""sdbm string hash (standard library only, no intra-batch imports)."""

_MASK32 = 0xFFFFFFFF


def sdbm_hash(text: str) -> int:
    """Compute the sdbm hash of ``text`` over its UTF-8 byte stream.

    Iterates each byte ``b`` as ``h = b + (h << 6) + (h << 16) - h``
    (equivalent to ``h = h * 65599 + b``) with a 32-bit unsigned
    truncation after every step. The empty string hashes to 0.

    Raises ``TypeError`` for non-``str`` input.
    """
    if not isinstance(text, str):
        raise TypeError(
            "sdbm_hash() expected str, got %s" % type(text).__name__
        )
    h = 0
    for b in text.encode("utf-8"):
        h = (b + (h << 6) + (h << 16) - h) & _MASK32
    return h


def sdbm_hex(text: str) -> str:
    """Return :func:`sdbm_hash` as an 8-digit lowercase hex string."""
    return format(sdbm_hash(text), "08x")
