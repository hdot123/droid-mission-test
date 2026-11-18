"""Tests for anagram module."""

import anagram


def test_is_anagram_listen_silent():
    assert anagram.is_anagram("Listen", "Silent") is True


def test_is_anagram_dormitory_dirty_room():
    assert anagram.is_anagram("Dormitory", "Dirty room") is True


def test_is_anagram_hello_world():
    assert anagram.is_anagram("hello", "world") is False


def test_group_anagrams_example():
    assert anagram.group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]) == [
        ["eat", "tea", "ate"],
        ["tan", "nat"],
        ["bat"],
    ]


def test_is_anagram_ignores_punctuation_and_case():
    assert anagram.is_anagram("Debit card", "Bad credit!") is True


def test_is_anagram_counts_matter():
    assert anagram.is_anagram("aab", "abb") is False


def test_group_anagrams_preserves_order_and_first_appearance():
    assert anagram.group_anagrams(["bat", "tan", "eat", "nat", "tea"]) == [
        ["bat"],
        ["tan", "nat"],
        ["eat", "tea"],
    ]


def test_group_anagrams_empty_list():
    assert anagram.group_anagrams([]) == []
