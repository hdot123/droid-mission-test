import pytest

from levenshtein import distance, is_within


def test_distance_spec_examples():
    assert distance("kitten", "sitting") == 3
    assert distance("", "abc") == 3
    assert distance("abc", "abc") == 0


def test_distance_empty_and_single_char():
    assert distance("", "") == 0
    assert distance("a", "") == 1
    assert distance("", "a") == 1
    assert distance("a", "b") == 1


def test_distance_single_character_edits():
    # One insertion
    assert distance("abc", "abcd") == 1
    assert distance("abcd", "abc") == 1
    # One deletion
    assert distance("abc", "ac") == 1
    # One substitution
    assert distance("abc", "abd") == 1
    # Symmetry
    assert distance("kitten", "sitting") == distance("sitting", "kitten")


def test_distance_classic_examples():
    assert distance("saturday", "sunday") == 3
    assert distance("flaw", "lawn") == 2


def test_is_within_true_and_false():
    assert is_within("kitten", "sitting", 3) is True
    assert is_within("kitten", "sitting", 2) is False
    assert is_within("abc", "abc", 0) is True


def test_is_within_boundary_equal_to_k():
    # distance is exactly 3; k == 3 must pass, k == 2 must fail
    assert distance("kitten", "sitting") == 3
    assert is_within("kitten", "sitting", 3) is True
    assert is_within("kitten", "sitting", 2) is False


def test_is_within_boundary_one_over():
    # k one greater than the distance always passes
    assert is_within("kitten", "sitting", 4) is True
    assert is_within("", "abc", 4) is True
    assert is_within("", "abc", 2) is False


def test_is_within_zero_distance_zero_k():
    assert is_within("same", "same", 0) is True
    assert is_within("same", "diff", 0) is False


def test_is_within_negative_k_raises():
    with pytest.raises(ValueError):
        is_within("a", "b", -1)
    with pytest.raises(ValueError):
        is_within("abc", "abc", -1)
