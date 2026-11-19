"""Elias gamma coding for positive integers, as bit strings.

Standard library only; no imports from other project modules.
"""


def elias_encode(n: int) -> str:
    """Encode a positive integer ``n`` as an Elias gamma bit string.

    ``n`` must be an ``int`` (``bool`` is rejected) with ``n >= 1``.

    Encoding: let ``L`` be the bit length of ``n``.  Write ``L - 1``
    zeros followed by the binary representation of ``n`` (no leading
    zeros).

    Raises:
        TypeError: if ``n`` is not an ``int`` (``bool`` is rejected).
        ValueError: if ``n < 1``.
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be int, got {type(n).__name__}")
    if n < 1:
        raise ValueError(f"n must be >= 1, got {n}")
    bits = bin(n)[2:]
    return "0" * (len(bits) - 1) + bits


def elias_decode(bits: str) -> int:
    """Decode a string holding exactly one Elias gamma codeword.

    Raises:
        TypeError: if ``bits`` is not a ``str``.
        ValueError: if ``bits`` is empty, contains characters other than
            ``0``/``1``, is a truncated codeword, or contains trailing
            bits after one complete codeword.
    """
    if not isinstance(bits, str):
        raise TypeError(f"bits must be str, got {type(bits).__name__}")
    if not bits:
        raise ValueError("cannot decode an empty string")
    if any(ch not in "01" for ch in bits):
        raise ValueError(f"bits must contain only '0' and '1', got {bits!r}")
    z = len(bits) - len(bits.lstrip("0"))  # number of leading zeros
    codeword_len = 2 * z + 1
    if len(bits) < codeword_len:
        raise ValueError(f"truncated codeword: {bits!r}")
    if len(bits) > codeword_len:
        raise ValueError(f"trailing bits after one codeword: {bits!r}")
    return int(bits[z:], 2)


def elias_encode_list(nums) -> str:
    """Encode a list or tuple of positive integers as a concatenated
    Elias gamma bit string.

    Raises:
        TypeError: if ``nums`` is neither a ``list`` nor a ``tuple``, or
            if an element is not an ``int``.
        ValueError: if an element is ``< 1``.
    """
    if not isinstance(nums, (list, tuple)):
        raise TypeError(f"nums must be list or tuple, got {type(nums).__name__}")
    return "".join(elias_encode(n) for n in nums)


def elias_decode_list(bits: str) -> list[int]:
    """Decode a concatenated Elias gamma bit string into a list of ints.

    Decodes left to right until the string is exhausted.  An empty
    string decodes to ``[]``.

    Raises:
        TypeError: if ``bits`` is not a ``str``.
        ValueError: if the string contains invalid characters or a
            codeword is truncated mid-string.
    """
    if not isinstance(bits, str):
        raise TypeError(f"bits must be str, got {type(bits).__name__}")
    values: list[int] = []
    i = 0
    n = len(bits)
    while i < n:
        if bits[i] not in "01":
            raise ValueError(f"bits must contain only '0' and '1', got {bits!r}")
        z = 0
        while i + z < n and bits[i + z] == "0":
            z += 1
        end = i + 2 * z + 1  # exclusive end of this codeword
        if end > n:
            raise ValueError(f"truncated codeword at position {i}: {bits!r}")
        chunk = bits[i:end]
        if any(ch not in "01" for ch in chunk):
            raise ValueError(f"bits must contain only '0' and '1', got {bits!r}")
        values.append(int(chunk[z:], 2))
        i = end
    return values
