"""Tests for wrapwidth.wrap and wrapwidth.justify."""

import pytest

import wrapwidth
from wrapwidth import justify, wrap


# --- wrap: worked examples ---

def test_wrap_example_brown_fox():
    assert wrap("the quick brown fox", 10) == ["the quick", "brown fox"]


def test_wrap_example_overlong_word():
    assert wrap("a supercalifragilistic word", 10) == [
        "a",
        "supercalifragilistic",
        "word",
    ]


# --- wrap: edge cases ---

def test_wrap_empty_text():
    assert wrap("", 5) == []


def test_wrap_whitespace_only_text():
    assert wrap("   \t\n  ", 5) == []


def test_wrap_overlong_single_word_unbroken():
    # A single word longer than width occupies its own line, unbroken,
    # and that line may exceed width.
    assert wrap("supercalifragilistic", 3) == ["supercalifragilistic"]


def test_wrap_multiple_whitespace_splits_words():
    # "a b c" is exactly 5 chars, so all three words fit on one line.
    assert wrap("  a\t b\n  c  ", 5) == ["a b c"]


def test_wrap_word_exactly_width():
    assert wrap("abcd", 4) == ["abcd"]


def test_wrap_words_fit_exactly_on_line():
    assert wrap("ab cd", 5) == ["ab cd"]


def test_wrap_greedy_packing():
    assert wrap("aa bb cc dd", 5) == ["aa bb", "cc dd"]


def test_wrap_long_word_in_the_middle():
    assert wrap("a toolongword b", 4) == ["a", "toolongword", "b"]


# --- wrap: width validation ---

@pytest.mark.parametrize("bad_width", [0, -1, -10, 2.5, 0.0, "10", None, True])
def test_wrap_invalid_width_raises(bad_width):
    with pytest.raises(ValueError):
        wrap("some text", bad_width)


def test_wrap_invalid_width_raises_on_empty_text():
    with pytest.raises(ValueError):
        wrap("", 0)


# --- justify: worked examples ---

def test_justify_example_the_quick():
    assert justify("the quick", 10) == "the  quick"


def test_justify_example_a_b_c():
    assert justify("a b c", 8) == "a   b  c"


def test_justify_example_aa_bb_cc():
    assert justify("aa bb cc", 12) == "aa   bb   cc"


# --- justify: edge cases ---

def test_justify_line_already_long_enough_unchanged():
    assert justify("the quick brown fox", 10) == "the quick brown fox"


def test_justify_line_exactly_width_unchanged():
    assert justify("abcd ef", 7) == "abcd ef"


def test_justify_single_word_unchanged():
    assert justify("hello", 20) == "hello"


def test_justify_single_word_already_long_unchanged():
    assert justify("a" * 30, 5) == "a" * 30


def test_justify_remainder_distribution_left_to_right():
    # "a b c" is 5 chars; width 8 -> 3 extra spaces over 2 gaps:
    # base 1 each, remainder 1 -> first gap gets one more.
    assert justify("a b c", 8) == "a   b  c"


def test_justify_no_remainder_even_split():
    # "aa bb" is 5 chars with 1 gap; width 9 -> 4 extra in that single gap:
    # base 4, remainder 0 -> 1 original + 4 = 5 spaces total.
    assert justify("aa bb", 9) == "aa     bb"
    assert len(justify("aa bb", 9)) == 9


def test_justify_output_length_matches_width():
    line = "the quick"
    result = justify(line, 10)
    assert len(result) == 10


# --- justify: width validation ---

@pytest.mark.parametrize("bad_width", [0, -1, -10, 2.5, 0.0, "10", None, True])
def test_justify_invalid_width_raises(bad_width):
    with pytest.raises(ValueError):
        justify("the quick", bad_width)


def test_justify_invalid_width_raises_on_single_word():
    with pytest.raises(ValueError):
        justify("hello", 0)


# --- round trip / module surface ---

def test_module_exposes_both_functions():
    assert hasattr(wrapwidth, "wrap")
    assert hasattr(wrapwidth, "justify")


def test_wrap_then_justify_round_length():
    lines = wrap("the quick brown fox jumps over the lazy dog", 10)
    for ln in lines:
        if len(ln.split(" ")) > 1:
            # Multi-word lines justify to exactly the target width;
            # single-word lines are returned unchanged per spec.
            assert len(justify(ln, 12)) == 12
        else:
            assert justify(ln, 12) == ln
