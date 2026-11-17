"""Text cleaning and palindrome checking utilities."""

import string


def clean_text(text):
    """Return only alphanumeric characters from text, lowercased."""
    return "".join(ch.lower() for ch in text if ch.isalnum())


def is_palindrome(text):
    """Judge whether text is a palindrome based on clean_text.

    An empty string after cleaning counts as a palindrome.
    """
    cleaned = clean_text(text)
    return cleaned == cleaned[::-1]
