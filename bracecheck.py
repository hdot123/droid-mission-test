"""Bracket balancing check, independent of the codecbox directory.

This module intentionally has no dependency on ``codecbox`` or the codec
plugins: it only inspects parentheses, square brackets, and braces.
"""

_OPEN_TO_CLOSE = {"(": ")", "[": "]", "{": "}"}
_CLOSE_TO_OPEN = {close: open_ for open_, close in _OPEN_TO_CLOSE.items()}


def is_balanced(text):
    """Return True if (), [], and {} in *text* are correctly paired/nested.

    Every character that is not one of the six bracket characters is ignored.
    """
    stack = []
    for ch in text:
        if ch in _OPEN_TO_CLOSE:
            stack.append(_OPEN_TO_CLOSE[ch])
        elif ch in _CLOSE_TO_OPEN:
            if not stack or stack.pop() != ch:
                return False
    return not stack
