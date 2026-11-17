"""Luhn check for digit strings."""


def is_valid(number):
    """Return True if `number` passes the Luhn check.

    Spaces and hyphens are ignored. After removing them the remaining
    content must be pure digits with length >= 2. The Luhn algorithm is
    then applied: from the right, double every second digit, subtract 9 if
    the doubled value exceeds 9, and the total sum must be divisible by 10.

    Raises:
        ValueError: if the content contains non-digit characters other than
            spaces/hyphens, or if the digit length is less than 2.
    """
    if not isinstance(number, str):
        raise ValueError("number must be a string")

    digits_only = number.replace(" ", "").replace("-", "")

    if not digits_only.isdigit():
        raise ValueError("number must contain only digits, spaces, or hyphens")
    if len(digits_only) < 2:
        raise ValueError("number must contain at least 2 digits")

    total = 0
    # Double every second digit starting from the rightmost-1 position.
    for i, ch in enumerate(reversed(digits_only)):
        digit = ord(ch) - 48
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit

    return total % 10 == 0
