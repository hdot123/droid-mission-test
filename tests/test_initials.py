from legacy_stringkit import initials


def test_initials_full_name():
    assert initials("john ronald reuel tolkien") == "JRRT"


def test_initials_two_words():
    assert initials("ada lovelace") == "AL"


def test_initials_empty():
    assert initials("") == ""
