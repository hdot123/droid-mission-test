"""Vigenere cipher implementation."""


def _validate_key(key):
    if not isinstance(key, str) or key == "" or not key.isalpha() or not key.isascii():
        raise ValueError("key must be a non-empty string of English letters")


def encrypt(text, key):
    """Encrypt text with the Vigenere cipher using the given key."""
    _validate_key(key)
    key_upper = key.upper()
    result = []
    key_index = 0
    for ch in text:
        if ch.isalpha() and ch.isascii():
            shift = ord(key_upper[key_index % len(key_upper)]) - ord("A")
            base = ord("A") if ch.isupper() else ord("a")
            result.append(chr((ord(ch) - base + shift) % 26 + base))
            key_index += 1
        else:
            result.append(ch)
    return "".join(result)


def decrypt(text, key):
    """Decrypt text with the Vigenere cipher using the given key."""
    _validate_key(key)
    key_upper = key.upper()
    result = []
    key_index = 0
    for ch in text:
        if ch.isalpha() and ch.isascii():
            shift = ord(key_upper[key_index % len(key_upper)]) - ord("A")
            base = ord("A") if ch.isupper() else ord("a")
            result.append(chr((ord(ch) - base - shift) % 26 + base))
            key_index += 1
        else:
            result.append(ch)
    return "".join(result)
