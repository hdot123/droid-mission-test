"""Pig Latin translation for single English words (standard library only)."""

VOWELS = set("aeiouAEIOU")


def translate(word):
    """Translate a single English word to Pig Latin.

    Words starting with a vowel (a/e/i/o/u, case-insensitive) get "way"
    appended. Words starting with a consonant move the leading consonant
    cluster to the end and append "ay". Case shape is preserved: an
    all-lowercase input yields an all-lowercase output, a capitalized
    input yields a capitalized output.

    Raises ValueError for non-string or empty input.
    """
    if not isinstance(word, str) or not word:
        raise ValueError("word must be a non-empty string")
    if not word.isalpha():
        raise ValueError("word must contain only letters")

    if word[0] in VOWELS:
        translated = word + "way"
    else:
        i = 0
        while i < len(word) and word[i] not in VOWELS:
            i += 1
        translated = word[i:] + word[:i] + "ay"

    # Preserve case shape: all-lowercase in -> all-lowercase out,
    # capitalized in -> capitalized out.
    if word.islower():
        return translated.lower()
    if word.istitle():
        return translated.capitalize()
    return translated
