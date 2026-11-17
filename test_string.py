"""Pytest checks for string.py."""

from string import count_vowels, reverse_words, title_case


# --- Work order examples (must hold exactly) ---


def test_reverse_words_example():
    assert reverse_words("the quick fox") == "fox quick the"


def test_count_vowels_example():
    assert count_vowels("Abacus") == 3


def test_title_case_example():
    assert title_case("hELLO wORLD") == "Hello World"


# --- reverse_words extras ---


def test_reverse_words_extra_spaces():
    assert reverse_words("  the   quick   fox  ") == "fox quick the"


def test_reverse_words_empty():
    assert reverse_words("") == ""


def test_reverse_words_single_word():
    assert reverse_words("hello") == "hello"


def test_reverse_words_tabs_newlines():
    assert reverse_words("a\tb\nc") == "c b a"


# --- count_vowels extras ---


def test_count_vowels_uppercase():
    assert count_vowels("AEIOU") == 5


def test_count_vowels_empty():
    assert count_vowels("") == 0


def test_count_vowels_all_consonants():
    assert count_vowels("rhythm") == 0


def test_count_vowels_mixed_case():
    assert count_vowels("AbAcUs") == 3


# --- title_case extras ---


def test_title_case_empty():
    assert title_case("") == ""


def test_title_case_extra_spaces():
    assert title_case("  hELLO   wORLD  ") == "Hello World"


def test_title_case_all_consonants():
    assert title_case("rhythm") == "Rhythm"


def test_title_case_single_word():
    assert title_case("hELLO") == "Hello"


def test_title_case_leading_upper_rest():
    assert title_case("McDONALD") == "Mcdonald"
