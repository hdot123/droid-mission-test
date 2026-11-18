"""ISBN-13 check digit utilities (round 40 · unit D)."""

_DIGITS = frozenset("0123456789")


def check_digit(first12: str) -> int:
    """Return the ISBN-13 check digit for the first 12 digits.

    The argument must be exactly 12 numeric digit characters, otherwise
    ValueError is raised. Weights alternate 1, 3 from the left; the check
    digit makes the weighted sum (including the check digit) divisible by 10.
    """
    if not isinstance(first12, str) or len(first12) != 12 or not all(
        c in _DIGITS for c in first12
    ):
        raise ValueError("first12 must be exactly 12 digit characters")
    total = 0
    for i, ch in enumerate(first12):
        weight = 1 if i % 2 == 0 else 3
        total += (ord(ch) - 48) * weight
    return (10 - total % 10) % 10


def is_valid(isbn: str) -> bool:
    """Return whether the ISBN-13 is valid.

    Hyphens are removed first; afterwards the string must be exactly 13
    digits, otherwise ValueError is raised. Returns whether the 13th digit
    equals the check digit computed from the first 12.
    """
    if not isinstance(isbn, str):
        raise ValueError("isbn must be a string of 13 digits (hyphens allowed)")
    digits = isbn.replace("-", "")
    if len(digits) != 13 or not all(c in _DIGITS for c in digits):
        raise ValueError("isbn must be exactly 13 digits after removing hyphens")
    return int(digits[12]) == check_digit(digits[:12])
