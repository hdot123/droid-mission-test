"""Strict IPv4 address utilities (Python standard library only).

Functions:
    is_valid_ipv4(s)  -- strict validity check; returns bool, never raises
    to_int(s)         -- dotted quad -> 32-bit int; ValueError if invalid
    from_int(n)       -- 32-bit int -> dotted quad; ValueError if out of range
    is_private(s)     -- RFC 1918 private-range check; ValueError if invalid
"""

__all__ = ["is_valid_ipv4", "to_int", "from_int", "is_private"]

_DECIMAL_DIGITS = frozenset("0123456789")


def _parse_ipv4(s):
    """Parse a strict IPv4 string into a 4-tuple of ints, or raise ValueError.

    Strict rules: exactly four dot-separated octets, each a decimal number
    0-255 with no leading zeros (the single character "0" is allowed), and no
    spaces or any other non-digit characters anywhere.
    """
    if not isinstance(s, str):
        raise ValueError("IPv4 address must be a string, got %r" % (s,))
    parts = s.split(".")
    if len(parts) != 4:
        raise ValueError(
            "IPv4 address must have exactly four octets: %r" % (s,)
        )
    octets = []
    for part in parts:
        if part == "":
            raise ValueError("empty octet in IPv4 address: %r" % (s,))
        if not all(ch in _DECIMAL_DIGITS for ch in part):
            raise ValueError("octet must contain only digits: %r" % (s,))
        if len(part) > 1 and part[0] == "0":
            raise ValueError("octet has a leading zero: %r" % (s,))
        value = int(part)
        if value > 255:
            raise ValueError("octet out of range 0-255: %r" % (s,))
        octets.append(value)
    return tuple(octets)


def is_valid_ipv4(s):
    """Return True iff *s* is a strict IPv4 address; never raises."""
    try:
        _parse_ipv4(s)
    except ValueError:
        return False
    return True


def to_int(s):
    """Convert a strict IPv4 address string to its 32-bit integer value.

    Raises ValueError for anything that is not a strict IPv4 address.
    """
    a, b, c, d = _parse_ipv4(s)
    return (a << 24) | (b << 16) | (c << 8) | d


def from_int(n):
    """Convert an int in 0..2**32-1 to its dotted-quad IPv4 string.

    Raises ValueError if *n* is not an int in that inclusive range.
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError("n must be an int in 0..2**32-1, got %r" % (n,))
    if n < 0 or n > 0xFFFFFFFF:
        raise ValueError("n must be in 0..2**32-1, got %r" % (n,))
    return "%d.%d.%d.%d" % (
        (n >> 24) & 0xFF,
        (n >> 16) & 0xFF,
        (n >> 8) & 0xFF,
        n & 0xFF,
    )


def is_private(s):
    """Return True iff *s* is a valid RFC 1918 private IPv4 address.

    Private ranges: 10/8, 172.16/12, 192.168/16.
    Raises ValueError if *s* is not a valid IPv4 address.
    """
    first, second = _parse_ipv4(s)[:2]
    if first == 10:
        return True
    if first == 172 and 16 <= second <= 31:
        return True
    if first == 192 and second == 168:
        return True
    return False
