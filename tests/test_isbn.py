"""Tests for isbn.py — ISBN-10 validation."""

import unittest

from isbn import is_valid_isbn10


class TestValidIsbn10(unittest.TestCase):
    def test_valid_simple(self):
        self.assertTrue(is_valid_isbn10("0306406152"))

    def test_valid_with_hyphens_and_spaces(self):
        self.assertTrue(is_valid_isbn10("0-306-40615-2"))
        self.assertTrue(is_valid_isbn10("0 306 40615 2"))

    def test_valid_ending_in_x(self):
        # Weighted sum with check value 10: 047195862X is a valid code.
        self.assertTrue(is_valid_isbn10("047195862X"))

    def test_valid_known_examples(self):
        self.assertTrue(is_valid_isbn10("0471958697"))


class TestInvalidCheckDigit(unittest.TestCase):
    def test_wrong_check_digit(self):
        self.assertFalse(is_valid_isbn10("0306406153"))

    def test_wrong_check_digit_with_hyphens(self):
        self.assertFalse(is_valid_isbn10("0-306-40615-3"))

    def test_sum_not_divisible_by_11(self):
        self.assertFalse(is_valid_isbn10("0000000001"))


class TestXPlacement(unittest.TestCase):
    def test_x_in_middle_is_invalid(self):
        self.assertFalse(is_valid_isbn10("03X6406152"))

    def test_x_as_first_char_is_invalid(self):
        self.assertFalse(is_valid_isbn10("X306406152"))

    def test_x_twice_is_invalid(self):
        self.assertFalse(is_valid_isbn10("03064061XX"))


class TestBadLengthAndCharset(unittest.TestCase):
    def test_too_short(self):
        self.assertFalse(is_valid_isbn10("030640615"))

    def test_too_long(self):
        self.assertFalse(is_valid_isbn10("03064061523"))

    def test_empty_string(self):
        self.assertFalse(is_valid_isbn10(""))

    def test_illegal_characters(self):
        self.assertFalse(is_valid_isbn10("030640615A"))
        self.assertFalse(is_valid_isbn10("ABCDEFGHIJ"))


if __name__ == "__main__":
    unittest.main()
