"""Pig Latin translation for single English words.

Standard library only; this module imports nothing from the repository.
"""

VOWELS = set("aeiouAEIOU")


def translate(word):
    """Translate a single English word to pig Latin.

    Rules:
    - Words starting with a vowel (a/e/i/o/u, case-insensitive) get "way"
      appended.
    - Words starting with a consonant move the initial consecutive
      consonants to the end and add "ay".
    - Capitalization shape is preserved: all-lowercase input produces an
      all-lowercase output; initial-capital input produces an
      initial-capital output.
    - An empty string is invalid and raises ValueError.
    """
    if not isinstance(word, str):
        raise ValueError("translate() expects a string")
    if word == "":
        raise ValueError("translate() expects a non-empty string")
    if not word.isalpha():
        raise ValueError("translate() expects a single alphabetic word")

    lower = word.lower()
    if lower[0] in VOWELS:
        pig = lower + "way"
    else:
        i = 0
        while i < len(lower) and lower[i] not in VOWELS:
            i += 1
        pig = lower[i:] + lower[:i] + "ay"

    if word[0].isupper():
        return pig[0].upper() + pig[1:]
    return pig
