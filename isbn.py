"""ISBN-10 and ISBN-13 validation, plus ISBN-10 to ISBN-13 conversion.

Only the Python standard library is used; this module does not import
other project modules.
"""

__all__ = ["is_valid", "to_isbn13"]


def _require_str(isbn):
    if isbn is None:
        raise TypeError("isbn must be a string, not None")
    if not isinstance(isbn, str):
        raise TypeError("isbn must be a string, not %s" % type(isbn).__name__)
    return isbn.replace("-", "").replace(" ", "")


def _digits_or_none(text, size, allow_x_last):
    """Parse *text* into digit values, or None if it is malformed."""
    if len(text) != size:
        return None
    values = []
    for i, ch in enumerate(text):
        if "0" <= ch <= "9":
            values.append(ord(ch) - 48)
        elif allow_x_last and i == size - 1 and ch == "X":
            values.append(10)
        else:
            return None
    return values


def _isbn10_checksum_ok(values):
    # Positions 1..9 (0-based 0..8) weigh 10..2; the check value weighs 1.
    total = sum(values[i] * (10 - i) for i in range(9)) + values[9]
    return total % 11 == 0


def _isbn13_checksum_ok(values):
    total = sum(d * (1 if i % 2 == 0 else 3) for i, d in enumerate(values))
    return total % 10 == 0


def is_valid(isbn):
    """Return True if *isbn* is a valid ISBN-10 or ISBN-13.

    Hyphens and spaces are ignored anywhere in the input.  For ISBN-10 the
    check character may be ``X`` (value 10), but only as the final
    character.  Any other illegal character, wrong length, or wrong
    checksum returns False (no exception).

    Raises TypeError when *isbn* is None or not a string.
    """
    text = _require_str(isbn)
    if len(text) == 10:
        values = _digits_or_none(text, 10, allow_x_last=True)
        return values is not None and _isbn10_checksum_ok(values)
    if len(text) == 13:
        values = _digits_or_none(text, 13, allow_x_last=False)
        return values is not None and _isbn13_checksum_ok(values)
    return False


def to_isbn13(isbn):
    """Convert a valid ISBN-10 to its ISBN-13 equivalent.

    Returns a 13-digit string with the ``978`` prefix and a correct check
    digit.  Raises TypeError when *isbn* is None or not a string, and
    ValueError when *isbn* is not a valid ISBN-10.
    """
    text = _require_str(isbn)
    values = _digits_or_none(text, 10, allow_x_last=True)
    if values is None or not _isbn10_checksum_ok(values):
        raise ValueError("not a valid ISBN-10: %r" % (isbn,))
    twelve = [9, 7, 8] + values[:9]
    total = sum(d * (1 if i % 2 == 0 else 3) for i, d in enumerate(twelve))
    check = (10 - total % 10) % 10
    return "".join(str(d) for d in twelve) + str(check)
