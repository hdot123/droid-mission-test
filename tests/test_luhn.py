"""tests/test_luhn.py: luhn.py 的验收测试。"""

import unittest

import luhn


class TestLuhn(unittest.TestCase):
    def test_known_valid(self):
        self.assertTrue(luhn.is_valid("79927398713"))
        self.assertTrue(luhn.is_valid("4242424242424242"))

    def test_known_invalid(self):
        self.assertFalse(luhn.is_valid("79927398710"))
        self.assertFalse(luhn.is_valid("4242424242424241"))

    def test_check_digit(self):
        self.assertEqual(luhn.check_digit("7992739871"), 3)
        self.assertEqual(luhn.check_digit("424242424242424"), 2)

    def test_check_digit_makes_valid(self):
        self.assertTrue(luhn.is_valid("7992739871" + str(luhn.check_digit("7992739871"))))
        self.assertTrue(
            luhn.is_valid("424242424242424" + str(luhn.check_digit("424242424242424")))
        )

    def test_is_valid_rejects_non_digits(self):
        with self.assertRaises(ValueError):
            luhn.is_valid("12a3")

    def test_check_digit_rejects_empty(self):
        with self.assertRaises(ValueError):
            luhn.check_digit("")


if __name__ == "__main__":
    unittest.main()
