"""International Morse code encoding and decoding.

Supports uppercase letters A-Z, digits 0-9, and spaces only.
"""

MORSE_TABLE = {
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

DECODE_TABLE = {code: char for char, code in MORSE_TABLE.items()}

WORD_SEPARATOR = " / "


def encode(text):
    """Encode text into Morse code.

    Letters are separated by a single space, words by " / ".
    Raises ValueError for unsupported characters (lowercase, punctuation, etc.).
    """
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    words = text.split(" ")
    encoded_words = []
    for word in words:
        if word == "":
            raise ValueError("unsupported character in input: empty word")
        codes = []
        for ch in word:
            if ch not in MORSE_TABLE:
                raise ValueError("unsupported character: %r" % (ch,))
            codes.append(MORSE_TABLE[ch])
        encoded_words.append(" ".join(codes))
    return WORD_SEPARATOR.join(encoded_words)


def decode(code):
    """Decode Morse code back into text.

    Letters are separated by a single space, words by " / ".
    Raises ValueError for unknown code groups or unsupported input.
    """
    if not isinstance(code, str):
        raise ValueError("code must be a string")
    if code == "":
        raise ValueError("empty code")
    words = code.split(WORD_SEPARATOR)
    decoded_words = []
    for word in words:
        if word == "":
            raise ValueError("empty code group")
        groups = word.split(" ")
        chars = []
        for group in groups:
            if group == "" or group not in DECODE_TABLE:
                raise ValueError("unknown code group: %r" % (group,))
            chars.append(DECODE_TABLE[group])
        decoded_words.append("".join(chars))
    return " ".join(decoded_words)
