"""Luhn (mod 10) checksum helpers for card-like numeric strings.

Standard library only; no third-party dependencies.
"""


def _strip(number):
    """Remove spaces and hyphens from a string."""
    return number.replace(" ", "").replace("-", "")


_ASCII_DIGITS = frozenset("0123456789")


def _is_all_digits(text):
    """True iff every character is an ASCII digit 0-9."""
    return bool(text) and all(ch in _ASCII_DIGITS for ch in text)


def _luhn_sum_digits(digits):
    """Sum digits (as ints) applying the Luhn doubling rule from the right.

    ``digits`` is a sequence of int digits of the number *without* the check
    digit; its rightmost digit is doubled (it will sit just left of the check
    digit in the full number).
    """
    total = 0
    for index, digit in enumerate(reversed(digits)):
        value = digit * 2 if index % 2 == 0 else digit
        if value > 9:
            value -= 9
        total += value
    return total


def is_valid(number):
    """Return True if ``number`` passes the Luhn check, else False.

    ``number`` may contain spaces and hyphens, which are stripped first.
    After stripping, the string must be all digits with length 12-19
    inclusive; otherwise False is returned. Never raises.
    """
    if not isinstance(number, str):
        return False
    stripped = _strip(number)
    if not (12 <= len(stripped) <= 19):
        return False
    if not _is_all_digits(stripped):
        return False
    digits = [int(ch) for ch in stripped]
    return (_luhn_sum_digits(digits[:-1]) + digits[-1]) % 10 == 0


def check_digit(prefix):
    """Return the single-character check digit for ``prefix``.

    ``prefix`` may contain spaces and hyphens, which are stripped first.
    After stripping, the result must be all digits and non-empty, otherwise
    ValueError is raised.
    """
    if not isinstance(prefix, str):
        raise ValueError("prefix must be a string")
    stripped = _strip(prefix)
    if not _is_all_digits(stripped):
        raise ValueError("prefix must contain only digits after stripping")
    digits = [int(ch) for ch in stripped]
    return str((10 - (_luhn_sum_digits(digits) % 10)) % 10)


def generate(prefix):
    """Return the stripped ``prefix`` concatenated with its check digit."""
    stripped = _strip(prefix)
    return stripped + check_digit(stripped)
