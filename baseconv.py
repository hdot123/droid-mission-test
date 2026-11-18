"""Arbitrary base (2-36) integer conversion helpers.

Digit alphabet is exactly ``0123456789abcdefghijklmnopqrstuvwxyz``; only
lowercase letters are accepted when parsing.
"""

DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"


def _check_base(base: int) -> None:
    if not 2 <= base <= 36:
        raise ValueError(f"base must be in 2-36, got {base!r}")


def to_base(n: int, base: int) -> str:
    """Convert a non-negative integer to a base-``base`` string."""
    _check_base(base)
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n!r}")
    if n == 0:
        return "0"
    digits = []
    while n > 0:
        n, rem = divmod(n, base)
        digits.append(DIGITS[rem])
    return "".join(reversed(digits))


def from_base(s: str, base: int) -> int:
    """Parse a base-``base`` string (lowercase alphabet only) to an int."""
    _check_base(base)
    if not s:
        raise ValueError("empty string is not a valid number")
    value = 0
    for ch in s:
        # Uppercase letters (and anything else outside the alphabet) raise.
        if ch not in DIGITS:
            raise ValueError(f"invalid digit {ch!r} for base {base}")
        d = DIGITS.index(ch)
        if d >= base:
            raise ValueError(f"digit {ch!r} not allowed in base {base}")
        value = value * base + d
    return value
