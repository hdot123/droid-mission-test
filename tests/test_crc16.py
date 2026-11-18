"""Tests for CRC-16/CCITT-FALSE (crc16.py)."""

import unittest

import crc16


class TestCrc16(unittest.TestCase):
    def test_check_value_123456789(self):
        self.assertEqual(crc16.compute(b"123456789"), 0x29B1)

    def test_check_value_123456789_decimal(self):
        self.assertEqual(crc16.compute(b"123456789"), 10673)

    def test_empty_input(self):
        self.assertEqual(crc16.compute(b""), 0xFFFF)

    def test_single_zero_byte(self):
        self.assertEqual(crc16.compute(b"\x00"), 0xE1F0)

    def test_single_zero_byte_decimal(self):
        self.assertEqual(crc16.compute(b"\x00"), 57840)


if __name__ == "__main__":
    unittest.main()
