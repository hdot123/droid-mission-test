"""Crockford Base32 encoding and decoding.

Alphabet: 0123456789ABCDEFGHJKMNPQRSTVWXYZ (no I, L, O, U).
"""

ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


def encode(n: int) -> str:
    """Encode a non-negative integer as a Crockford Base32 string.

    Raises ValueError for negative input.
    """
    if n < 0:
        raise ValueError("cannot encode a negative integer")
    if n == 0:
        return "0"
    digits = []
    while n > 0:
        digits.append(ALPHABET[n & 31])
        n >>= 5
    return "".join(reversed(digits))


def decode(s: str) -> int:
    """Decode a Crockford Base32 string to an integer.

    The input is uppercased first; ``I`` and ``L`` are treated as ``1``
    and ``O`` as ``0``. Any other character outside the alphabet
    (including ``U``) raises ValueError, as does an empty string.
    """
    if not s:
        raise ValueError("empty string")
    value = 0
    for ch in s.upper():
        if ch in ("I", "L"):
            ch = "1"
        elif ch == "O":
            ch = "0"
        index = ALPHABET.find(ch)
        if index < 0:
            raise ValueError("invalid character: {!r}".format(ch))
        value = value * 32 + index
    return value
