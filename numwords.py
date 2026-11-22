"""Integer to English words (American style, no "and").

Public API:
    number_to_words(n: int) -> str
"""

__all__ = ["number_to_words"]

_ONES = (
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
)

_TENS = (
    "",
    "",
    "twenty",
    "thirty",
    "forty",
    "fifty",
    "sixty",
    "seventy",
    "eighty",
    "ninety",
)

_MAX = 999_999_999


def _under_1000(n: int) -> str:
    """Spell 0 <= n <= 999 as American English words (no "and")."""
    parts = []
    if n >= 100:
        parts.append(_ONES[n // 100] + " hundred")
        n %= 100
    if n >= 20:
        tens = _TENS[n // 10]
        ones = n % 10
        parts.append(tens + ("-" + _ONES[ones] if ones else ""))
    elif n > 0 or not parts:
        parts.append(_ONES[n])
    return " ".join(parts)


def number_to_words(n: int) -> str:
    """Convert an integer in [0, 999,999,999] to American English words.

    Rules: all lowercase, no "and", grouped by thousand/million,
    hundreds as "X hundred", tens-ones joined by a hyphen,
    groups separated by single spaces, no leading/trailing spaces.

    Raises:
        TypeError: if n is not an int (bool rejected).
        ValueError: if n is out of the pinned range.
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an int, got {!r}".format(n))
    if n < 0 or n > _MAX:
        raise ValueError("n must be in [0, 999999999], got {!r}".format(n))
    if n == 0:
        return "zero"

    millions = n // 1_000_000
    thousands = (n % 1_000_000) // 1000
    rest = n % 1000

    groups = []
    if millions:
        groups.append(_under_1000(millions) + " million")
    if thousands:
        groups.append(_under_1000(thousands) + " thousand")
    if rest:
        groups.append(_under_1000(rest))
    return " ".join(groups)
