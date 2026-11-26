"""Parity-bit helpers: append, check, and strip an even/odd parity bit.

Standard library only; no imports from sibling modules.
"""

__all__ = ["append_parity", "check_parity", "strip_parity"]

_MODES = ("even", "odd")


def _validate_mode(mode: str) -> None:
    if not isinstance(mode, str):
        raise TypeError("mode must be a str")
    if mode not in _MODES:
        raise ValueError("mode must be 'even' or 'odd'")


def _validate_bits(bits) -> None:
    if not isinstance(bits, str):
        raise TypeError("bits must be a str")
    if bits == "":
        raise ValueError("bits must be a non-empty string")
    if any(ch not in "01" for ch in bits):
        raise ValueError("bits may only contain '0' and '1'")


def append_parity(bits: str, mode: str = "even") -> str:
    """Append one parity bit so the whole string satisfies ``mode``.

    ``mode="even"`` makes the total number of 1s even; ``mode="odd"``
    makes it odd. Raises ValueError for an empty string, characters
    outside 0-1, or an unknown mode; TypeError for non-str input.
    """
    _validate_bits(bits)
    _validate_mode(mode)
    ones = bits.count("1")
    if mode == "even":
        parity = ones % 2
    else:
        parity = 1 - (ones % 2)
    return bits + str(parity)


def check_parity(bits: str, mode: str = "even") -> bool:
    """Return True if the total number of 1s satisfies ``mode``."""
    _validate_bits(bits)
    _validate_mode(mode)
    ones = bits.count("1")
    if mode == "even":
        return ones % 2 == 0
    return ones % 2 == 1


def strip_parity(bits: str) -> str:
    """Remove the parity bit (the last character) and return the rest.

    Raises ValueError if the input length is < 2 (including the empty
    string) or contains characters outside 0-1; TypeError for non-str.
    """
    if not isinstance(bits, str):
        raise TypeError("bits must be a str")
    if len(bits) < 2:
        raise ValueError("bits must be at least 2 characters long")
    if any(ch not in "01" for ch in bits):
        raise ValueError("bits may only contain '0' and '1'")
    return bits[:-1]
