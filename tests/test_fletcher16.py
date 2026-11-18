"""tests/test_fletcher16.py: Fletcher-16 校验和验收测试。"""

import unittest

import fletcher16


class TestFletcher16(unittest.TestCase):
    def test_empty_input_is_zero(self):
        self.assertEqual(fletcher16.checksum(b""), 0)

    def test_abcde(self):
        self.assertEqual(fletcher16.checksum(b"abcde"), 0xC8F0)
        self.assertEqual(fletcher16.checksum(b"abcde"), 51440)

    def test_abcdef(self):
        self.assertEqual(fletcher16.checksum(b"abcdef"), 0x2057)
        self.assertEqual(fletcher16.checksum(b"abcdef"), 8279)

    def test_verify_true(self):
        self.assertTrue(fletcher16.verify(b"abcde", 51440))

    def test_verify_false(self):
        self.assertFalse(fletcher16.verify(b"abcde", 51441))

    def test_single_byte(self):
        self.assertEqual(fletcher16.checksum(b"\x01"), 0x0101)


if __name__ == "__main__":
    unittest.main()
