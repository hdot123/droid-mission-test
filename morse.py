"""International Morse code encoding and decoding for A-Z and 0-9."""

MORSE = {
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

DECODE = {code: ch for ch, code in MORSE.items()}


def encode(text: str) -> str:
    """Encode uppercase text into Morse code.

    Letters are separated by a single space; words (original spaces) are
    separated by ' / '. Any character outside A-Z, 0-9 and space raises
    ValueError. Empty string returns empty string.
    """
    if text == "":
        return ""
    words = text.upper().split(" ")
    encoded_words = []
    for word in words:
        if word == "":
            raise ValueError("malformed input: consecutive spaces")
        letters = []
        for ch in word:
            if ch not in MORSE:
                raise ValueError(f"unsupported character: {ch!r}")
            letters.append(MORSE[ch])
        encoded_words.append(" ".join(letters))
    return " / ".join(encoded_words)


def decode(code: str) -> str:
    """Decode Morse code into uppercase text.

    Words separated by ' / ' become single spaces in the output. Unknown
    code groups or malformed forms (e.g. consecutive spaces) raise
    ValueError. Empty string returns empty string.
    """
    if code == "":
        return ""
    words = code.split(" / ")
    decoded_words = []
    for word in words:
        if word == "":
            raise ValueError("malformed code: empty word")
        groups = word.split(" ")
        letters = []
        for group in groups:
            if group == "":
                raise ValueError("malformed code: consecutive spaces")
            if group not in DECODE:
                raise ValueError(f"unknown code group: {group!r}")
            letters.append(DECODE[group])
        decoded_words.append("".join(letters))
    return " ".join(decoded_words)
