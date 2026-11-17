"""Run-length encoding and decoding for strings."""

import re

_PATTERN = re.compile(r"([a-zA-Z]|.)(\d*)")


def encode(s):
    """Encode a string with run-length encoding.

    Consecutive repeated characters become the character followed by the
    run count; the digit is omitted when the count is 1.

    >>> encode("aaabbbbc")
    'a3b4c'
    >>> encode("abc")
    'abc'
    """
    if not isinstance(s, str):
        raise ValueError("s must be a string")
    out = []
    i = 0
    n = len(s)
    while i < n:
        ch = s[i]
        j = i + 1
        while j < n and s[j] == ch:
            j += 1
        count = j - i
        if count == 1:
            out.append(ch)
        else:
            out.append(ch + str(count))
        i = j
    return "".join(out)


def decode(s):
    """Decode a run-length encoded string.

    Inverse of encode. Raises ValueError on invalid format, including a
    leading digit at the start of the string and a count of 0.

    >>> decode("a3b4c")
    'aaabbbbc'
    """
    if not isinstance(s, str):
        raise ValueError("s must be a string")
    if s == "":
        return ""
    if s[0].isdigit():
        raise ValueError("run-length encoded string must not start with a digit")
    out = []
    pos = 0
    while pos < len(s):
        m = _PATTERN.match(s, pos)
        if m is None:
            raise ValueError("invalid run-length encoded string")
        char, digits = m.group(1), m.group(2)
        if digits == "":
            count = 1
        else:
            if char.isdigit():
                raise ValueError("invalid run-length encoded string")
            count = int(digits)
            if count == 0:
                raise ValueError("run count must not be 0")
        out.append(char * count)
        pos = m.end()
    return "".join(out)
