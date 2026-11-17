"""Roman numeral conversion for integers 1-3999 (standard subtractive notation)."""


def to_roman(n):
    """Convert an integer 1-3999 to a Roman numeral string.

    Raises ValueError for non-integers and out-of-range values.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise ValueError("n must be an integer")
    if not 1 <= n <= 3999:
        raise ValueError("n must be in range 1-3999")

    values = (
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
    result = []
    remaining = n
    for value, symbol in values:
        while remaining >= value:
            result.append(symbol)
            remaining -= value
    return "".join(result)


def from_roman(s):
    """Convert a valid Roman numeral string to an integer.

    Raises ValueError for invalid or non-canonical Roman numeral strings.
    """
    if not isinstance(s, str) or not s:
        raise ValueError("s must be a non-empty string")

    roman_values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    if any(ch not in roman_values for ch in s):
        raise ValueError("invalid Roman numeral characters")

    total = 0
    for i, ch in enumerate(s):
        value = roman_values[ch]
        if i + 1 < len(s) and value < roman_values[s[i + 1]]:
            total -= value
        else:
            total += value

    # Reject non-canonical forms such as "IIII", "VV", "IC", "XM", etc.
    if not 1 <= total <= 3999 or to_roman(total) != s:
        raise ValueError("invalid Roman numeral")
    return total
