"""Morse code encoder/decoder for letters, digits, and spaces."""

_MORSE_TO_CHAR = {
    ".-": "A",
    "-...": "B",
    "-.-.": "C",
    "-..": "D",
    ".": "E",
    "..-.": "F",
    "--.": "G",
    "....": "H",
    "..": "I",
    ".---": "J",
    "-.-": "K",
    ".-..": "L",
    "--": "M",
    "-.": "N",
    "---": "O",
    ".--.": "P",
    "--.-": "Q",
    ".-.": "R",
    "...": "S",
    "-": "T",
    "..-": "U",
    "...-": "V",
    ".--": "W",
    "-..-": "X",
    "-.--": "Y",
    "--..": "Z",
    "-----": "0",
    ".----": "1",
    "..---": "2",
    "...--": "3",
    "....-": "4",
    ".....": "5",
    "-....": "6",
    "--...": "7",
    "---..": "8",
    "----.": "9",
}

_CHAR_TO_MORSE = {char: code for code, char in _MORSE_TO_CHAR.items()}


def encode(text):
    """Convert an English string to Morse code.

    Letters and digits are separated by a single space; words are
    separated by " / ". Case-insensitive. Raises ValueError on
    characters other than ASCII letters, digits, and spaces.
    """
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    words = []
    for word in text.split():
        letters = []
        for char in word.upper():
            if char not in _CHAR_TO_MORSE:
                raise ValueError(f"illegal character: {char!r}")
            letters.append(_CHAR_TO_MORSE[char])
        words.append(" ".join(letters))
    return " / ".join(words)


def decode(code):
    """Convert Morse code back to an uppercase English string.

    Inverse of encode: words separated by " / ", letters separated by a
    single space, output words joined by a single space. Raises
    ValueError on illegal tokens.
    """
    if not isinstance(code, str):
        raise ValueError("code must be a string")
    words = []
    for word in code.split(" / "):
        letters = []
        for token in word.split(" "):
            if token == "":
                raise ValueError("empty morse token")
            if token not in _MORSE_TO_CHAR:
                raise ValueError(f"illegal morse token: {token!r}")
            letters.append(_MORSE_TO_CHAR[token])
        words.append("".join(letters))
    return " ".join(words)
