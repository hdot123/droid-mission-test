"""snake_case <-> camelCase conversion helpers."""

import re


def snake_to_camel(s: str) -> str:
    """Convert a lowercase snake_case string to camelCase.

    The input must be lowercase snake_case: lowercase letters and digits
    separated by underscores. Empty strings, leading/trailing/consecutive
    underscores, and uppercase letters are invalid and raise ValueError.

    The first segment is kept as-is; each subsequent segment's first letter
    is uppercased; the segments are then concatenated.
    """
    if not isinstance(s, str):
        raise ValueError("input must be a string")
    if not s or not re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", s):
        raise ValueError("input must be lowercase snake_case: " + repr(s))
    segments = s.split("_")
    return segments[0] + "".join(seg[:1].upper() + seg[1:] for seg in segments[1:])


def camel_to_snake(s: str) -> str:
    """Convert a camelCase string to snake_case.

    The input must be an alphanumeric string containing no underscores
    (the first letter may be upper or lower case). Empty strings and
    strings containing underscores (or other non-alphanumeric characters)
    are invalid and raise ValueError.

    An underscore is inserted before every uppercase letter except the
    first, then everything is lowercased.
    """
    if not isinstance(s, str):
        raise ValueError("input must be a string")
    if not s or not re.fullmatch(r"[A-Za-z0-9]+", s):
        raise ValueError("input must be alphanumeric without underscores: " + repr(s))
    out = []
    for i, ch in enumerate(s):
        if ch.isupper() and i > 0:
            out.append("_")
        out.append(ch.lower())
    return "".join(out)
