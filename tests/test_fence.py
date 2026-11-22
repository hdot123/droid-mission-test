"""Tests for the fence module: wrap() and unwrap()."""

import pytest

import fence


def test_wrap_respects_width():
    assert fence.wrap("the quick brown fox", 11) == "the quick\nbrown fox"


def test_wrap_lines_never_exceed_width_for_normal_words():
    text = "alpha beta gamma delta epsilon zeta"
    width = 7
    lines = fence.wrap(text, width).split("\n")
    assert all(len(line) <= width for line in lines)
    assert " ".join(lines) == text


def test_wrap_long_word_on_own_line_untruncated():
    long_word = "supercalifragilisticexpialidocious"
    result = fence.wrap("a " + long_word + " b", 5)
    lines = result.split("\n")
    assert lines[0] == "a"
    assert lines[1] == long_word
    assert lines[2] == "b"
    assert len(lines[1]) > 5


def test_wrap_treats_whitespace_runs_as_separators():
    assert fence.wrap("  a\t b\n\n c  ", 10) == "a b c"


def test_wrap_empty_and_whitespace_only_text():
    assert fence.wrap("", 10) == ""
    assert fence.wrap("   \n\t ", 10) == ""


def test_wrap_unwrap_round_trip():
    text = "the quick brown fox jumps over the lazy dog"
    wrapped = fence.wrap(text, 10)
    assert fence.unwrap(wrapped) == text


def test_unwrap_keeps_trailing_hyphen():
    assert fence.unwrap("a well-\nknown fact") == "a well- known fact"


def test_unwrap_normalizes_blank_lines_and_whitespace():
    assert fence.unwrap("one\n\n  two\n\n\nthree   ") == "one two three"


def test_unwrap_single_line_unchanged():
    assert fence.unwrap("already one line") == "already one line"


@pytest.mark.parametrize("width", [0, -1, -5])
def test_wrap_non_positive_width_raises_value_error(width):
    with pytest.raises(ValueError):
        fence.wrap("a", width)


def test_wrap_none_text_raises_type_error():
    with pytest.raises(TypeError):
        fence.wrap(None, 10)


def test_wrap_none_width_raises_type_error():
    with pytest.raises(TypeError):
        fence.wrap("a", None)


def test_unwrap_none_raises_type_error():
    with pytest.raises(TypeError):
        fence.unwrap(None)
