"""Fraction arithmetic implemented from scratch (no fractions module)."""

import re

__all__ = ["Fraction", "parse"]


def _gcd(a: int, b: int) -> int:
    a = abs(a)
    b = abs(b)
    while b:
        a, b = b, a % b
    return a


class Fraction:
    """A rational number reduced to lowest terms with a positive denominator."""

    def __init__(self, numerator: int, denominator: int = 1):
        if denominator == 0:
            raise ValueError("denominator must not be zero")
        n = int(numerator)
        d = int(denominator)
        if d < 0:
            n = -n
            d = -d
        g = _gcd(n, d)
        if g:
            n //= g
            d //= g
        self._numerator = n
        self._denominator = d

    @property
    def numerator(self) -> int:
        return self._numerator

    @property
    def denominator(self) -> int:
        return self._denominator

    def __add__(self, other):
        if not isinstance(other, Fraction):
            return NotImplemented
        return Fraction(
            self._numerator * other._denominator + other._numerator * self._denominator,
            self._denominator * other._denominator,
        )

    def __sub__(self, other):
        if not isinstance(other, Fraction):
            return NotImplemented
        return Fraction(
            self._numerator * other._denominator - other._numerator * self._denominator,
            self._denominator * other._denominator,
        )

    def __mul__(self, other):
        if not isinstance(other, Fraction):
            return NotImplemented
        return Fraction(
            self._numerator * other._numerator,
            self._denominator * other._denominator,
        )

    def __truediv__(self, other):
        if not isinstance(other, Fraction):
            return NotImplemented
        if other._numerator == 0:
            raise ZeroDivisionError("division by zero fraction")
        return Fraction(
            self._numerator * other._denominator,
            self._denominator * other._numerator,
        )

    def __eq__(self, other):
        if not isinstance(other, Fraction):
            return NotImplemented
        return (
            self._numerator == other._numerator
            and self._denominator == other._denominator
        )

    def __str__(self) -> str:
        if self._denominator == 1:
            return str(self._numerator)
        return f"{self._numerator}/{self._denominator}"

    def __repr__(self) -> str:
        return f"Fraction({self._numerator}, {self._denominator})"


# Accepted forms: '3/4', '-3/4', or an integer such as '5'.
# Whitespace (leading, trailing, or interior) is never allowed.
_PARSE_RE = re.compile(r"(-?\d+)(?:/(\d+))?\Z")


def parse(text: str) -> Fraction:
    """Parse '3/4', '-3/4', or an integer like '5'. Whitespace is not allowed."""
    if not isinstance(text, str):
        raise ValueError("input must be a string")
    match = _PARSE_RE.match(text)
    if match is None:
        raise ValueError(f"malformed fraction: {text!r}")
    num_text, den_text = match.group(1), match.group(2)
    if den_text is None:
        return Fraction(int(num_text), 1)
    if den_text == "0":
        raise ValueError("denominator must not be zero")
    return Fraction(int(num_text), int(den_text))
