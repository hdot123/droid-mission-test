"""Semantic version parsing and comparison (MAJOR.MINOR.PATCH).

Only the Python standard library is used. This module does not import
any other project modules.
"""

import re

__all__ = ["parse", "compare", "is_valid"]

_PATTERN = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\Z")


def parse(s):
    """Parse a "MAJOR.MINOR.PATCH" version string into a tuple of three ints.

    Each segment must be a non-negative integer with no extra characters
    and no leading zeros (e.g. "01.2.3" is invalid).

    Raises:
        ValueError: if s is not a valid version string.
        TypeError: if s is not a string.
    """
    if not isinstance(s, str):
        raise TypeError("version must be a string, got %r" % (type(s).__name__,))
    match = _PATTERN.match(s)
    if match is None:
        raise ValueError("invalid version string: %r" % (s,))
    return (int(match.group(1)), int(match.group(2)), int(match.group(3)))


def compare(a, b):
    """Compare two version strings segment-wise numerically.

    Returns -1 if a < b, 0 if a == b, and 1 if a > b.

    Raises:
        ValueError: if either argument is not a valid version string.
    """
    parsed_a = parse(a)
    parsed_b = parse(b)
    if parsed_a < parsed_b:
        return -1
    if parsed_a > parsed_b:
        return 1
    return 0


def is_valid(s):
    """Return True if s is a valid version string, False otherwise.

    Never raises: invalid types and invalid formats both yield False.
    """
    try:
        parse(s)
    except (ValueError, TypeError):
        return False
    return True
