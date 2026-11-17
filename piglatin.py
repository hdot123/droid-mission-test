"""Pig latin translation utilities (standard library only)."""

VOWELS = set("aeiou")


def translate(word: str) -> str:
    """Convert a single word to pig latin.

    Input is treated as lowercase and the result is always lowercase.
    Words starting with a vowel get "way" appended; words starting with a
    consonant move the entire leading consonant cluster to the end and add
    "ay". The empty string returns "".
    """
    w = word.lower()
    if not w:
        return ""
    if w[0] in VOWELS:
        return w + "way"
    i = 0
    while i < len(w) and w[i] not in VOWELS:
        i += 1
    return w[i:] + w[:i] + "ay"


def translate_sentence(s: str) -> str:
    """Translate each space-separated word and join results with a space."""
    return " ".join(translate(word) for word in s.split(" "))
