"""Luhn (mod 10) check-digit utilities.

Standard library only; no third-party dependencies.

Public API:
    is_valid(number)   -- validate a card number (str in, bool out, never raises)
    check_digit(prefix)-- compute the single check digit for a numeric prefix
    generate(prefix)   -- prefix + check digit as a pure digit string
"""

__all__ = ["is_valid", "check_digit", "generate"]


def _clean(number):
    """Remove spaces and hyphens from *number* and return the remainder."""
    return number.replace(" ", "").replace("-", "")


def _is_pure_digits(text):
    """True when *text* is a non-empty run of ASCII digits."""
    return bool(text) and text.isascii() and text.isdigit()


def _luhn_sum(digits):
    """Luhn checksum of a pure digit string (right-to-left, double every 2nd)."""
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = ord(ch) - 48
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total


def is_valid(number):
    """Return True when *number* passes the Luhn check.

    *number* is a string that may contain spaces and hyphens; they are
    stripped first. After stripping the remainder must be all digits and
    12-19 characters long, otherwise (including non-string input) False is
    returned -- this function never raises.
    """
    if not isinstance(number, str):
        return False
    digits = _clean(number)
    if not _is_pure_digits(digits):
        return False
    if not 12 <= len(digits) <= 19:
        return False
    return _luhn_sum(digits) % 10 == 0


def check_digit(prefix):
    """Return the one-digit check digit (as a string) for *prefix*.

    *prefix* may contain spaces and hyphens; after stripping it must be a
    non-empty string of digits, otherwise ValueError is raised. Appending
    the returned digit to the stripped prefix yields a Luhn-valid number.
    """
    if not isinstance(prefix, str):
        raise ValueError("prefix must be a string of digits")
    digits = _clean(prefix)
    if not _is_pure_digits(digits):
        raise ValueError(
            "prefix must be non-empty and contain only digits "
            "(after removing spaces and hyphens)"
        )
    # Once the check digit is appended, the rightmost prefix digit sits at
    # doubling position, so double starting from it (i == 0).
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = ord(ch) - 48
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return str((10 - total % 10) % 10)


def generate(prefix):
    """Return the stripped *prefix* followed by its check digit.

    The result is a pure digit string. Invalid prefixes (non-string,
    empty, or containing non-digits after stripping) raise ValueError.
    """
    if not isinstance(prefix, str):
        raise ValueError("prefix must be a string of digits")
    digits = _clean(prefix)
    return digits + check_digit(digits)
