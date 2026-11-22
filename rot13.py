"""ROT13 transformation for English letters."""

import string

# Build translation table: shift each ASCII letter by 13 within its case.
_UPPER = string.ascii_uppercase
_LOWER = string.ascii_lowercase
_TABLE = str.maketrans(
    _UPPER + _LOWER,
    _UPPER[13:] + _UPPER[:13] + _LOWER[13:] + _LOWER[:13],
)


def apply(text):
    """Return text with each English letter ROT13-transformed (case preserved).

    All non-letter characters are passed through unchanged. Applying this
    function twice restores the original text.
    """
    return text.translate(_TABLE)
