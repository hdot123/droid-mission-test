from anagram import is_anagram


def test_worked_example_listen_silent():
    assert is_anagram("Listen", "Silent") is True


def test_worked_example_hello_world():
    assert is_anagram("hello", "world") is False


def test_ignores_case():
    assert is_anagram("AbC", "cba") is True


def test_ignores_other_characters():
    assert is_anagram("a-b!c", "cba") is True
    assert is_anagram("dormitory", "dirty room!") is True


def test_two_empty_strings_return_true():
    assert is_anagram("", "") is True


def test_strings_with_no_letters_return_true():
    assert is_anagram("123", "!!!") is True


def test_letter_count_matters():
    assert is_anagram("aa", "a") is False
