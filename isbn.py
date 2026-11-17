"""ISBN-10 validation helpers (standard library only)."""


def is_valid_isbn10(s):
    """Return True if ``s`` is a valid ISBN-10 code.

    Hyphens and spaces are ignored.  After stripping, the code must be
    exactly 10 characters: 9 digits followed by a check digit that is
    either a digit or ``X`` (which may only appear as the last character
    and represents 10).  The weighted sum
    ``10*d1 + 9*d2 + ... + 1*d10`` must be divisible by 11.
    """
    if not isinstance(s, str):
        raise ValueError("ISBN-10 must be a string")
    cleaned = s.replace("-", "").replace(" ", "")
    if len(cleaned) != 10:
        return False
    for i, ch in enumerate(cleaned[:-1]):
        if not ch.isdigit():
            return False
        if len(ch) != 1:  # guard against non-ASCII digit lookalikes
            return False
    last = cleaned[-1]
    if last == "X":
        check = 10
    elif last.isdigit() and len(last) == 1:
        check = int(last)
    else:
        return False
    total = 0
    for i, ch in enumerate(cleaned[:-1]):
        total += (10 - i) * int(ch)
    total += 1 * check
    return total % 11 == 0
