def is_anagram(a: str, b: str) -> bool:
    """Return True if the English letters in a and b are anagrams.

    Only English letters are compared; case and all other characters are
    ignored. Two strings with no letters at all are anagrams (True).
    """
    letters_a = [ch.lower() for ch in a if ch.isalpha() and ch.isascii()]
    letters_b = [ch.lower() for ch in b if ch.isalpha() and ch.isascii()]
    return sorted(letters_a) == sorted(letters_b)
