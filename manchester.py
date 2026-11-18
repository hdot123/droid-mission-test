"""Manchester coding (IEEE 802.3 convention).

Each input bit maps to two symbols:
    '0' -> '10'
    '1' -> '01'
"""


def encode(bits: str) -> str:
    """Encode a string of '0'/'1' bits into Manchester symbols."""
    out = []
    for ch in bits:
        if ch == "0":
            out.append("10")
        elif ch == "1":
            out.append("01")
        else:
            raise ValueError(f"invalid bit character: {ch!r}")
    return "".join(out)


def decode(symbols: str) -> str:
    """Decode Manchester symbols back into a string of '0'/'1' bits."""
    if len(symbols) % 2 != 0:
        raise ValueError("symbol string has odd length")
    out = []
    for i in range(0, len(symbols), 2):
        pair = symbols[i:i + 2]
        if pair == "10":
            out.append("0")
        elif pair == "01":
            out.append("1")
        else:
            raise ValueError(f"illegal symbol pair: {pair!r}")
    return "".join(out)
