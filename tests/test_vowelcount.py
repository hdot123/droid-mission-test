from vowelcount import count


def test_banana_example():
    assert count("banana") == 3


def test_sky_example():
    assert count("sky") == 0


def test_mixed_case_example():
    assert count("AeIoU") == 5


def test_uppercase_is_case_insensitive():
    assert count("BANANA") == 3


def test_empty_string():
    assert count("") == 0


def test_non_vowels_ignored():
    assert count("xyz123!") == 0
