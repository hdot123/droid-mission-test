"""Tests for piglatin module behavior only."""

import piglatin


def test_translate_word_vowel_start():
    assert piglatin.translate_word("apple") == "appleway"


def test_translate_word_consonant_start():
    assert piglatin.translate_word("hello") == "ellohay"


def test_translate_word_consonant_cluster():
    assert piglatin.translate_word("string") == "ingstray"


def test_translate_word_no_vowels():
    assert piglatin.translate_word("rhythm") == "rhythmay"


def test_translate_sentence():
    assert piglatin.translate("hello world") == "ellohay orldway"
