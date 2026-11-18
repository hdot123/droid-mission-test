"""Unit tests for the log_filter module.

Tests only log_filter's own behavior. Records are hand-built stubs defined
here, so this test never imports the parsing module (or any other module
besides log_filter and the standard library).
"""

import unittest
from datetime import datetime

import log_filter


class StubRecord:
    """Minimal record stub carrying timestamp, level, and message attributes."""

    def __init__(self, timestamp, level, message=""):
        self.timestamp = timestamp
        self.level = level
        self.message = message


def build_records():
    """Four records, one per level, spanning 12:00:00 to 12:10:00."""
    return [
        StubRecord(datetime(2026, 11, 18, 12, 0, 0), "DEBUG", "d1"),
        StubRecord(datetime(2026, 11, 18, 12, 3, 22), "INFO", "i1"),
        StubRecord(datetime(2026, 11, 18, 12, 5, 0), "WARN", "w1"),
        StubRecord(datetime(2026, 11, 18, 12, 10, 0), "ERROR", "e1"),
    ]


class SeverityConstantsTest(unittest.TestCase):
    def test_constants_match_documented_values(self):
        self.assertEqual(
            (log_filter.DEBUG, log_filter.INFO, log_filter.WARN, log_filter.ERROR),
            (0, 1, 2, 3),
        )

    def test_constants_order_levels_low_to_high(self):
        self.assertLess(log_filter.DEBUG, log_filter.INFO)
        self.assertLess(log_filter.INFO, log_filter.WARN)
        self.assertLess(log_filter.WARN, log_filter.ERROR)


class FilterByLevelTest(unittest.TestCase):
    def test_debug_threshold_keeps_all_records(self):
        records = build_records()
        result = log_filter.filter_by_level(records, log_filter.DEBUG)
        self.assertEqual(result, records)

    def test_error_threshold_keeps_only_error(self):
        records = build_records()
        result = log_filter.filter_by_level(records, log_filter.ERROR)
        self.assertEqual([r.level for r in result], ["ERROR"])
        self.assertEqual([r.message for r in result], ["e1"])

    def test_warn_threshold_drops_info_and_debug(self):
        records = build_records()
        result = log_filter.filter_by_level(records, log_filter.WARN)
        self.assertEqual([r.level for r in result], ["WARN", "ERROR"])
        self.assertEqual([r.message for r in result], ["w1", "e1"])

    def test_info_threshold_keeps_info_and_above(self):
        records = build_records()
        result = log_filter.filter_by_level(records, log_filter.INFO)
        self.assertEqual([r.level for r in result], ["INFO", "WARN", "ERROR"])

    def test_threshold_accepts_level_name_string(self):
        records = build_records()
        by_name = log_filter.filter_by_level(records, "WARN")
        by_const = log_filter.filter_by_level(records, log_filter.WARN)
        self.assertEqual(by_name, by_const)

    def test_record_level_may_be_severity_constant(self):
        records = [
            StubRecord(datetime(2026, 11, 18, 12, 0, 0), log_filter.ERROR),
            StubRecord(datetime(2026, 11, 18, 12, 1, 0), log_filter.INFO),
        ]
        result = log_filter.filter_by_level(records, log_filter.WARN)
        self.assertEqual(result, [records[0]])

    def test_unknown_threshold_raises_value_error(self):
        with self.assertRaises(ValueError):
            log_filter.filter_by_level(build_records(), "TRACE")

    def test_unknown_record_level_raises_value_error(self):
        records = [StubRecord(datetime(2026, 11, 18, 12, 0, 0), "FATAL")]
        with self.assertRaises(ValueError):
            log_filter.filter_by_level(records, log_filter.DEBUG)

    def test_level_filter_preserves_input_order(self):
        records = [
            StubRecord(datetime(2026, 11, 18, 12, 0, 0), "ERROR"),
            StubRecord(datetime(2026, 11, 18, 12, 1, 0), "DEBUG"),
            StubRecord(datetime(2026, 11, 18, 12, 2, 0), "INFO"),
            StubRecord(datetime(2026, 11, 18, 12, 3, 0), "WARN"),
        ]
        result = log_filter.filter_by_level(records, log_filter.INFO)
        self.assertEqual([r.level for r in result], ["ERROR", "INFO", "WARN"])

    def test_returns_new_list_without_mutating_input(self):
        records = build_records()
        original = list(records)
        result = log_filter.filter_by_level(records, log_filter.DEBUG)
        self.assertIsNot(result, records)
        self.assertEqual(records, original)

    def test_accepts_plain_sequence(self):
        records = tuple(build_records())
        result = log_filter.filter_by_level(records, log_filter.DEBUG)
        self.assertIsInstance(result, list)
        self.assertEqual(result, list(records))


class FilterByTimeTest(unittest.TestCase):
    def test_window_includes_both_endpoints(self):
        records = build_records()
        # start matches i1's timestamp exactly; end matches w1's exactly.
        start = datetime(2026, 11, 18, 12, 3, 22)
        end = datetime(2026, 11, 18, 12, 5, 0)
        result = log_filter.filter_by_time(records, start, end)
        self.assertEqual([r.message for r in result], ["i1", "w1"])

    def test_records_outside_window_are_dropped(self):
        records = build_records()
        start = datetime(2026, 11, 18, 12, 1, 0)
        end = datetime(2026, 11, 18, 12, 4, 0)
        result = log_filter.filter_by_time(records, start, end)
        # d1 (12:00) is before start; w1 (12:05) and e1 (12:10) are after end.
        self.assertEqual([r.message for r in result], ["i1"])

    def test_none_start_or_end_leaves_that_side_unbounded(self):
        records = build_records()
        end = datetime(2026, 11, 18, 12, 5, 0)
        self.assertEqual(
            [r.message for r in log_filter.filter_by_time(records, None, end)],
            ["d1", "i1", "w1"],
        )
        start = datetime(2026, 11, 18, 12, 3, 22)
        self.assertEqual(
            [r.message for r in log_filter.filter_by_time(records, start, None)],
            ["i1", "w1", "e1"],
        )

    def test_inverted_window_returns_empty_list(self):
        records = build_records()
        start = datetime(2026, 11, 18, 12, 6, 0)
        end = datetime(2026, 11, 18, 12, 5, 0)
        self.assertEqual(log_filter.filter_by_time(records, start, end), [])

    def test_time_filter_preserves_input_order(self):
        records = [
            StubRecord(datetime(2026, 11, 18, 12, 10, 0), "ERROR", "e1"),
            StubRecord(datetime(2026, 11, 18, 12, 0, 0), "DEBUG", "d1"),
            StubRecord(datetime(2026, 11, 18, 12, 5, 0), "WARN", "w1"),
            StubRecord(datetime(2026, 11, 18, 12, 3, 22), "INFO", "i1"),
        ]
        start = datetime(2026, 11, 18, 12, 0, 0)
        end = datetime(2026, 11, 18, 12, 10, 0)
        result = log_filter.filter_by_time(records, start, end)
        self.assertEqual([r.message for r in result], ["e1", "d1", "w1", "i1"])

    def test_record_without_timestamp_attribute_raises(self):
        class NoTimestamp(object):
            level = "INFO"

        with self.assertRaises(AttributeError):
            log_filter.filter_by_time(
                [NoTimestamp()],
                datetime(2026, 11, 18, 12, 0, 0),
                datetime(2026, 11, 18, 12, 5, 0),
            )

    def test_datetime_attribute_is_used_when_timestamp_absent(self):
        class AltRecord(object):
            def __init__(self, ts, level):
                self.datetime = ts
                self.level = level

        records = [AltRecord(datetime(2026, 11, 18, 12, 3, 0), "INFO")]
        start = datetime(2026, 11, 18, 12, 0, 0)
        end = datetime(2026, 11, 18, 12, 4, 0)
        result = log_filter.filter_by_time(records, start, end)
        self.assertEqual(result, records)

    def test_returns_new_list_without_mutating_input(self):
        records = build_records()
        original = list(records)
        start = datetime(2026, 11, 18, 12, 0, 0)
        end = datetime(2026, 11, 18, 12, 10, 0)
        result = log_filter.filter_by_time(records, start, end)
        self.assertIsNot(result, records)
        self.assertEqual(records, original)


class CombinedFilterTest(unittest.TestCase):
    def test_level_then_time(self):
        records = build_records()
        start = datetime(2026, 11, 18, 12, 0, 0)
        end = datetime(2026, 11, 18, 12, 5, 0)
        result = log_filter.filter_by_level(records, log_filter.WARN)
        result = log_filter.filter_by_time(result, start, end)
        # w1 passes both; e1 passes level but is outside the window;
        # d1/i1 are inside the window but below WARN.
        self.assertEqual([r.message for r in result], ["w1"])

    def test_time_then_level_gives_same_members_in_same_order(self):
        records = build_records()
        start = datetime(2026, 11, 18, 12, 0, 0)
        end = datetime(2026, 11, 18, 12, 5, 0)
        level_then_time = log_filter.filter_by_time(
            log_filter.filter_by_level(records, log_filter.WARN), start, end
        )
        time_then_level = log_filter.filter_by_level(
            log_filter.filter_by_time(records, start, end), log_filter.WARN
        )
        self.assertEqual(level_then_time, time_then_level)
        self.assertEqual([r.message for r in level_then_time], ["w1"])


if __name__ == "__main__":
    unittest.main()
