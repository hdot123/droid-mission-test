"""tests/test_log_parser.py: 只测 log_parser 模块的解析行为。"""

import unittest
from datetime import datetime

from log_parser import LEVELS, LogRecord, ParseError, parse_line, parse_lines


class TestParseWellFormed(unittest.TestCase):
    def test_well_formed_line_parses_into_record(self):
        result = parse_line("2026-11-18 12:03:22 INFO service started")
        self.assertIsInstance(result, LogRecord)
        self.assertEqual(result.timestamp, datetime(2026, 11, 18, 12, 3, 22))
        self.assertEqual(result.level, "INFO")
        self.assertEqual(result.message, "service started")

    def test_all_four_levels_parse(self):
        for level in LEVELS:
            with self.subTest(level=level):
                result = parse_line(f"2026-01-01 00:00:00 {level} some message")
                self.assertIsInstance(result, LogRecord)
                self.assertEqual(result.level, level)

    def test_message_keeps_internal_spaces_and_multiword_text(self):
        result = parse_line("2026-11-18 12:03:22 ERROR connection to db failed")
        self.assertIsInstance(result, LogRecord)
        self.assertEqual(result.message, "connection to db failed")

    def test_parse_lines_preserves_order_and_keeps_every_line(self):
        lines = [
            "2026-11-18 12:03:22 INFO a",
            "not a log line",
            "2026-11-18 12:03:23 WARN b",
        ]
        results = parse_lines(lines)
        self.assertEqual(len(results), 3)
        self.assertIsInstance(results[0], LogRecord)
        self.assertIsInstance(results[1], ParseError)
        self.assertIsInstance(results[2], LogRecord)
        self.assertEqual(results[0].message, "a")
        self.assertEqual(results[2].message, "b")


class TestParseMalformed(unittest.TestCase):
    def assert_malformed(self, line):
        result = parse_line(line)
        self.assertIsInstance(
            result, ParseError, f"expected ParseError for {line!r}, got {result!r}"
        )
        self.assertEqual(result.line, line)
        self.assertTrue(result.reason)
        return result

    def test_wrong_field_count_missing_message(self):
        # 只有日期、时间、级别三个字段 -> 字段数量不对。
        self.assert_malformed("2026-11-18 12:03:22 INFO")

    def test_wrong_field_count_incomplete_prefix(self):
        self.assert_malformed("2026-11-18")

    def test_bad_date_shape(self):
        self.assert_malformed("18-11-2026 12:03:22 INFO started")
        self.assert_malformed("2026/11/18 12:03:22 INFO started")

    def test_bad_time_shape(self):
        self.assert_malformed("2026-11-18 12:03 INFO started")
        self.assert_malformed("2026-11-18 25:03:22 INFO started")

    def test_unknown_level_is_malformed(self):
        self.assert_malformed("2026-11-18 12:03:22 FATAL boom")
        self.assert_malformed("2026-11-18 12:03:22 TRACE boom")

    def test_no_message_after_level_is_malformed(self):
        # 级别之后没有消息（即使有尾随空格也算没有消息）。
        self.assert_malformed("2026-11-18 12:03:22 ERROR")

    def test_blank_line_is_malformed(self):
        self.assert_malformed("")
        self.assert_malformed("   ")

    def test_parse_error_is_not_a_log_record(self):
        result = parse_line("2026-11-18 12:03:22 FATAL boom")
        self.assertNotIsInstance(result, LogRecord)
        self.assertIsInstance(result, ParseError)


if __name__ == "__main__":
    unittest.main()
