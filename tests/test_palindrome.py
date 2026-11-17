"""Tests for palindrome.py (clean_text and is_palindrome)."""

from palindrome import clean_text, is_palindrome


def test_clean_text_strips_punctuation_symbols_and_spaces():
    assert clean_text("A man, a plan, a canal: Panama!") == "amanaplanacanalpanama"
    assert clean_text("Hello, World!") == "helloworld"
    assert clean_text("  spaces   everywhere  ") == "spaceseverywhere"
    assert clean_text("no-symbols; none: here.") == "nosymbolsnonehere"


def test_clean_text_lowercases_and_keeps_digits():
    assert clean_text("AbC123xYz") == "abc123xyz"
    assert clean_text("RACEcar") == "racecar"


def test_clean_text_empty_string():
    assert clean_text("") == ""


def test_is_palindrome_true_with_mixed_case_and_separators():
    assert is_palindrome("A man, a plan, a canal: Panama")
    assert is_palindrome("Racecar")
    assert is_palindrome("Was it a car or a cat I saw?")
    assert is_palindrome("No 'x' in Nixon")


def test_is_palindrome_false_cases():
    assert not is_palindrome("hello")
    assert not is_palindrome("palindrome")
    assert not is_palindrome("ab")


def test_is_palindrome_empty_string_is_palindrome():
    assert is_palindrome("")
    assert is_palindrome("   ,,, !!! ")


def test_is_palindrome_single_character():
    assert is_palindrome("a")
    assert is_palindrome("Z")
    assert is_palindrome("7")
    assert is_palindrome("!!")  # cleans to empty, which is a palindrome
