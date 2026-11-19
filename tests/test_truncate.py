import pytest

from truncate import truncate


def test_longer_than_max_len_returns_input_unchanged():
    assert truncate("hello world", 11) == "hello world"
    assert truncate("hello world", 20) == "hello world"


def test_truncates_on_word_boundary_when_possible():
    assert truncate("hello world", 8) == "hello…"
    assert truncate("hello world", 5) == "hell…"
    assert truncate("hello world", 9, "...") == "hello..."
    assert truncate("hello world", 10) == "hello…"


def test_hard_cut_when_no_space_in_head():
    assert truncate("helloworld", 8) == "hellowo…"


def test_word_boundary_with_trailing_space_in_head():
    assert truncate("a b c d e", 5) == "a b…"


def test_empty_and_fitting_text():
    assert truncate("", 5) == ""
    assert truncate("hi", 2) == "hi"


def test_max_len_equal_to_ellipsis_length():
    assert truncate("hello", 1) == "…"


def test_leading_space_keeps_hard_cut_when_candidate_empty():
    assert truncate(" hello world", 6) == " hell…"


def test_value_error_when_max_len_below_ellipsis_length():
    with pytest.raises(ValueError):
        truncate("hello", 0)
    with pytest.raises(ValueError):
        truncate("hello", 2, "...")


def test_type_error_on_invalid_argument_types():
    with pytest.raises(TypeError):
        truncate(123, 5)
    with pytest.raises(TypeError):
        truncate("hello", 5.0)
    with pytest.raises(TypeError):
        truncate("hello", 5, None)


def test_type_error_on_bool_max_len():
    with pytest.raises(TypeError):
        truncate("hello", True)


def test_result_length_always_at_most_max_len():
    cases = [
        ("hello world", 8, "…"),
        ("hello world", 5, "…"),
        ("helloworld", 8, "…"),
        ("a b c d e", 5, "…"),
        (" hello world", 6, "…"),
        ("hello world", 9, "..."),
        ("hello", 1, "…"),
    ]
    for text, max_len, ellipsis in cases:
        result = truncate(text, max_len, ellipsis)
        assert len(result) <= max_len
