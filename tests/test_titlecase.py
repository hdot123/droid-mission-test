"""Tests for titlecase.title_case — round-55 acceptance examples, verbatim."""

import pytest

from titlecase import title_case


def test_empty_string():
    assert title_case("") == ""


def test_hello_world():
    assert title_case("hello world") == "Hello World"


def test_small_words_middle_and_edges():
    assert title_case("the lord of the rings") == "The Lord of the Rings"


def test_a_tale_of_two_cities():
    assert title_case("a tale of two cities") == "A Tale of Two Cities"


def test_war_and_peace_uppercase_input():
    assert title_case("WAR AND PEACE") == "War and Peace"


def test_the_old_man_and_the_sea():
    assert title_case("the old man and the sea") == "The Old Man and the Sea"


def test_to_be_or_not_to_be():
    assert title_case("to be or not to be") == "To Be or Not to Be"


def test_mother_in_law():
    assert title_case("mother-in-law") == "Mother-in-Law"


def test_the_mother_in_law():
    assert title_case("the mother-in-law") == "The Mother-in-Law"


def test_jack_of_all_trades():
    assert title_case("jack-of-all-trades") == "Jack-of-All-Trades"


def test_apostrophe_word():
    assert title_case("don't look back") == "Don't Look Back"


def test_leading_symbols_preserved():
    assert title_case("(the) end") == "(The) End"


def test_abbreviations_lowered():
    assert title_case("NASA and ESA") == "Nasa and Esa"


def test_whitespace_normalization():
    assert title_case("  spaced   out  ") == "Spaced Out"


def test_what_to_look_for():
    assert title_case("what to look for") == "What to Look For"


def test_in_the_two_words():
    assert title_case("in the") == "In The"


def test_single_word():
    assert title_case("the") == "The"


def test_leading_digits():
    assert title_case("123 go") == "123 Go"


def test_hyphenated_small_word_segment():
    assert title_case("e-mail etiquette") == "E-Mail Etiquette"


def test_non_str_raises_type_error():
    with pytest.raises(TypeError):
        title_case(None)
