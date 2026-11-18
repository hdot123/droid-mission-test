"""isbn13 模块测试：覆盖工单全部验收要点与典型非法输入。"""

import unittest

import isbn13


class TestCheckDigit(unittest.TestCase):
    def test_known_prefix(self):
        self.assertEqual(isbn13.check_digit("978030640615"), 7)

    def test_wrong_length_11_digits(self):
        with self.assertRaises(ValueError):
            isbn13.check_digit("97803064061")

    def test_wrong_length_13_digits(self):
        with self.assertRaises(ValueError):
            isbn13.check_digit("9780306406157")

    def test_empty_string(self):
        with self.assertRaises(ValueError):
            isbn13.check_digit("")

    def test_non_digit_characters(self):
        with self.assertRaises(ValueError):
            isbn13.check_digit("97803064061x")
        with self.assertRaises(ValueError):
            isbn13.check_digit("978-03064061")

    def test_non_string_input(self):
        with self.assertRaises(ValueError):
            isbn13.check_digit(None)


class TestIsValid(unittest.TestCase):
    def test_valid_isbn(self):
        self.assertTrue(isbn13.is_valid("9780306406157"))

    def test_wrong_check_digit(self):
        self.assertFalse(isbn13.is_valid("9780306406158"))

    def test_hyphenated_form(self):
        self.assertFalse(isbn13.is_valid("978-0-306-40615-7"))

    def test_empty_string(self):
        self.assertFalse(isbn13.is_valid(""))

    def test_too_short(self):
        self.assertFalse(isbn13.is_valid("978030640615"))

    def test_too_long(self):
        self.assertFalse(isbn13.is_valid("97803064061570"))

    def test_non_digit_characters(self):
        self.assertFalse(isbn13.is_valid("978030640615x"))

    def test_non_string_input(self):
        self.assertFalse(isbn13.is_valid(None))
        self.assertFalse(isbn13.is_valid(9780306406157))


if __name__ == "__main__":
    unittest.main()
