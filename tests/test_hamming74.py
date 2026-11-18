"""Tests for the (7,4) Hamming code component."""

import unittest

import hamming74


class TestEncode(unittest.TestCase):
    def test_encode_zero(self):
        self.assertEqual(hamming74.encode(0), 0)

    def test_encode_1011(self):
        self.assertEqual(hamming74.encode(0b1011), 0b0110011)  # 51

    def test_encode_out_of_range(self):
        with self.assertRaises(ValueError):
            hamming74.encode(16)


class TestRoundTrip(unittest.TestCase):
    def test_roundtrip_all_16_values(self):
        for data in range(16):
            self.assertEqual(hamming74.decode(hamming74.encode(data)), data)


class TestSingleBitCorrection(unittest.TestCase):
    def test_flip_each_bit_of_1011(self):
        codeword = hamming74.encode(0b1011)
        self.assertEqual(codeword, 0b0110011)
        for bit in range(7):
            flipped = codeword ^ (1 << bit)
            self.assertEqual(hamming74.decode(flipped), 0b1011)


if __name__ == "__main__":
    unittest.main()
