"""ISBN-10 check digit utilities (standard library only)."""


def check_digit(first9):
    """Return the ISBN-10 check character for a 9-digit string.

    Position i (1-based, leftmost = 1) has weight i; the weighted sum of
    the first 9 digits modulo 11 is the check value, with 10 mapped to 'X'.

    Raises ValueError if the input is not exactly 9 ASCII digit characters.
    """
    if not isinstance(first9, str) or len(first9) != 9 or not first9.isascii() or not first9.isdigit():
        raise ValueError("first9 must be exactly 9 ASCII digit characters")
    total = sum(int(d) * (i + 1) for i, d in enumerate(first9))
    value = total % 11
    return "X" if value == 10 else str(value)


def is_valid(code):
    """Return True if code is a valid 10-character ISBN-10, else False.

    The first 9 characters must be digits and the last must be a digit or
    'X'; malformed input returns False rather than raising.
    """
    if not isinstance(code, str) or len(code) != 10:
        return False
    first9, last = code[:9], code[9]
    last_is_digit = last.isascii() and last.isdigit()
    if not first9.isascii() or not first9.isdigit() or not (last_is_digit or last == "X"):
        return False
    return check_digit(first9) == last
