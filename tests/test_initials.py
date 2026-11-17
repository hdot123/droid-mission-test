"""Tests for the initials module only."""

import unittest

from initials import initials


class TestInitials(unittest.TestCase):
    def test_two_words(self):
        self.assertEqual(initials("Ada Lovelace"), "A.L.")

    def test_extra_spaces_and_lowercase(self):
        self.assertEqual(initials("  grace   hopper "), "G.H.")

    def test_single_word(self):
        self.assertEqual(initials("Prince"), "P.")

    def test_multiple_words(self):
        self.assertEqual(initials("Alan Turing"), "A.T.")

    def test_empty_string(self):
        self.assertEqual(initials(""), "")


if __name__ == "__main__":
    unittest.main()
