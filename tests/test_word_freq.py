"""Tests for the word_freq module (word-frequency statistics).

Only word_freq.py is exercised here; no other modules are imported.
"""

import pytest

import word_freq
from word_freq import (
    count_words,
    tokenize,
    top_words,
    unique_word_count,
    word_count,
)


class TestTokenize:
    def test_basic_split(self):
        assert tokenize("Hello, hello world!") == ["Hello", "hello", "world"]

    def test_preserves_case(self):
        assert tokenize("The THE the") == ["The", "THE", "the"]

    def test_empty_and_no_words(self):
        assert tokenize("") == []
        assert tokenize("... !!! \n\t") == []

    def test_apostrophes_and_hyphens(self):
        assert tokenize("don't state-of-the-art") == ["don't", "state-of-the-art"]

    def test_punctuation_is_separator(self):
        assert tokenize("one,two;three") == ["one", "two", "three"]

    def test_rejects_non_str(self):
        with pytest.raises(TypeError):
            tokenize(None)


class TestCountWords:
    def test_counts_case_insensitively(self):
        assert count_words("A cat, a hat.") == {"a": 2, "cat": 1, "hat": 1}

    def test_repeated_words(self):
        assert count_words("to be or not to be") == {"to": 2, "be": 2, "or": 1, "not": 1}

    def test_empty_text(self):
        assert count_words("") == {}

    def test_returns_dict(self):
        assert isinstance(count_words("x y x"), dict)


class TestTopWords:
    def test_orders_by_descending_count(self):
        assert top_words("a b b c c c", 2) == [("c", 3), ("b", 2)]

    def test_ties_broken_alphabetically(self):
        assert top_words("b a a c c") == [("a", 2), ("c", 2), ("b", 1)]

    def test_n_larger_than_distinct_returns_all(self):
        assert top_words("x y", 10) == [("x", 1), ("y", 1)]

    def test_non_positive_n_returns_empty(self):
        assert top_words("a b", 0) == []
        assert top_words("a b", -3) == []

    def test_empty_text_returns_empty(self):
        assert top_words("", 5) == []

    def test_rejects_non_int_n(self):
        with pytest.raises(TypeError):
            top_words("a b", "2")


class TestWordCount:
    def test_counts_repeated_words(self):
        assert word_count("one two two") == 3

    def test_empty_text(self):
        assert word_count("") == 0

    def test_matches_tokenize_length(self):
        text = "The quick, brown fox!"
        assert word_count(text) == len(tokenize(text))


class TestUniqueWordCount:
    def test_case_insensitive_distinct(self):
        assert unique_word_count("The the THE") == 1

    def test_empty_text(self):
        assert unique_word_count("") == 0

    def test_matches_count_words_size(self):
        text = "a A b B c"
        assert unique_word_count(text) == len(count_words(text))


def test_module_exports_expected_functions():
    for name in ("tokenize", "count_words", "top_words", "word_count",
                 "unique_word_count"):
        assert hasattr(word_freq, name)
        assert callable(getattr(word_freq, name))
