"""Tests for wordscore only."""

import unittest

from wordscore import score


class TestWordscore(unittest.TestCase):
    def test_bad_equals_7(self):
        # Acceptance example group (hard requirement): score("bad") equals 7.
        self.assertEqual(score("bad"), 7)

    def test_abc_equals_7(self):
        # Authoritative value per acceptance criteria (hard gate): score("abc") == 7.
        # (The work-order body example text, preserved as evidence only in the
        # handoff/status, states score("abc") returns 6; acceptance criteria
        # resolve this to 7. This assertion encodes the authoritative value.)
        self.assertEqual(score("abc"), 7)

    def test_z_returns_26(self):
        self.assertEqual(score("z"), 26)

    def test_hyphen_ignored(self):
        self.assertEqual(score("a-b"), 3)

    def test_empty_string_returns_0(self):
        self.assertEqual(score(""), 0)

    def test_no_letters_returns_0(self):
        self.assertEqual(score("123!?"), 0)

    def test_case_insensitive(self):
        # Case-insensitive: the acceptance-gate value applies to any casing
        # of "abc", and other words follow the formula.
        self.assertEqual(score("AbC"), score("abc"))
        self.assertEqual(score("BAD"), score("bad"))

    def test_non_ascii_letters_ignored(self):
        # é is not an a-z letter position; only ASCII a-z/a-Z count.
        self.assertEqual(score("café"), score("caf"))


if __name__ == "__main__":
    unittest.main()
