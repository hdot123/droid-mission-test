"""Tests for the hamming module."""

import unittest

import hamming


class TestHammingDistance(unittest.TestCase):
    def test_karolin_kathrin(self):
        self.assertEqual(hamming.hamming_distance("karolin", "kathrin"), 3)

    def test_binary_strings(self):
        self.assertEqual(hamming.hamming_distance("1011101", "1001001"), 2)

    def test_identical_strings(self):
        self.assertEqual(hamming.hamming_distance("abc", "abc"), 0)

    def test_completely_different_strings(self):
        self.assertEqual(hamming.hamming_distance("abc", "xyz"), 3)

    def test_empty_strings(self):
        self.assertEqual(hamming.hamming_distance("", ""), 0)

    def test_unequal_lengths_raises(self):
        with self.assertRaises(ValueError):
            hamming.hamming_distance("abc", "ab")


class TestIsWithin(unittest.TestCase):
    def test_within_true(self):
        self.assertIs(hamming.is_within("karolin", "kathrin", 3), True)

    def test_within_false(self):
        self.assertIs(hamming.is_within("karolin", "kathrin", 2), False)

    def test_zero_threshold_same(self):
        self.assertIs(hamming.is_within("abc", "abc", 0), True)

    def test_negative_threshold(self):
        self.assertIs(hamming.is_within("abc", "abd", -1), False)

    def test_unequal_lengths_raises(self):
        with self.assertRaises(ValueError):
            hamming.is_within("abc", "abcd", 3)


if __name__ == "__main__":
    unittest.main()
