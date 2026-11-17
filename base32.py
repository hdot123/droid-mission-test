"""RFC 4648 standard Base32 encoding and decoding.

Uppercase alphabet (A-Z plus 2-7) with '=' padding.
"""

import base64
import re

_PATTERN = re.compile(r"\A[A-Z2-7]+={0,6}\Z")

# Number of trailing '=' required for a given number of alphabet characters
# in the final (partial) group.  Key is (alphabet chars) % 8.
_PADS = {0: 0, 2: 6, 4: 4, 5: 3, 7: 1}


def encode(data: bytes) -> str:
    """Encode *data* as RFC 4648 standard Base32 (uppercase, padded)."""
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be a bytes-like object")
    return base64.b32encode(bytes(data)).decode("ascii")


def decode(s: str) -> bytes:
    """Decode a canonical, padded, uppercase Base32 string.

    Raises ValueError on illegal characters, non-uppercase input,
    or bad/missing padding.  The empty string decodes to b"".
    """
    if not isinstance(s, str):
        raise ValueError("input must be a string")
    if s == "":
        return b""
    if not _PATTERN.match(s):
        raise ValueError("invalid base32: illegal characters, non-uppercase "
                         "input, or misplaced padding")
    pad = len(s) - len(s.rstrip("="))
    if len(s) % 8 != 0 or _PADS.get((len(s) - pad) % 8) != pad:
        raise ValueError("invalid base32: incorrect padding")
    try:
        return base64.b32decode(s)
    except ValueError as exc:  # binascii.Error is a ValueError subclass
        raise ValueError("invalid base32 data") from exc
