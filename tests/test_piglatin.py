"""Tests for piglatin.py only."""

import unittest

from piglatin import translate


class TestTranslate(unittest.TestCase):
    # Spec examples (must match verbatim)
    def test_example_apple(self):
        self.assertEqual(translate("apple"), "appleway")

    def test_example_banana(self):
        self.assertEqual(translate("banana"), "ananabay")

    def test_example_string(self):
        self.assertEqual(translate("string"), "ingstray")

    # Vowel-initial words
    def test_vowel_initial(self):
        self.assertEqual(translate("egg"), "eggway")
        self.assertEqual(translate("orange"), "orangeway")
        self.assertEqual(translate("a"), "away")

    # Consonant-initial words
    def test_consonant_initial(self):
        self.assertEqual(translate("cat"), "atcay")
        self.assertEqual(translate("chair"), "airchay")
        self.assertEqual(translate("school"), "oolschay")

    # Case-shape preservation
    def test_all_lowercase_stays_lowercase(self):
        self.assertEqual(translate("apple"), "appleway")
        self.assertEqual(translate("banana"), "ananabay")

    def test_capitalized_stays_capitalized(self):
        self.assertEqual(translate("Apple"), "Appleway")
        self.assertEqual(translate("Banana"), "Ananabay")
        self.assertEqual(translate("String"), "Ingstray")

    def test_single_letter_vowel(self):
        self.assertEqual(translate("I"), "Iway")

    # Invalid input raises ValueError
    def test_invalid_input_raises(self):
        with self.assertRaises(ValueError):
            translate("")
        with self.assertRaises(ValueError):
            translate(123)
        with self.assertRaises(ValueError):
            translate("123")
        with self.assertRaises(ValueError):
            translate("hi!")


if __name__ == "__main__":
    unittest.main()
