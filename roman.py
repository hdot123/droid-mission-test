"""Roman numeral conversion for integers 1-3999 (standard subtractive notation)."""

_ROMAN_VALS = (
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
)

_ROMAN_TO_INT = {sym: val for val, sym in _ROMAN_VALS}


def to_roman(n):
    """Convert integer n (1-3999) to a Roman numeral string.

    Raises ValueError if n is not an integer or is out of range.
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError("n must be an integer")
    if n < 1 or n > 3999:
        raise ValueError("n must be in range 1-3999")
    result = []
    for value, sym in _ROMAN_VALS:
        while n >= value:
            result.append(sym)
            n -= value
    return "".join(result)


def from_roman(s):
    """Convert a valid Roman numeral string back to an integer.

    Raises ValueError if s is not a valid Roman numeral string.
    """
    if not isinstance(s, str) or not s:
        raise ValueError("invalid Roman numeral")
    # Reject characters outside the Roman alphabet.
    if any(ch not in _ROMAN_TO_INT for ch in s):
        raise ValueError("invalid Roman numeral")
    # Parse subtractive pairs greedily, then require the canonical form
    # (roundtrip through to_roman) so non-canonical spellings like "IIII"
    # or "IC" are rejected.
    total = 0
    i = 0
    while i < len(s):
        cur = _ROMAN_TO_INT[s[i]]
        if i + 1 < len(s) and _ROMAN_TO_INT[s[i + 1]] > cur:
            total += _ROMAN_TO_INT[s[i + 1]] - cur
            i += 2
        else:
            total += cur
            i += 1
    if total < 1 or total > 3999 or to_roman(total) != s:
        raise ValueError("invalid Roman numeral")
    return total
