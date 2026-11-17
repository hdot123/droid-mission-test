"""Convert integer strings between bases 2-36."""

_DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"


def _digit_value(ch):
    if ch.isdigit() and ch in _DIGITS:
        return _DIGITS.index(ch)
    lowered = ch.lower()
    if lowered in _DIGITS:
        return _DIGITS.index(lowered)
    return -1


def _validate_base(base, name):
    if not isinstance(base, int) or isinstance(base, bool):
        raise ValueError("%s must be an integer in 2-36" % name)
    if not 2 <= base <= 36:
        raise ValueError("%s must be in 2-36, got %d" % (name, base))


def _to_int(s, from_base):
    if not isinstance(s, str) or s == "":
        raise ValueError("s must be a non-empty string")
    _validate_base(from_base, "from_base")
    body = s[1:] if s[0] in "+-" else s
    if body == "":
        raise ValueError("s must contain at least one digit")
    value = 0
    for ch in body:
        d = _digit_value(ch)
        if d < 0 or d >= from_base:
            raise ValueError("invalid character %r for base %d" % (ch, from_base))
        value = value * from_base + d
    return -value if s[0] == "-" else value


def _from_int(value, to_base):
    if value == 0:
        return "0"
    negative = value < 0
    value = abs(value)
    out = []
    while value:
        value, rem = divmod(value, to_base)
        out.append(_DIGITS[rem])
    result = "".join(reversed(out))
    return "-" + result if negative else result


def convert(s, from_base, to_base):
    """Convert the integer string s from from_base to to_base.

    Bases must be integers in 2-36. s must be a non-empty string, optionally
    signed, using digits 0-9 and letters a-z/A-Z whose value is less than
    from_base. Returns the target-base string in lowercase with no leading
    zeros, "0" for zero, and a leading minus sign for negatives.

    Raises ValueError for an out-of-range base, an empty string, or a
    character whose value exceeds the source base.
    """
    _validate_base(from_base, "from_base")
    _validate_base(to_base, "to_base")
    value = _to_int(s, from_base)
    return _from_int(value, to_base)
