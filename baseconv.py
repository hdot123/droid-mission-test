"""Arbitrary-base conversion between bases 2 and 36 (inclusive).

Digit characters are 0-9 and a-z; input letters are case-insensitive and
output is always lowercase. A leading negative sign is supported.
"""


def _digit_value(ch: str) -> int:
    """Return the numeric value of a single digit character in base <= 36."""
    if "0" <= ch <= "9":
        return ord(ch) - ord("0")
    if "a" <= ch <= "z":
        return ord(ch) - ord("a") + 10
    if "A" <= ch <= "Z":
        return ord(ch) - ord("A") + 10
    raise ValueError(f"invalid digit character: {ch!r}")


def convert(text: str, from_base: int, to_base: int) -> str:
    """Convert ``text`` written in ``from_base`` into ``to_base``.

    Raises ValueError for bases outside 2-36, empty input, a lone minus
    sign, or any digit whose value is not less than ``from_base``.
    Output has no leading zeros; zero (and negative zero) is "0".
    """
    if not isinstance(from_base, int) or not (2 <= from_base <= 36):
        raise ValueError(f"from_base must be in 2-36, got {from_base!r}")
    if not isinstance(to_base, int) or not (2 <= to_base <= 36):
        raise ValueError(f"to_base must be in 2-36, got {to_base!r}")
    if text == "":
        raise ValueError("empty input")

    negative = text.startswith("-")
    body = text[1:] if negative else text
    if body == "":
        raise ValueError("lone minus sign")

    value = 0
    for ch in body:
        d = _digit_value(ch)
        if d >= from_base:
            raise ValueError(f"digit {ch!r} not valid in base {from_base}")
        value = value * from_base + d

    if value == 0:
        return "0"

    digits = []
    while value > 0:
        value, rem = divmod(value, to_base)
        digits.append("0123456789abcdefghijklmnopqrstuvwxyz"[rem])
    result = "".join(reversed(digits))
    return "-" + result if negative else result
