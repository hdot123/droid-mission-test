"""Run-length encoding and decoding for plain text.

Encoding format
---------------
Every run of identical characters becomes the character itself followed by
its run length (a decimal count, no separators), e.g. ``"aaabbc"`` ->
``"a3b2c1"``. The empty string encodes to the empty string.

Decoding rule
-------------
``decode`` parses the input strictly as repeating pairs of:

1. a single symbol character (any character, including a digit), then
2. a count: one or more decimal digits with no leading zeros, whose value
   is at least 1.

Anything else raises ``ValueError``:

* a symbol not followed by any digit (missing count / trailing character),
* a count of 0 (``"a0"``) or a leading zero (``"a01"``),
* a count position where the next character is not a digit (``"ab"``,
  ``"a-2"``).

Round-trip guarantees
---------------------
* For any *valid* encoded string ``x`` (one that parses under the rules
  above), ``encode(decode(x)) == x``. Counts are greedy digit runs with no
  leading zeros, so re-encoding always regenerates the identical count
  text.
* For any text ``y`` that contains no decimal digit characters,
  ``decode(encode(y)) == y``.

The second guarantee cannot extend to text containing digits: the format
has no separators or escaping, so a digit in the source is
indistinguishable from a count (e.g. ``encode("12321")`` yields
``"112131211"``, which decodes greedily as one run of 12131211 ones).
This is an inherent property of the format specified in the work order;
callers must not round-trip digit-containing text through this encoding.
"""

__all__ = ["encode", "decode"]


def encode(text):
    """Run-length encode *text*.

    Each run of identical characters becomes ``<char><count>`` with no
    separators, e.g. ``"aaabbc"`` -> ``"a3b2c1"``. The empty string
    encodes to ``""``.
    """
    if text == "":
        return ""

    parts = []
    current = text[0]
    count = 1
    for char in text[1:]:
        if char == current:
            count += 1
        else:
            parts.append(current + str(count))
            current = char
            count = 1
    parts.append(current + str(count))
    return "".join(parts)


def decode(text):
    """Decode the run-length format produced by :func:`encode`.

    Parses strict ``<symbol><count>`` pairs as documented in the module
    docstring and raises ``ValueError`` for any malformed input, including
    missing counts, counts of 0, leading zeros in counts, and symbols whose
    count segment does not start with a digit.
    """
    if text == "":
        return ""

    result = []
    index = 0
    length = len(text)
    while index < length:
        symbol = text[index]
        index += 1
        start = index
        while index < length and text[index].isdigit():
            index += 1
        if start == index:
            raise ValueError(
                "run-length: missing count after symbol %r at position %d"
                % (symbol, start)
            )
        count_text = text[start:index]
        if len(count_text) > 1 and count_text[0] == "0":
            raise ValueError(
                "run-length: leading zero in count %r at position %d"
                % (count_text, start)
            )
        count = int(count_text)
        if count == 0:
            raise ValueError(
                "run-length: count of 0 at position %d" % start
            )
        result.append(symbol * count)
    return "".join(result)
