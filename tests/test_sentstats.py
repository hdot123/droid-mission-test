"""Tests for sentstats: count_sentences and average_sentence_length."""

import sentstats


# --- count_sentences ---

def test_count_sentences_example_one():
    assert sentstats.count_sentences("Hello world. How are you? Fine!") == 3


def test_count_sentences_consecutive_terminal_punctuation_one_separator():
    # "..." is one separator, "?!" is one separator
    assert sentstats.count_sentences("Wait... really?! Yes.") == 3


def test_count_sentences_empty_fragments_not_counted():
    # Leading/trailing separators produce empty fragments, not sentences.
    assert sentstats.count_sentences("Hello world.") == 1
    assert sentstats.count_sentences(". . .") == 0
    assert sentstats.count_sentences("") == 0


def test_count_sentences_no_terminal_punctuation():
    assert sentstats.count_sentences("just some text") == 1
    assert sentstats.count_sentences("one two three") == 1


def test_count_sentences_whitespace_only_between_separators():
    # Only whitespace between separators -> empty fragments, not counted.
    assert sentstats.count_sentences("Hi!   ?!  .") == 1


# --- average_sentence_length ---

def test_average_sentence_length_example():
    result = sentstats.average_sentence_length("One two. Three.")
    assert result == 1.5
    assert isinstance(result, float)


def test_average_sentence_length_no_sentences_returns_float_zero():
    result = sentstats.average_sentence_length("")
    assert result == 0.0
    assert isinstance(result, float)


def test_average_sentence_length_separators_only_returns_zero():
    result = sentstats.average_sentence_length("...?!.")
    assert result == 0.0
    assert isinstance(result, float)


def test_average_sentence_length_counts_words_per_sentence():
    # 3 words in sentence 1, 1 word in sentence 2 -> 2.0
    assert sentstats.average_sentence_length("a b c. d.") == 2.0


def test_average_sentence_length_is_float_even_when_integral():
    result = sentstats.average_sentence_length("One two. Three four.")
    assert result == 2.0
    assert isinstance(result, float)


def test_average_sentence_length_handles_consecutive_punctuation():
    # "Wait... really?! Yes." -> 3 sentences, words 1 + 1 + 1 = 3 -> 1.0
    result = sentstats.average_sentence_length("Wait... really?! Yes.")
    assert result == 1.0
    assert isinstance(result, float)
