"""Tests for the anagram module."""

import anagram


def test_are_anagrams_examples():
    assert anagram.are_anagrams("Dormitory", "dirty room") is True
    assert anagram.are_anagrams("hello", "world") is False


def test_are_anagrams_ignores_case_and_punctuation():
    assert anagram.are_anagrams("A gentleman", "Elegant man!") is True
    assert anagram.are_anagrams("Bob", "Bo b?") is True


def test_are_anagrams_single_letter():
    assert anagram.are_anagrams("a", "a") is True
    assert anagram.are_anagrams("a", "b") is False


def test_are_anagrams_empty_string():
    assert anagram.are_anagrams("", "") is True
    assert anagram.are_anagrams("", "abc") is False


def test_group_example():
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]
    assert anagram.group(words) == [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]


def test_group_single_word():
    assert anagram.group(["hello"]) == [["hello"]]


def test_group_empty_list():
    assert anagram.group([]) == []


def test_group_preserves_input_order_within_groups():
    words = ["b a", "ab!", "z", "c", "b,a"]
    assert anagram.group(words) == [["b a", "ab!", "b,a"], ["z"], ["c"]]
