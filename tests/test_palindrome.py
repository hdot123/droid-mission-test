from palindrome import is_palindrome


def test_required_example_panama():
    assert is_palindrome("A man, a plan, a canal: Panama") is True


def test_required_example_hello():
    assert is_palindrome("hello") is False


def test_case_insensitive():
    assert is_palindrome("RaceCar") is True


def test_digits_palindrome():
    assert is_palindrome("12321") is True


def test_digits_non_palindrome():
    assert is_palindrome("123") is False


def test_empty_string():
    assert is_palindrome("") is True


def test_only_non_alphanumeric():
    assert is_palindrome("!!!...") is True
    assert is_palindrome(" ,  ") is True


def test_non_palindrome_with_punctuation():
    assert is_palindrome("Hello, world!") is False
