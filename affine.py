"""Affine cipher (mod 26).

E(x) = (a*x + b) mod 26, with ``a`` coprime to 26 so the map is a
bijection; ``decode`` applies the modular inverse of ``a``.
Standard library only; no imports from other cipher modules.
"""

from math import gcd

__all__ = ["encode", "decode"]


def _check_key(a: int) -> None:
    if gcd(a, 26) != 1:
        raise ValueError(f"a={a} is not coprime with 26")


def _transform(text: str, a: int, b: int) -> str:
    _check_key(a)
    out = []
    for ch in text:
        if ch.isascii() and ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            x = ord(ch) - base
            out.append(chr((a * x + b) % 26 + base))
        else:
            out.append(ch)
    return "".join(out)


def encode(text: str, a: int, b: int) -> str:
    """Encrypt ``text`` with E(x) = (a*x + b) mod 26."""
    return _transform(text, a, b)


def decode(text: str, a: int, b: int) -> str:
    """Decrypt ``text``; the inverse of :func:`encode`."""
    _check_key(a)
    a_inv = pow(a, -1, 26)
    return _transform(text, a_inv, (-a_inv * b) % 26)
