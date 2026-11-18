from legacy_stringkit import count_vowels


def test_count_vowels_mixed_case():
    """大小写混合输入回归测试：大写元音也计入。"""
    assert count_vowels("AEIOU") == 5
    assert count_vowels("Apple") == 2
