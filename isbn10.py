"""ISBN-10 check digit validation (standard library only)."""


def check_digit(first9: str) -> str:
    """Return the ISBN-10 check character for the first 9 digits.

    Weights run from 10 on the left down to 2 on the right; the check
    character is (11 - sum % 11) % 11, with 10 represented as 'X'.

    Raises ValueError if the input is not exactly 9 digits.
    """
    if not isinstance(first9, str) or len(first9) != 9:
        raise ValueError("first9 must be exactly 9 characters")
    if not first9.isdigit() or not first9.isascii():
        raise ValueError("first9 must contain only digits")
    total = 0
    for i, ch in enumerate(first9):
        total += int(ch) * (10 - i)
    remainder = total % 11
    value = (11 - remainder) % 11
    return "X" if value == 10 else str(value)


def is_valid(isbn: str) -> bool:
    """Return True if isbn is a valid ISBN-10, else False.

    Exactly 10 characters; the last may be 'X' (uppercase only, and only
    in the final position). Never raises.
    """
    try:
        if not isinstance(isbn, str) or len(isbn) != 10:
            return False
        first9, last = isbn[:9], isbn[9]
        if not first9.isdigit() or not first9.isascii():
            return False
        if last not in "0123456789X":
            return False
        return check_digit(first9) == last
    except Exception:
        return False
