"""Tests for sentence_stats (sentence-level statistics only).

These tests exercise only sentence_stats.py's behavior, per this
process card; no other toolkit module is imported or tested here.
"""

import pytest

import sentence_stats as ss


class TestSplitSentences:
    def test_empty_input_returns_empty_list(self):
        assert ss.split_sentences("") == []

    def test_whitespace_only_returns_empty_list(self):
        assert ss.split_sentences("   \n\t  ") == []

    def test_single_sentence_with_terminator(self):
        assert ss.split_sentences("Hello world.") == ["Hello world."]

    def test_multiple_sentence_terminators(self):
        assert ss.split_sentences("One. Two! Three?") == ["One.", "Two!", "Three?"]

    def test_text_without_terminator_is_one_sentence(self):
        assert ss.split_sentences("no terminator here") == ["no terminator here"]

    def test_whitespace_around_sentences_is_stripped(self):
        text = "  First sentence.   \n  Second sentence!  "
        assert ss.split_sentences(text) == ["First sentence.", "Second sentence!"]

    def test_consecutive_terminators_form_one_boundary(self):
        assert ss.split_sentences("Really?! Yes.") == ["Really?!", "Yes."]

    def test_newline_inside_sentence_does_not_split(self):
        text = "A single sentence\nspanning two lines."
        assert ss.split_sentences(text) == ["A single sentence\nspanning two lines."]

    def test_decimal_point_does_not_split(self):
        assert ss.split_sentences("Pi is roughly 3.14159.") == [
            "Pi is roughly 3.14159."
        ]

    def test_non_string_input_raises_type_error(self):
        with pytest.raises(TypeError):
            ss.split_sentences(None)


class TestCountSentences:
    def test_empty_is_zero(self):
        assert ss.count_sentences("") == 0

    def test_single_sentence(self):
        assert ss.count_sentences("Just one.") == 1

    def test_three_sentences_mixed_terminators(self):
        assert ss.count_sentences("One. Two! Three?") == 3

    def test_matches_split_sentences_length(self):
        text = "Alpha. Beta! Gamma? Delta."
        assert ss.count_sentences(text) == len(ss.split_sentences(text))

    def test_text_without_terminator_counts_one(self):
        assert ss.count_sentences("a b c") == 1


class TestSentenceLengths:
    def test_empty_returns_empty_list(self):
        assert ss.sentence_lengths("") == []

    def test_word_count_per_sentence(self):
        assert ss.sentence_lengths("Hello world. Bye now.") == [2, 2]

    def test_lengths_align_with_split_sentences(self):
        text = "One two. Three!"
        assert ss.sentence_lengths(text) == [
            len(sentence.split()) for sentence in ss.split_sentences(text)
        ]


class TestAverageSentenceLength:
    def test_empty_returns_zero(self):
        assert ss.average_sentence_length("") == 0.0

    def test_average_of_two_sentences(self):
        assert ss.average_sentence_length("Hello world. Bye now.") == 2.0

    def test_single_sentence_without_terminator(self):
        assert ss.average_sentence_length("one two three four") == 4.0

    def test_partial_word_counts_average(self):
        # Sentence lengths [1, 2] -> mean 1.5.
        assert ss.average_sentence_length("One. Two two!") == 1.5


class TestSentenceLengthSummary:
    def test_empty_summary_is_all_zero(self):
        assert ss.sentence_length_summary("") == {
            "sentence_count": 0,
            "word_count": 0,
            "average_sentence_length": 0.0,
            "min_sentence_length": 0,
            "max_sentence_length": 0,
        }

    def test_summary_values(self):
        summary = ss.sentence_length_summary("One. Two two!")
        assert summary["sentence_count"] == 2
        assert summary["word_count"] == 3
        assert summary["average_sentence_length"] == 1.5
        assert summary["min_sentence_length"] == 1
        assert summary["max_sentence_length"] == 2

    def test_summary_has_exactly_documented_keys(self):
        summary = ss.sentence_length_summary("Hi.")
        assert set(summary) == {
            "sentence_count",
            "word_count",
            "average_sentence_length",
            "min_sentence_length",
            "max_sentence_length",
        }
