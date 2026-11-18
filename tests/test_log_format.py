"""tests/test_log_format.py: 只测 log_format 模块的行为。

记录桩在本文件内手工构造，不 import 解析模块。
"""

import unittest
from datetime import datetime

from log_format import format_record, format_records


class Record:
    """与解析模块产出同形的最小记录桩：timestamp / level / message。"""

    def __init__(self, timestamp, level, message):
        self.timestamp = timestamp
        self.level = level
        self.message = message


class TestFormatRecord(unittest.TestCase):
    def test_single_record_matches_uniform_line_shape(self):
        """单条记录输出与统一行格式逐字一致：日期 时间 级别 消息各归其位。"""
        record = Record(
            datetime(2026, 11, 18, 12, 3, 22), "INFO", "service started"
        )
        self.assertEqual(
            format_record(record), "2026-11-18 12:03:22 INFO service started"
        )

    def test_message_with_spaces_preserved_verbatim(self):
        """消息含多个空格时逐字保留，不被压缩或改写。"""
        record = Record(
            datetime(2026, 1, 2, 3, 4, 5), "ERROR", "db  down   retrying now"
        )
        self.assertEqual(
            format_record(record),
            "2026-01-02 03:04:05 ERROR db  down   retrying now",
        )

    def test_round_trip_identity(self):
        """格式良好的行 -> 记录桩 -> 同一行（格式化是行格式的精确逆操作）。"""
        line = "2026-11-18 12:03:22 INFO service started"
        date_str, time_str, level, message = line.split(" ", 3)
        stamp = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
        record = Record(stamp, level, message)
        self.assertEqual(format_record(record), line)


class TestFormatRecords(unittest.TestCase):
    def test_multi_record_formatting_preserves_order(self):
        """多条记录格式化为等长行列表，顺序与输入一一对应。"""
        records = [
            Record(datetime(2026, 11, 18, 12, 0, 0), "DEBUG", "first event"),
            Record(datetime(2026, 11, 18, 12, 0, 1), "WARN", "second event"),
            Record(datetime(2026, 11, 18, 12, 0, 2), "ERROR", "third event"),
        ]
        self.assertEqual(
            format_records(records),
            [
                "2026-11-18 12:00:00 DEBUG first event",
                "2026-11-18 12:00:01 WARN second event",
                "2026-11-18 12:00:02 ERROR third event",
            ],
        )


if __name__ == "__main__":
    unittest.main()
