"""Tests for wordfreq: count_words and top_words."""

import wordfreq


def test_count_words_spec_example():
    assert wordfreq.count_words("The cat, the CAT.") == {"the": 2, "cat": 2}


def test_count_words_empty_string():
    assert wordfreq.count_words("") == {}


def test_count_words_lowercases():
    assert wordfreq.count_words("Hello hello HELLO") == {"hello": 3}


def test_count_words_splits_on_any_whitespace():
    assert wordfreq.count_words("a\tb\nc  d") == {"a": 1, "b": 1, "c": 1, "d": 1}


def test_count_words_strips_all_listed_punctuation():
    # Leading and trailing punctuation .,;:!?"'() is stripped.
    text = '...Hello... (World)! "Yes"; it\'s: ok, sure? (end.)'
    result = wordfreq.count_words(text)
    assert "hello" in result
    assert "world" in result
    assert "yes" in result
    assert "it's" in result
    assert "ok" in result
    assert "sure" in result
    assert "end" in result


def test_count_words_punctuation_only_token_discarded():
    assert wordfreq.count_words("... !!! (()) ") == {}
    assert wordfreq.count_words("a !!! b") == {"a": 1, "b": 1}


def test_count_words_interior_punctuation_kept():
    assert wordfreq.count_words("can't") == {"can't": 1}


def test_top_words_spec_example():
    assert wordfreq.top_words("b a b c a b", 2) == [("b", 3), ("a", 2)]


def test_top_words_tie_broken_alphabetically():
    # Same count -> alphabetical ascending: a before b before c.
    assert wordfreq.top_words("c b a b c a", 3) == [("a", 2), ("b", 2), ("c", 2)]


def test_top_words_n_less_than_one_returns_empty():
    assert wordfreq.top_words("a b c", 0) == []
    assert wordfreq.top_words("a b c", -1) == []


def test_top_words_n_larger_than_unique_words():
    assert wordfreq.top_words("b a b", 10) == [("b", 2), ("a", 1)]


def test_top_words_n_one():
    assert wordfreq.top_words("x y x z x", 1) == [("x", 3)]


def test_top_words_empty_text():
    assert wordfreq.top_words("", 3) == []
