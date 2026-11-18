from legacy_stringkit import count_vowels, first_word, last_word, shout


def test_shout():
    assert shout("hello") == "HELLO!"
    assert shout("Hey") == "HEY!"


def test_count_vowels():
    assert count_vowels("banana") == 3
    assert count_vowels("hello world") == 3
    assert count_vowels("rhythm") == 0
    assert count_vowels("") == 0


def test_first_word():
    assert first_word("the quick fox") == "the"
    assert first_word("  padded text ") == "padded"
    assert first_word("") == ""
    assert first_word("   ") == ""


def test_last_word():
    assert last_word("the quick fox") == "fox"
    assert last_word("trailing space ") == "space"
    assert last_word("") == ""
    assert last_word("   ") == ""
