"""A1Z26 letter-index encoding.

`a1z26_encode` maps uppercase A-Z (words separated by a single space) to
1-26 indices joined with "-" inside a word and with a single space between
words. `a1z26_decode` performs the inverse transform with strict input
validation (indices 1-26, no leading zeros, no empty segments).

Standard library only.
"""

__all__ = ["a1z26_encode", "a1z26_decode"]


def a1z26_encode(text: str) -> str:
    """Encode uppercase A-Z text into A1Z26 indices.

    Accepts only uppercase letters A-Z separated by single spaces.
    Raises TypeError for non-str input and ValueError for lowercase
    letters, digits, or consecutive/leading/trailing spaces.
    """
    if not isinstance(text, str):
        raise TypeError(
            f"a1z26_encode expects str, got {type(text).__name__}"
        )
    if text == "":
        return ""
    words = text.split(" ")
    for word in words:
        if word == "":
            raise ValueError(
                "a1z26_encode: leading, trailing, or consecutive spaces"
            )
        for ch in word:
            if not ("A" <= ch <= "Z"):
                raise ValueError(
                    f"a1z26_encode: invalid character {ch!r}; "
                    "only uppercase A-Z and single spaces allowed"
                )
    encoded_words = []
    for word in words:
        encoded_words.append(
            "-".join(str(ord(ch) - ord("A") + 1) for ch in word)
        )
    return " ".join(encoded_words)


def a1z26_decode(code: str) -> str:
    """Decode A1Z26 indices back into uppercase A-Z text.

    Indices must be 1-26 with no leading zeros; segments are joined by
    "-" inside a word and words by a single space, symmetric with
    `a1z26_encode`. Raises TypeError for non-str input and ValueError
    for out-of-range indices, leading zeros, empty segments, or spaces
    inside a word.
    """
    if not isinstance(code, str):
        raise TypeError(
            f"a1z26_decode expects str, got {type(code).__name__}"
        )
    if code == "":
        return ""
    decoded_words = []
    for word in code.split(" "):
        if word == "":
            raise ValueError(
                "a1z26_decode: leading, trailing, or consecutive spaces"
            )
        letters = []
        for segment in word.split("-"):
            if segment == "":
                raise ValueError("a1z26_decode: empty segment")
            if not segment.isdigit() or not segment.isascii():
                raise ValueError(
                    f"a1z26_decode: invalid segment {segment!r}"
                )
            if len(segment) > 1 and segment[0] == "0":
                raise ValueError(
                    f"a1z26_decode: leading zero in segment {segment!r}"
                )
            value = int(segment)
            if not 1 <= value <= 26:
                raise ValueError(
                    f"a1z26_decode: index {value} out of range 1-26"
                )
            letters.append(chr(ord("A") + value - 1))
        decoded_words.append("".join(letters))
    return " ".join(decoded_words)
