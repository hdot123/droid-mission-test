"""Morse code encoding and decoding for English letters and digits.

Standard library only. This module has no dependency on any other
project module.
"""

_MORSE = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
}

_CHAR_TO_MORSE = {char: code for char, code in _MORSE.items()}
_MORSE_TO_CHAR = {code: char for char, code in _MORSE.items()}


def encode(text):
    """Encode letters and digits into Morse code.

    Character codes are separated by a single space; words are separated
    by `` / ``. Letters are encoded case-insensitively. Raises ValueError
    on any character other than a letter, digit, or space.
    """
    if not text:
        return ""
    words = []
    for word in text.split(" "):
        if not word:
            continue
        codes = []
        for char in word:
            code = _CHAR_TO_MORSE.get(char.upper())
            if code is None:
                raise ValueError("unsupported character for encoding: %r" % char)
            codes.append(code)
        words.append(" ".join(codes))
    return " / ".join(words)


def decode(code):
    """Decode Morse code back into uppercase letters and digits.

    Words are separated by a single space in the result. Raises ValueError
    on any unknown (or empty) code group.
    """
    if not code or not code.strip():
        return ""
    words = []
    for word in code.split("/"):
        chars = []
        for token in word.split():
            char = _MORSE_TO_CHAR.get(token)
            if char is None:
                raise ValueError("unknown Morse code group: %r" % token)
            chars.append(char)
        if not chars:
            raise ValueError("unknown Morse code group: empty word")
        words.append("".join(chars))
    return " ".join(words)
