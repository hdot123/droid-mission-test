"""(7,4) Hamming code.

Convention: data bits d1d2d3d4 (4 bits, integer 0-15, binary most-significant-bit
first); the 7-bit codeword most-significant-bit first is p1 p2 d1 p3 d2 d3 d4,
where p1 checks d1d2d4, p2 checks d1d3d4, p3 checks d2d3d4, all even parity.
"""

__all__ = ["encode", "decode"]


def _parity(bits):
    """Even parity bit for the given bit values (0/1)."""
    total = 0
    for bit in bits:
        total ^= bit
    return total


def encode(data: int) -> int:
    """Encode 4 data bits (0-15) into a 7-bit Hamming codeword (0-127)."""
    if not isinstance(data, int) or isinstance(data, bool) or not 0 <= data <= 15:
        raise ValueError("data must be an integer in 0..15")

    # Data bits d1 d2 d3 d4, most-significant-bit first.
    d1 = (data >> 3) & 1
    d2 = (data >> 2) & 1
    d3 = (data >> 1) & 1
    d4 = data & 1

    p1 = _parity([d1, d2, d4])
    p2 = _parity([d1, d3, d4])
    p3 = _parity([d2, d3, d4])

    # Codeword MSB first: p1 p2 d1 p3 d2 d3 d4
    return (p1 << 6) | (p2 << 5) | (d1 << 4) | (p3 << 3) | (d2 << 2) | (d3 << 1) | d4


def decode(code: int) -> int:
    """Decode a 7-bit codeword (0-127), correcting a single bit error first."""
    if not isinstance(code, int) or isinstance(code, bool) or not 0 <= code <= 127:
        raise ValueError("code must be an integer in 0..127")

    # Codeword MSB first: p1 p2 d1 p3 d2 d3 d4
    bits = [
        (code >> 6) & 1,  # p1
        (code >> 5) & 1,  # p2
        (code >> 4) & 1,  # d1
        (code >> 3) & 1,  # p3
        (code >> 2) & 1,  # d2
        (code >> 1) & 1,  # d3
        code & 1,         # d4
    ]
    p1, p2, d1, p3, d2, d3, d4 = bits

    # Syndrome: each check group must have even parity.
    s1 = _parity([p1, d1, d2, d4])
    s2 = _parity([p2, d1, d3, d4])
    s3 = _parity([p3, d2, d3, d4])

    if s1 or s2 or s3:
        # Syndrome maps to the position of the single erroneous bit.
        # Positions MSB first: p1(1) p2(2) d1(3) p3(4) d2(5) d3(6) d4(7).
        position = (s3 << 2) | (s2 << 1) | s1
        bits[position - 1] ^= 1
        p1, p2, d1, p3, d2, d3, d4 = bits

    # Data bits d1 d2 d3 d4 as a 4-bit integer, MSB first.
    return (d1 << 3) | (d2 << 2) | (d3 << 1) | d4
