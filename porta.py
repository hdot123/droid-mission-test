"""Porta cipher: a reciprocal polyalphabetic cipher built on 13 tables.

Key letters select a table in pairs (A/B -> table 0, C/D -> table 1, ...,
Y/Z -> table 12).  Within table ``n`` the first half A-M maps onto the second
half N-Z (``A + i -> N + ((i + n) % 13)``) and the second half maps back
(``N + i -> A + ((i - n) % 13)``).  The mapping is an involution, so
encryption and decryption are the same operation.
"""

from __future__ import annotations

__all__ = ["porta_encrypt", "porta_decrypt"]

_ALPHA_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_HALF = 13


def _check_inputs(text: object, key: object) -> tuple[str, str]:
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    if not isinstance(key, str):
        raise TypeError("key must be a str")
    if not key or not all(c.isascii() and c.isalpha() for c in key):
        raise ValueError("key must be a non-empty alphabetic string")
    return text, key


def _substitute(letter: str, row: int) -> str:
    idx = ord(letter) - ord("A")
    if idx < _HALF:
        mapped = _HALF + ((idx + row) % _HALF)
    else:
        mapped = (idx - _HALF - row) % _HALF
    return _ALPHA_UPPER[mapped]


def porta_encrypt(text: str, key: str) -> str:
    """Encrypt ``text`` with the Porta cipher under ``key``.

    The key repeats and advances only over letters of the plaintext;
    non-letters are preserved as-is and the output is uppercased.
    """
    text, key = _check_inputs(text, key)
    key_upper = key.upper()
    out = []
    key_pos = 0
    key_len = len(key_upper)
    for ch in text:
        if not (ch.isascii() and ch.isalpha()):
            out.append(ch)
            continue
        row = (ord(key_upper[key_pos]) - ord("A")) // 2
        key_pos = (key_pos + 1) % key_len
        out.append(_substitute(ch.upper(), row))
    return "".join(out)


def porta_decrypt(text: str, key: str) -> str:
    """Decrypt ``text``; Porta is reciprocal, so this equals encryption."""
    return porta_encrypt(text, key)
