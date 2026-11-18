"""Gray code encode/decode (standard reflected binary Gray code)."""


def encode(n: int) -> int:
    """Encode non-negative integer n as its Gray code: n ^ (n >> 1)."""
    if n < 0:
        raise ValueError("n must be non-negative")
    return n ^ (n >> 1)


def decode(g: int) -> int:
    """Decode a Gray code value back to its non-negative integer."""
    if g < 0:
        raise ValueError("g must be non-negative")
    n = 0
    while g:
        n ^= g
        g >>= 1
    return n
