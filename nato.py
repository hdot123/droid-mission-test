"""NATO phonetic alphabet spelling utility (standard library only)."""

_NATO = (
    "Alfa",
    "Bravo",
    "Charlie",
    "Delta",
    "Echo",
    "Foxtrot",
    "Golf",
    "Hotel",
    "India",
    "Juliett",
    "Kilo",
    "Lima",
    "Mike",
    "November",
    "Oscar",
    "Papa",
    "Quebec",
    "Romeo",
    "Sierra",
    "Tango",
    "Uniform",
    "Victor",
    "Whiskey",
    "Xray",
    "Yankee",
    "Zulu",
)


def spell(word):
    """Convert an English word to NATO phonetic names joined by hyphens.

    Input is case-insensitive; output is normalized to initial-capital form.
    Raises ValueError if the word contains any non-letter character.
    """
    if not isinstance(word, str):
        raise ValueError("word must be a string")
    if not word.isalpha():
        raise ValueError("word must contain only letters: %r" % (word,))
    return "-".join(_NATO[ord(ch.upper()) - ord("A")] for ch in word)
