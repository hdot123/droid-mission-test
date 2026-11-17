"""Tests for piglatin.translate and piglatin.translate_sentence."""

from piglatin import translate, translate_sentence


def test_vowel_start_examples():
    assert translate("apple") == "appleway"


def test_consonant_start_examples():
    assert translate("string") == "ingstray"
    assert translate("cat") == "atcay"


def test_empty_string():
    assert translate("") == ""


def test_sentence_example():
    assert translate_sentence("hello world") == "ellohay orldway"


def test_vowel_start_words():
    assert translate("elephant") == "elephantway"
    assert translate("orange") == "orangeway"
    assert translate("igloo") == "iglooway"


def test_consonant_cluster_moves_entirely():
    assert translate("strong") == "ongstray"
    assert translate("chair") == "airchay"
    assert translate("three") == "eethray"
    assert translate("rhythm") == "rhythmay"


def test_mixed_case_input_lowercased_output():
    assert translate("Apple") == "appleway"
    assert translate("String") == "ingstray"
    assert translate("CAT") == "atcay"
    assert translate("HeLLo") == "ellohay"


def test_single_letter_words():
    assert translate("a") == "away"
    assert translate("b") == "bay"


def test_empty_sentence():
    assert translate_sentence("") == ""


def test_sentence_single_word():
    assert translate_sentence("cat") == "atcay"
