"""Tests for wordfreq.top_words (wordfreq module only)."""

import wordfreq


def test_case_insensitive_and_digits_mixed():
    text = "Cat cat CAT 42 dog 42dog Cat"
    assert wordfreq.top_words(text, 10) == [
        ("cat", 4),
        ("42", 1),
        ("42dog", 1),
        ("dog", 1),
    ]


def test_punctuation_splits_words():
    text = "hello, world! hello-world; (world)"
    assert wordfreq.top_words(text, 10) == [("world", 3), ("hello", 2)]


def test_frequency_descending_order():
    text = "a a a b b c"
    assert wordfreq.top_words(text, 3) == [("a", 3), ("b", 2), ("c", 1)]


def test_ties_sorted_alphabetically():
    text = "pear apple apple mango mango kiwi"
    assert wordfreq.top_words(text, 10) == [
        ("apple", 2),
        ("mango", 2),
        ("kiwi", 1),
        ("pear", 1),
    ]


def test_n_zero_returns_empty():
    assert wordfreq.top_words("a b a", 0) == []


def test_n_negative_returns_empty():
    assert wordfreq.top_words("a b a", -3) == []


def test_n_exceeds_distinct_words_returns_all():
    text = "one two one"
    assert wordfreq.top_words(text, 99) == [("one", 2), ("two", 1)]


def test_empty_text_returns_empty():
    assert wordfreq.top_words("", 5) == []
    assert wordfreq.top_words("   \n\t,!? ", 5) == []
