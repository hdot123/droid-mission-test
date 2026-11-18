"""Tests for the Spartan scytale transposition cipher."""

import unittest

from scytale import scytale_decrypt, scytale_encrypt


class TestScytaleEncrypt(unittest.TestCase):
    def test_hello_circ3(self):
        self.assertEqual(scytale_encrypt("HELLO", 3), "HLEOLX")

    def test_attack_at_dawn_circ4(self):
        self.assertEqual(scytale_encrypt("ATTACKATDAWN", 4), "ACDTKATAWATN")

    def test_we_are_discovered_circ5(self):
        self.assertEqual(scytale_encrypt("WEAREDISCOVERED", 5), "WDVEIEASRRCEEOD")

    def test_hello_circ1(self):
        self.assertEqual(scytale_encrypt("HELLO", 1), "HELLO")

    def test_exact_multiple_no_padding(self):
        self.assertEqual(scytale_encrypt("ABC", 3), "ABC")

    def test_empty_string(self):
        self.assertEqual(scytale_encrypt("", 3), "")

    def test_zero_circ_raises_value_error(self):
        with self.assertRaises(ValueError):
            scytale_encrypt("HELLO", 0)

    def test_negative_circ_raises_value_error(self):
        with self.assertRaises(ValueError):
            scytale_encrypt("HELLO", -2)

    def test_non_str_input_raises_type_error(self):
        with self.assertRaises(TypeError):
            scytale_encrypt(123, 3)


class TestScytaleDecrypt(unittest.TestCase):
    def test_hello_circ3(self):
        self.assertEqual(scytale_decrypt("HLEOLX", 3), "HELLOX")

    def test_attack_at_dawn_circ4(self):
        self.assertEqual(scytale_decrypt("ACDTKATAWATN", 4), "ATTACKATDAWN")

    def test_we_are_discovered_circ5(self):
        self.assertEqual(scytale_decrypt("WDVEIEASRRCEEOD", 5), "WEAREDISCOVERED")

    def test_empty_string(self):
        self.assertEqual(scytale_decrypt("", 3), "")

    def test_length_not_multiple_of_circ_raises_value_error(self):
        with self.assertRaises(ValueError):
            scytale_decrypt("HELLO", 3)

    def test_zero_circ_raises_value_error(self):
        with self.assertRaises(ValueError):
            scytale_decrypt("", 0)
        with self.assertRaises(ValueError):
            scytale_decrypt("HLEOLX", 0)

    def test_negative_circ_raises_value_error(self):
        with self.assertRaises(ValueError):
            scytale_decrypt("HLEOLX", -2)

    def test_non_str_input_raises_type_error(self):
        with self.assertRaises(TypeError):
            scytale_decrypt(123, 3)


class TestRoundTrip(unittest.TestCase):
    def test_round_trip_returns_padded_plaintext(self):
        for text, circ in [("HELLO", 3), ("ATTACKATDAWN", 4), ("WEAREDISCOVERED", 5), ("ABC", 3)]:
            padded_len = ((len(text) + circ - 1) // circ) * circ
            padded = text + "X" * (padded_len - len(text))
            self.assertEqual(scytale_decrypt(scytale_encrypt(text, circ), circ), padded)


if __name__ == "__main__":
    unittest.main()
