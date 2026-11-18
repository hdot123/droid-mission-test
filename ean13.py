"""EAN-13 check digit utilities (standard library only)."""


def check_digit(first12):
    """Return the EAN-13 check digit (int) for a 12-digit numeric string.

    Odd positions (1-based, from the left) weigh 1, even positions weigh 3.
    Weighted sum's last digit is subtracted from 10; a result of 10 becomes 0.

    Raises:
        ValueError: if ``first12`` is not a 12-character pure-digit string.
    """
    if not isinstance(first12, str) or len(first12) != 12 or not first12.isdigit():
        raise ValueError("first12 must be a 12-digit numeric string")
    total = 0
    for i, ch in enumerate(first12):
        weight = 1 if (i % 2 == 0) else 3
        total += int(ch) * weight
    result = (10 - (total % 10)) % 10
    return result


def is_valid(code):
    """Return True if ``code`` is a 13-digit string with a correct check digit.

    Malformed input (not 13 pure digits) returns False without raising.
    """
    if not isinstance(code, str) or len(code) != 13 or not code.isdigit():
        return False
    return check_digit(code[:12]) == int(code[12])
