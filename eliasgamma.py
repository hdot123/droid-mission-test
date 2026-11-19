"""Elias gamma coding over bit strings.

Functions:
    elias_encode(n) / elias_decode(bits)
    elias_encode_list(nums) / elias_decode_list(bits)
"""

__all__ = ["elias_encode", "elias_decode", "elias_encode_list", "elias_decode_list"]


def elias_encode(n: int) -> str:
    """Encode a positive integer n (>= 1) as an Elias gamma bit string.

    Writes L-1 zero bits followed by the binary representation of n,
    where L is the bit length of n.
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an int")
    if n < 1:
        raise ValueError("n must be >= 1")
    binary = bin(n)[2:]
    return "0" * (len(binary) - 1) + binary


def elias_decode(bits: str) -> int:
    """Decode a bit string holding exactly one Elias gamma codeword."""
    if not isinstance(bits, str):
        raise TypeError("bits must be a str")
    if bits == "":
        raise ValueError("bits must be a non-empty Elias gamma codeword")
    for ch in bits:
        if ch not in ("0", "1"):
            raise ValueError("bits may only contain '0' and '1'")
    z = 0
    while z < len(bits) and bits[z] == "0":
        z += 1
    # A codeword is z zero bits followed by z+1 value bits: total 2z+1.
    if len(bits) != 2 * z + 1:
        raise ValueError("bits must contain exactly one complete codeword")
    return int(bits[z:], 2)


def elias_encode_list(nums) -> str:
    """Encode each element of a list/tuple and concatenate the codewords."""
    if not isinstance(nums, (list, tuple)):
        raise TypeError("nums must be a list or tuple")
    return "".join(elias_encode(n) for n in nums)


def elias_decode_list(bits: str) -> list:
    """Decode a concatenated Elias gamma bit string into a list of ints."""
    if not isinstance(bits, str):
        raise TypeError("bits must be a str")
    result = []
    pos = 0
    length = len(bits)
    while pos < length:
        if bits[pos] not in ("0", "1"):
            raise ValueError("bits may only contain '0' and '1'")
        z = 0
        while pos + z < length and bits[pos + z] == "0":
            z += 1
        total = 2 * z + 1
        if pos + total > length:
            raise ValueError("truncated Elias gamma codeword")
        body = bits[pos + z:pos + total]
        if any(c not in ("0", "1") for c in body):
            raise ValueError("bits may only contain '0' and '1'")
        result.append(int(body, 2))
        pos += total
    return result
