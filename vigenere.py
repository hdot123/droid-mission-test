"""Vigenere cipher: encrypt/decrypt with a letter-only key."""


def _validate_key(key):
    if not isinstance(key, str) or key == "" or not key.isascii() or not key.isalpha():
        raise ValueError("key must be a non-empty string of English letters")


def encrypt(text, key):
    """Encrypt ``text`` with the Vigenere cipher using ``key``."""
    _validate_key(key)
    key_upper = key.upper()
    result = []
    key_index = 0
    for char in text:
        if char.isascii() and char.isalpha():
            shift = ord(key_upper[key_index % len(key_upper)]) - ord("A")
            base = ord("A") if char.isupper() else ord("a")
            result.append(chr((ord(char) - base + shift) % 26 + base))
            key_index += 1
        else:
            result.append(char)
    return "".join(result)


def decrypt(text, key):
    """Decrypt ``text`` with the Vigenere cipher using ``key``."""
    _validate_key(key)
    key_upper = key.upper()
    result = []
    key_index = 0
    for char in text:
        if char.isascii() and char.isalpha():
            shift = ord(key_upper[key_index % len(key_upper)]) - ord("A")
            base = ord("A") if char.isupper() else ord("a")
            result.append(chr((ord(char) - base - shift) % 26 + base))
            key_index += 1
        else:
            result.append(char)
    return "".join(result)
