"""Adler-32 checksum (self-implementation, no zlib)."""

MOD = 65521


def adler32(data: bytes) -> int:
    """Compute the Adler-32 checksum of ``data``.

    ``data`` must be a bytes-like object; any other type raises TypeError.
    """
    if not isinstance(data, (bytes, bytearray, memoryview)):
        raise TypeError(
            "adler32() argument must be bytes-like, not %s" % type(data).__name__
        )
    a = 1
    b = 0
    for byte in bytes(data):
        a = (a + byte) % MOD
        b = (b + a) % MOD
    return (b << 16) | a
