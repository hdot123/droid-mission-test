"""ROT13 and general Caesar shift utilities (standard library only)."""


def rot_n(text, n):
    """Shift English letters in ``text`` by ``n`` positions.

    Case is preserved and non-letters are returned unchanged. ``n`` may be
    any integer (negative or larger than 26); the shift wraps within a-z
    and A-Z independently.
    """
    result = []
    for ch in text:
        if "a" <= ch <= "z":
            result.append(chr((ord(ch) - ord("a") + n) % 26 + ord("a")))
        elif "A" <= ch <= "Z":
            result.append(chr((ord(ch) - ord("A") + n) % 26 + ord("A")))
        else:
            result.append(ch)
    return "".join(result)


def rot13(text):
    """Apply the ROT13 transform to ``text`` (equivalent to ``rot_n(text, 13)``)."""
    return rot_n(text, 13)
