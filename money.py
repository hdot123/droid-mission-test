"""Integer-cent money helpers (parse / format / split)."""

import re

_AMOUNT_RE = re.compile(r"^-?\d+(?:\.\d{1,2})?$")


def parse(text: str) -> int:
    """Convert an amount string to integer cents.

    Accepted form: optional leading '-', one or more integer digits,
    optionally a decimal point followed by one or two fractional digits
    (a single fractional digit counts as tenths).  Commas, whitespace and
    '+' are not allowed.  Malformed input raises ValueError.
    """
    if not isinstance(text, str) or not _AMOUNT_RE.match(text):
        raise ValueError(f"invalid amount: {text!r}")

    negative = text.startswith("-")
    body = text[1:] if negative else text

    if "." in body:
        int_part, frac_part = body.split(".")
        frac_part = frac_part.ljust(2, "0")
    else:
        int_part, frac_part = body, "00"

    cents = int(int_part) * 100 + int(frac_part)
    return -cents if negative else cents


def format(cents: int) -> str:
    """Format integer cents as an amount string with two decimal places."""
    if not isinstance(cents, int):
        raise TypeError("cents must be an int")
    sign = "-" if cents < 0 else ""
    magnitude = abs(cents)
    return f"{sign}{magnitude // 100}.{magnitude % 100:02d}"


def split(cents: int, n: int) -> list[int]:
    """Split cents into n parts as evenly as possible.

    Remainder cents are added one cent each to the first parts, so the sum
    of the result equals cents.  Negative amounts are split by absolute
    value and then the negative sign is applied uniformly.  n < 1 raises
    ValueError.
    """
    if not isinstance(n, int) or n < 1:
        raise ValueError(f"n must be >= 1, got {n!r}")

    negative = cents < 0
    magnitude = abs(cents)
    base, remainder = divmod(magnitude, n)

    parts = [base + 1 if i < remainder else base for i in range(n)]
    if negative:
        parts = [-part for part in parts]
    return parts
