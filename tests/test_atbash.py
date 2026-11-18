from atbash import atbash


def test_hello():
    assert atbash("Hello") == "Svool"


def test_mixed_case_letters():
    assert atbash("abcXYZ") == "zyxCBA"


def test_punctuation_and_spaces_preserved():
    assert atbash("Hello, World!") == "Svool, Dliow!"


def test_empty_string():
    assert atbash("") == ""


def test_digits_unchanged():
    assert atbash("123") == "123"


def test_roundtrip_identity():
    text = "Hello, World! 123"
    assert atbash(atbash(text)) == text
    assert atbash(text) == "Svool, Dliow! 123"


def test_case_preserved_for_single_letters():
    assert atbash("a") == "z"
    assert atbash("z") == "a"
    assert atbash("A") == "Z"
    assert atbash("Z") == "A"


def test_non_letter_characters_unchanged():
    assert atbash(" \t\n,!?") == " \t\n,!?"
