"""base64url: RFC 4648 base64url codec without padding.

Standard library only.  The URL-safe alphabet replaces '+' with '-' and
'/' with '_', and no '=' padding is emitted or accepted.
"""

import base64

_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
_DECODE_TABLE = {ch: i for i, ch in enumerate(_ALPHABET)}
_PAD_TRANS = str.maketrans("-_", "+/")


def encode(data: bytes) -> str:
    """Encode bytes as unpadded base64url text.

    Empty input encodes to the empty string.
    """
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def decode(s: str) -> bytes:
    """Decode unpadded base64url text back to bytes.

    Raises ValueError if the input contains '=', a character outside the
    base64url alphabet, or a length whose remainder mod 4 is 1.
    """
    if "=" in s:
        raise ValueError("padding is not allowed: %r" % (s,))
    for ch in s:
        if ch not in _DECODE_TABLE:
            raise ValueError("invalid character: %r" % (ch,))
    if len(s) % 4 == 1:
        raise ValueError("invalid length: %d" % (len(s),))
    padded = s + "=" * (-len(s) % 4)
    return base64.b64decode(padded.translate(_PAD_TRANS))
