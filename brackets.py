"""Bracket balance checking with quote-awareness (standard library only)."""

_OPEN = {"(": ")", "[": "]", "{": "}"}
_CLOSERS = {v: k for k, v in _OPEN.items()}


def is_balanced(text):
    """Return True if (), [] and {} in ``text`` are properly paired/nested.

    Rules:
    - Content inside single or double quotes is ignored entirely (brackets
      inside quotes never count).
    - A quote is closed only by the same kind of quote; if a quote is left
      unclosed, everything after it is treated as being inside the quote.
    - Non-bracket characters outside quotes are ignored.
    - The empty string is balanced.
    """
    stack = []
    quote = None
    for ch in text:
        if quote is not None:
            if ch == quote:
                quote = None
            continue
        if ch in ("'", '"'):
            quote = ch
        elif ch in _OPEN:
            stack.append(ch)
        elif ch in _CLOSERS:
            if not stack or stack[-1] != _CLOSERS[ch]:
                return False
            stack.pop()
    return not stack
