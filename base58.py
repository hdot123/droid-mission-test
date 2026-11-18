"""Base58 byte codec (Bitcoin-style alphabet, 0/O/I/l removed)."""

ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

_INDEX = {c: i for i, c in enumerate(ALPHABET)}


def b58encode(data: bytes) -> str:
    """Encode bytes as a big-endian base58 string.

    Each leading 0x00 byte becomes one leading '1' character.
    An empty byte string encodes to an empty string.
    """
    if not isinstance(data, bytes):
        raise TypeError(f"expected bytes, got {type(data).__name__}")

    zeros = 0
    while zeros < len(data) and data[zeros] == 0:
        zeros += 1

    num = int.from_bytes(data, "big")
    body = ""
    while num > 0:
        num, rem = divmod(num, 58)
        body = ALPHABET[rem] + body

    return "1" * zeros + body


def b58decode(text: str) -> bytes:
    """Decode a base58 string back to bytes (inverse of b58encode).

    An empty string decodes to b"". Characters outside the alphabet
    raise ValueError.
    """
    if not isinstance(text, str):
        raise TypeError(f"expected str, got {type(text).__name__}")

    zeros = 0
    while zeros < len(text) and text[zeros] == "1":
        zeros += 1

    num = 0
    for ch in text:
        try:
            digit = _INDEX[ch]
        except KeyError:
            raise ValueError(f"invalid base58 character: {ch!r}") from None
        num = num * 58 + digit

    body = num.to_bytes((num.bit_length() + 7) // 8, "big") if num else b""
    return b"\x00" * zeros + body
