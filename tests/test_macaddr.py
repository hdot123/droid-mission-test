"""macaddr.py 的验收测试。"""

import unittest

import macaddr


class TestNormalize(unittest.TestCase):
    def test_colon_upper(self):
        self.assertEqual(macaddr.normalize("AA:BB:CC:DD:EE:FF"), "aa:bb:cc:dd:ee:ff")

    def test_hyphen(self):
        self.assertEqual(macaddr.normalize("AA-BB-CC-DD-EE-FF"), "aa:bb:cc:dd:ee:ff")

    def test_dot(self):
        self.assertEqual(macaddr.normalize("AABB.CCDD.EEFF"), "aa:bb:cc:dd:ee:ff")

    def test_too_few_groups(self):
        with self.assertRaises(ValueError):
            macaddr.normalize("aa:bb:cc:dd:ee")

    def test_non_hex(self):
        with self.assertRaises(ValueError):
            macaddr.normalize("GG:BB:CC:DD:EE:FF")

    def test_mixed_separators(self):
        with self.assertRaises(ValueError):
            macaddr.normalize("AA:BB-CC-DD-EE-FF")

    def test_lowercase_input(self):
        self.assertEqual(macaddr.normalize("aa:bb:cc:dd:ee:ff"), "aa:bb:cc:dd:ee:ff")

    def test_too_many_groups(self):
        with self.assertRaises(ValueError):
            macaddr.normalize("AA:BB:CC:DD:EE:FF:00")

    def test_wrong_group_length(self):
        with self.assertRaises(ValueError):
            macaddr.normalize("AAB.CCDD.EEFF")
        with self.assertRaises(ValueError):
            macaddr.normalize("AA:BBB:CC:DD:EE:FF")

    def test_empty_string(self):
        with self.assertRaises(ValueError):
            macaddr.normalize("")


if __name__ == "__main__":
    unittest.main()
