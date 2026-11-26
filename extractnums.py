"""extractnums — text number extraction under a pinned token grammar.

Token grammar (pinned, verbatim from the spec):

    token = \\d+(\\.\\d+)? | \\.\\d+

Scanned left to right with maximal munch: at each start position take the
longest possible integer part plus optional fractional part first.  After a
token ends, a following '.' whose next character is a digit forms a NEW
standalone token in ``.\\d+`` shape (it does NOT merge with the previous
token) — e.g. ``"v2.0.1 build 45"`` -> ``[2.0, 0.1, 45]`` and
``"3.14.15"`` -> ``[3.14, 0.15]``.

No signs (``"-5"`` yields only ``5``), no exponent or thousands separators
(``"1e5"`` -> ``[1, 5]``, ``"1,000"`` -> ``[1, 0]``); a lone '.' with no
digit after it forms no token.

A token containing '.' is returned as float, otherwise as int.
"""

from __future__ import annotations

__all__ = ["extract_numbers"]


def _is_digit(ch: str) -> bool:
    return "0" <= ch <= "9"


def extract_numbers(text: str) -> list:
    """Extract numeric tokens from ``text`` under the pinned grammar.

    Returns a list of int/float values: tokens containing '.' are float,
    all others are int.  Raises TypeError for non-str input.
    """
    if not isinstance(text, str):
        raise TypeError(
            f"extract_numbers() expected str, got {type(text).__name__}"
        )

    results: list = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if _is_digit(ch):
            # \\d+ — maximal munch of the integer part.
            start = i
            while i < n and _is_digit(text[i]):
                i += 1
            # (\\.\\d+)? — optional fractional part, only when a digit
            # follows the '.' (so "5." stays the integer 5).
            if i < n and text[i] == "." and i + 1 < n and _is_digit(text[i + 1]):
                i += 1
                while i < n and _is_digit(text[i]):
                    i += 1
            token = text[start:i]
            results.append(float(token) if "." in token else int(token))
        elif ch == ".":
            # \\.\\d+ — a '.' starting (or following a token) whose next
            # character is a digit is a NEW standalone token.
            if i + 1 < n and _is_digit(text[i + 1]):
                start = i
                i += 1
                while i < n and _is_digit(text[i]):
                    i += 1
                token = text[start:i]
                results.append(float(token) if "." in token else int(token))
            else:
                # Lone '.' — not a token; move past it.
                i += 1
        else:
            i += 1
    return results


if __name__ == "__main__":  # pragma: no cover
    import sys

    print(extract_numbers(" ".join(sys.argv[1:])) if len(sys.argv) > 1 else extract_numbers(""))
