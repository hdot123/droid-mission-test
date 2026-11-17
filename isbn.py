"""ISBN-10 validation (standard library only)."""


def is_valid_isbn10(s):
    """Return whether s is a valid ISBN-10.

    Ignores hyphens and spaces. The cleaned string must be exactly 10
    characters: 9 digits plus a check character (a digit or 'X'). The
    weighted sum 10*d1 + 9*d2 + ... + 1*d10 must be divisible by 11.
    'X' is allowed only in the last position and represents 10.
    """
    if not isinstance(s, str):
        return False
    cleaned = s.replace('-', '').replace(' ', '')
    if len(cleaned) != 10:
        return False
    if not cleaned[:9].isdigit():
        return False
    last = cleaned[9]
    if last == 'X':
        check = 10
    elif last.isdigit():
        check = int(last)
    else:
        return False
    total = check
    for i, ch in enumerate(cleaned[:9]):
        total += (10 - i) * int(ch)
    return total % 11 == 0
