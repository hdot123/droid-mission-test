"""Chaocipher: dual-alphabet evolving substitution cipher.

Left alphabet is the ciphertext side, right alphabet is the plaintext side.
Both alphabets are pinned permutations of A-Z and evolve after every letter.
Standard library only; no imports from sibling modules.
"""

from __future__ import annotations

LEFT_ALPHABET = "HXUCZVAMDSLKPEFJRIGTWOBNYQ"  # ciphertext side
RIGHT_ALPHABET = "PTLNBQDEOYSFAVZKGJRIHWXUMC"  # plaintext side


def _preprocess(text: str) -> str:
    """Uppercase the input and keep only A-Z letters."""
    if not isinstance(text, str):
        raise TypeError(f"expected str, got {type(text).__name__}")
    return "".join(ch for ch in text.upper() if "A" <= ch <= "Z")


def _rotate_to_front(alphabet: list[str], ch: str) -> None:
    """Rotate the alphabet so ``ch`` sits at index 0."""
    k = alphabet.index(ch)
    alphabet[:] = alphabet[k:] + alphabet[:k]


def _permute_left(left: list[str], cipher_char: str) -> None:
    # (1) rotate so the just-produced ciphertext letter reaches index 0,
    #     then take the letter at index 1 and insert it at index 13
    #     (pre-removal frame: after the pop it lands at index 12, i.e.
    #     before the element that was originally at index 13).
    _rotate_to_front(left, cipher_char)
    letter = left.pop(1)
    left.insert(12, letter)


def _permute_right(right: list[str], plain_char: str) -> None:
    # (2) rotate so the just-consumed plaintext letter reaches index 0,
    #     rotate left by one, then take the letter at index 2 and insert it
    #     at index 13 (pre-removal frame: insert index 12 after the pop).
    _rotate_to_front(right, plain_char)
    right[:] = right[1:] + right[:1]
    letter = right.pop(2)
    right.insert(12, letter)


def chaocipher_encrypt(text: str) -> str:
    """Encrypt ``text`` with the Chaocipher dual-alphabet evolution."""
    plain = _preprocess(text)
    left = list(LEFT_ALPHABET)
    right = list(RIGHT_ALPHABET)
    out: list[str] = []
    for ch in plain:
        idx = right.index(ch)
        enc = left[idx]
        out.append(enc)
        _permute_left(left, enc)
        _permute_right(right, ch)
    return "".join(out)


def chaocipher_decrypt(cipher: str) -> str:
    """Decrypt ``cipher`` produced by :func:`chaocipher_encrypt`."""
    enc_text = _preprocess(cipher)
    left = list(LEFT_ALPHABET)
    right = list(RIGHT_ALPHABET)
    out: list[str] = []
    for ch in enc_text:
        idx = left.index(ch)
        dec = right[idx]
        out.append(dec)
        _permute_left(left, ch)
        _permute_right(right, dec)
    return "".join(out)
