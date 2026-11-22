"""IBAN-style mod-97 computation (ISO 13616 style remainder).

Standard library only; no imports from sibling components.
"""

__all__ = ["is_valid_iban_numeric", "remainder"]

# Chunk size for the rolling remainder. 10**9 stays well inside ordinary
# machine-word arithmetic, so each step only ever touches small ints, while
# arbitrarily long inputs are consumed without a single whole-string int().
_CHUNK = 9


def remainder(digits: str) -> int:
    """Return ``int(digits) % 97`` computed in fixed-size chunks.

    ``digits`` must be a non-empty string of ASCII digits ('0'-'9').
    Anything else (empty string, non-digits, non-str) raises ValueError;
    the value is never materialised as one giant int, so length is
    bounded only by available memory.
    """
    if not isinstance(digits, str) or not digits:
        raise ValueError("digits must be a non-empty string of ASCII digits")
    if any(ch < "0" or ch > "9" for ch in digits):
        raise ValueError("digits must contain only ASCII digits 0-9")

    rem = 0
    for i in range(0, len(digits), _CHUNK):
        chunk = digits[i : i + _CHUNK]
        # (rem * 10**len(chunk) + chunk) mod 97, keeping intermediates small.
        rem = (rem * (10 ** len(chunk)) + int(chunk)) % 97
    return rem


def is_valid_iban_numeric(digits: str) -> bool:
    """True iff ``digits`` is valid input whose mod-97 remainder equals 1.

    Invalid input (empty, non-digits, wrong type) returns False instead of
    raising.
    """
    try:
        return remainder(digits) == 1
    except ValueError:
        return False
