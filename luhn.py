"""Luhn (mod 10) checksum helpers.

Standard library only; no imports from sibling components.
"""


def is_valid(number: str) -> bool:
    """Return True if ``number`` is a pure-digit string passing the Luhn check.

    Empty strings and strings containing non-digit characters return False
    instead of raising.
    """
    if not isinstance(number, str) or number == "" or not number.isdigit():
        return False
    total = 0
    # Double every second digit starting from the right (the rightmost digit
    # keeps weight 1).
    for i, ch in enumerate(reversed(number)):
        digit = ord(ch) - 48
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0


def check_digit(prefix: str) -> int:
    """Return the digit (0-9) that makes ``prefix`` + that digit pass Luhn.

    Raises ValueError for an empty string or a string containing non-digit
    characters.
    """
    if not isinstance(prefix, str) or prefix == "" or not prefix.isdigit():
        raise ValueError("prefix must be a non-empty pure-digit string")
    total = 0
    # The appended check digit sits at the rightmost position (weight 1), so
    # the prefix's last digit gets weight 2, the one before it weight 1, etc.
    for i, ch in enumerate(reversed(prefix)):
        digit = ord(ch) - 48
        if i % 2 == 0:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return (10 - total % 10) % 10
