"""Strict IPv4 address helpers: validation, integer conversion, RFC 1918.

Standard library only; no third-party dependencies.

Public API:
    is_valid_ipv4(s) -- strict IPv4 syntax check (bool, never raises)
    to_int(s)        -- valid IPv4 -> 32-bit int (invalid raises ValueError)
    from_int(n)      -- 32-bit int -> IPv4 string (bad input raises ValueError)
    is_private(s)    -- RFC 1918 private-address test (invalid raises ValueError)

Strict syntax: exactly four decimal octets, each 0-255, no leading zeros
("0" itself is allowed), no spaces.
"""

__all__ = ["is_valid_ipv4", "to_int", "from_int", "is_private"]


def is_valid_ipv4(s):
    """Return True when *s* is a strict IPv4 address; never raises."""
    if not isinstance(s, str):
        return False
    parts = s.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isascii() or not part.isdigit():
            return False
        if len(part) > 1 and part[0] == "0":
            return False
        if int(part) > 255:
            return False
    return True


def to_int(s):
    """Convert a valid IPv4 address to its 32-bit integer value.

    Raises ValueError for anything that is not a strict IPv4 address.
    """
    if not is_valid_ipv4(s):
        raise ValueError(f"invalid IPv4 address: {s!r}")
    a, b, c, d = (int(part) for part in s.split("."))
    return (a << 24) | (b << 16) | (c << 8) | d


def from_int(n):
    """Convert an integer in 0..2**32-1 to its IPv4 address string.

    Raises ValueError for non-int input (bool included) or out-of-range
    values.
    """
    if isinstance(n, bool) or not isinstance(n, int) or not 0 <= n <= 0xFFFFFFFF:
        raise ValueError(f"expected int in 0..2**32-1, got {n!r}")
    return f"{(n >> 24) & 0xFF}.{(n >> 16) & 0xFF}.{(n >> 8) & 0xFF}.{n & 0xFF}"


def is_private(s):
    """Return True when *s* is a valid RFC 1918 private address.

    Blocks: 10/8, 172.16/12, 192.168/16. Raises ValueError for invalid
    addresses.
    """
    if not is_valid_ipv4(s):
        raise ValueError(f"invalid IPv4 address: {s!r}")
    first, second = (int(part) for part in s.split(".")[:2])
    if first == 10:
        return True
    if first == 172 and 16 <= second <= 31:
        return True
    if first == 192 and second == 168:
        return True
    return False
