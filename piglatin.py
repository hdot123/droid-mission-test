"""Pig Latin translation utilities (standard library only)."""

VOWELS = set("aeiou")


def translate_word(word):
    """Convert a single lowercase English word to Pig Latin.

    - A word starting with a vowel gets "way" appended.
    - A word starting with a consonant moves the entire leading consonant
      cluster to the end, then appends "ay".
    - A word with no vowels at all is treated as an all-consonant cluster:
      the original word plus "ay".
    """
    for i, ch in enumerate(word):
        if ch in VOWELS:
            if i == 0:
                return word + "way"
            return word[i:] + word[:i] + "ay"
    # No vowels at all: treat the whole word as a consonant cluster.
    return word + "ay"


def translate(sentence):
    """Translate a sentence of single-space-separated lowercase words."""
    return " ".join(translate_word(w) for w in sentence.split(" "))
