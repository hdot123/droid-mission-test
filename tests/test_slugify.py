from slugify import slugify


def test_basic_punctuation_and_space():
    assert slugify("Hello, World! 2026") == "hello-world-2026"


def test_leading_trailing_and_repeated_hyphens():
    assert slugify("--A  b--") == "a-b"


def test_empty_string():
    assert slugify("") == ""


def test_only_special_characters():
    assert slugify("!!!") == ""


def test_already_a_slug_is_idempotent():
    assert slugify("hello-world-2026") == "hello-world-2026"


def test_case_folding_of_letters_and_digits_kept():
    assert slugify("AbC123") == "abc123"
