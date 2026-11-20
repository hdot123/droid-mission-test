"""Elias gamma encoding over bit strings.

Encoding of an integer n >= 1: let L be the length of n's binary
representation; the codeword is L-1 zeros followed by the binary
representation of n (no leading zeros).
"""


def elias_encode(n: int) -> str:
    """Encode n (an int >= 1, bool rejected) as an Elias gamma bit string."""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be int, got {type(n).__name__}")
    if n < 1:
        raise ValueError(f"n must be >= 1, got {n}")
    binary = bin(n)[2:]
    return "0" * (len(binary) - 1) + binary


def elias_decode(bits: str) -> int:
    """Decode exactly one complete Elias gamma codeword from bits."""
    if not isinstance(bits, str):
        raise TypeError(f"bits must be str, got {type(bits).__name__}")
    if not bits:
        raise ValueError("empty string is not a codeword")
    for ch in bits:
        if ch not in ("0", "1"):
            raise ValueError(f"invalid bit character {ch!r}")
    z = 0
    while z < len(bits) and bits[z] == "0":
        z += 1
    end = z + z + 1
    if end > len(bits):
        raise ValueError("truncated codeword")
    if end != len(bits):
        raise ValueError("trailing bits after codeword")
    return int(bits[z:end], 2)


def elias_encode_list(nums) -> str:
    """Encode a list/tuple of ints, concatenating codeword head to tail."""
    if not isinstance(nums, (list, tuple)):
        raise TypeError(f"nums must be list or tuple, got {type(nums).__name__}")
    return "".join(elias_encode(n) for n in nums)


def elias_decode_list(bits: str) -> list:
    """Decode a bit string that holds zero or more concatenated codewords."""
    if not isinstance(bits, str):
        raise TypeError(f"bits must be str, got {type(bits).__name__}")
    result = []
    i = 0
    n = len(bits)
    while i < n:
        if bits[i] not in ("0", "1"):
            raise ValueError(f"invalid bit character {bits[i]!r}")
        z = 0
        while i + z < n and bits[i + z] == "0":
            z += 1
        if i + z >= n:
            raise ValueError("truncated codeword")
        end = i + z + z + 1
        if end > n:
            raise ValueError("truncated codeword")
        result.append(int(bits[i + z:end], 2))
        i = end
    return result
