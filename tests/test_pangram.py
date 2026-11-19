"""tests for pangram: 全字母句判定与缺失字母（第 46 轮 B）。"""

import pytest

from pangram import is_pangram, missing_letters

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


class TestIsPangram:
    def test_quick_brown_fox(self):
        assert is_pangram("The quick brown fox jumps over the lazy dog") is True

    def test_pack_my_box(self):
        assert is_pangram("Pack my box with five dozen liquor jugs") is True

    def test_hello_world_not_pangram(self):
        assert is_pangram("hello world") is False

    def test_empty_string(self):
        assert is_pangram("") is False

    def test_uppercase_alphabet(self):
        assert is_pangram("ABCDEFGHIJKLMNOPQRSTUVWXYZ") is True

    def test_sphinx(self):
        assert is_pangram("Sphinx of black quartz, judge my vow") is True

    def test_all_uppercase_sentence(self):
        assert is_pangram("THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG") is True

    def test_rejects_non_str(self):
        with pytest.raises(TypeError):
            is_pangram(123)


class TestMissingLetters:
    def test_quick_brown_fox(self):
        assert missing_letters("The quick brown fox jumps over the lazy dog") == []

    def test_hello_world(self):
        assert missing_letters("hello world") == [
            "a", "b", "c", "f", "g", "i", "j", "k", "m", "n",
            "p", "q", "s", "t", "u", "v", "x", "y", "z",
        ]

    def test_empty_string_full_alphabet(self):
        assert missing_letters("") == list(ALPHABET)

    def test_uppercase_alphabet(self):
        assert missing_letters("ABCDEFGHIJKLMNOPQRSTUVWXYZ") == []

    def test_mixed_case_abc(self):
        expected = [ch for ch in ALPHABET if ch not in "abc"]
        assert missing_letters("aAbBcC") == expected
        assert len(expected) == 23

    def test_rejects_non_str(self):
        with pytest.raises(TypeError):
            missing_letters(None)
