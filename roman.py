"""Roman numeral conversion helpers (standard library only)."""

_SYMBOLS = (
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
)

_VALUES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
_SUBTRACTIVE = {"IV", "IX", "XL", "XC", "CD", "CM"}
# Consecutive-run limits: I/X/C/M repeat at most 3 times; V/L/D appear at most once.
_MAX_REPEAT = {"I": 3, "X": 3, "C": 3, "M": 3, "V": 1, "L": 1, "D": 1}


def to_roman(n):
    """Convert an integer in 1-3999 to its Roman numeral string.

    Raises ValueError if n is not an int in 1-3999 (bools rejected too).
    """
    if isinstance(n, bool) or not isinstance(n, int) or not 1 <= n <= 3999:
        raise ValueError("n must be an integer in 1-3999, got %r" % (n,))
    remaining = n
    parts = []
    for value, symbol in _SYMBOLS:
        while remaining >= value:
            parts.append(symbol)
            remaining -= value
    return "".join(parts)


def _check_runs(s):
    """Reject illegal consecutive repetition (IIII, VV, MMMM, ...)."""
    i = 0
    length = len(s)
    while i < length:
        symbol = s[i]
        run = 1
        while i + run < length and s[i + run] == symbol:
            run += 1
        limit = _MAX_REPEAT[symbol]
        if run > limit:
            raise ValueError(
                "illegal repetition of %r (%d times) in %r" % (symbol, run, s)
            )
        i += run


def from_roman(s):
    """Convert a canonical Roman numeral string back to an integer.

    Raises ValueError for empty strings, illegal characters, illegal
    repetition (e.g. 'IIII', 'VV', 'MMMM'), improper subtraction
    (e.g. 'IC', 'VX'), and any other non-canonical form.
    """
    if not isinstance(s, str) or s == "":
        raise ValueError("empty or non-string Roman numeral: %r" % (s,))
    for ch in s:
        if ch not in _VALUES:
            raise ValueError("illegal character %r in %r" % (ch, s))

    _check_runs(s)

    # Left-to-right parse: a smaller numeral before a larger one must form
    # one of the six canonical subtractive pairs (each exactly one place
    # apart), so forms like 'IC' or 'VX' are rejected here.
    total = 0
    i = 0
    length = len(s)
    while i < length:
        if i + 1 < length and _VALUES[s[i]] < _VALUES[s[i + 1]]:
            pair = s[i:i + 2]
            if pair not in _SUBTRACTIVE:
                raise ValueError("improper subtraction %r in %r" % (pair, s))
            total += _VALUES[pair[1]] - _VALUES[pair[0]]
            i += 2
        else:
            total += _VALUES[s[i]]
            i += 1

    # Final safety net: only the canonical encoding of `total` is accepted
    # (catches any remaining additive oddities and out-of-range values).
    if not 1 <= total <= 3999 or to_roman(total) != s:
        raise ValueError("non-canonical Roman numeral %r" % (s,))
    return total
