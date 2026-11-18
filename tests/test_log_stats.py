"""Tests for log_stats.py (statistics/aggregation module only)."""

import unittest
from datetime import datetime, timedelta

from log_stats import LEVELS, count_by_level, error_frequency, error_rate, top_messages


class Record:
    """Hand-built record stub; does not import the parser module."""

    def __init__(self, timestamp, level, message):
        self.timestamp = timestamp
        self.level = level
        self.message = message


def make(ts, level, message):
    return Record(ts, level, message)


BASE = datetime(2026, 11, 18, 12, 0, 0)


class CountByLevelTests(unittest.TestCase):
    def test_empty_records_give_zero_for_every_level(self):
        counts = count_by_level([])
        self.assertEqual(counts, {level: 0 for level in LEVELS})

    def test_counts_each_level_and_includes_zero_levels(self):
        records = [
            make(BASE, "INFO", "a"),
            make(BASE, "INFO", "b"),
            make(BASE, "ERROR", "boom"),
            make(BASE, "WARN", "careful"),
            # DEBUG absent -> must still appear with count 0
        ]
        counts = count_by_level(records)
        self.assertEqual(counts["INFO"], 2)
        self.assertEqual(counts["ERROR"], 1)
        self.assertEqual(counts["WARN"], 1)
        self.assertEqual(counts["DEBUG"], 0)
        self.assertEqual(set(counts), set(LEVELS))

    def test_unknown_levels_are_ignored(self):
        records = [make(BASE, "FATAL", "nope"), make(BASE, "INFO", "ok")]
        counts = count_by_level(records)
        self.assertEqual(counts["INFO"], 1)
        self.assertEqual(sum(counts.values()), 1)


class ErrorFrequencyTests(unittest.TestCase):
    def setUp(self):
        self.start = datetime(2026, 11, 18, 12, 0, 0)
        self.end = datetime(2026, 11, 18, 13, 0, 0)
        self.records = [
            make(self.start - timedelta(seconds=1), "ERROR", "before"),
            make(self.start, "ERROR", "at-start"),
            make(self.start + timedelta(minutes=30), "ERROR", "inside"),
            make(self.end, "ERROR", "at-end"),
            make(self.end + timedelta(seconds=1), "ERROR", "after"),
            make(self.start + timedelta(minutes=10), "WARN", "not-error"),
            make(self.start + timedelta(minutes=10), "INFO", "not-error"),
        ]

    def test_counts_only_errors_inside_window(self):
        self.assertEqual(error_frequency(self.records, self.start, self.end), 3)

    def test_boundaries_are_inclusive(self):
        # "at-start" and "at-end" are both counted (inclusive boundaries).
        only_boundaries = [
            make(self.start, "ERROR", "at-start"),
            make(self.end, "ERROR", "at-end"),
        ]
        self.assertEqual(error_frequency(only_boundaries, self.start, self.end), 2)

    def test_records_outside_window_are_excluded(self):
        outside = [
            make(self.start - timedelta(seconds=1), "ERROR", "before"),
            make(self.end + timedelta(seconds=1), "ERROR", "after"),
        ]
        self.assertEqual(error_frequency(outside, self.start, self.end), 0)

    def test_non_error_records_inside_window_are_not_counted(self):
        inside_non_errors = [
            make(self.start + timedelta(minutes=5), "WARN", "w"),
            make(self.start + timedelta(minutes=5), "INFO", "i"),
            make(self.start + timedelta(minutes=5), "DEBUG", "d"),
        ]
        self.assertEqual(
            error_frequency(inside_non_errors, self.start, self.end), 0
        )

    def test_error_rate_expresses_frequency_over_window_duration(self):
        # 3 errors in a 1-hour window -> 3.0 per hour.
        self.assertAlmostEqual(
            error_rate(self.records, self.start, self.end), 3.0
        )
        # Zero-length window -> 0.0 (no duration to express a rate over).
        self.assertEqual(
            error_rate(self.records, self.start, self.start), 0.0
        )


class TopMessagesTests(unittest.TestCase):
    def test_orders_by_descending_count(self):
        records = [
            make(BASE, "INFO", "alpha"),
            make(BASE, "INFO", "alpha"),
            make(BASE, "INFO", "alpha"),
            make(BASE, "WARN", "beta"),
            make(BASE, "WARN", "beta"),
            make(BASE, "ERROR", "gamma"),
        ]
        self.assertEqual(
            top_messages(records),
            [("alpha", 3), ("beta", 2), ("gamma", 1)],
        )

    def test_ties_broken_by_message_text_ascending(self):
        records = [
            make(BASE, "INFO", "zeta"),
            make(BASE, "INFO", "zeta"),
            make(BASE, "INFO", "mu"),
            make(BASE, "INFO", "mu"),
            make(BASE, "INFO", "alpha"),
            make(BASE, "INFO", "alpha"),
        ]
        # All tied at 2 -> deterministic ascending-text order.
        self.assertEqual(
            top_messages(records),
            [("alpha", 2), ("mu", 2), ("zeta", 2)],
        )

    def test_limit_is_respected(self):
        records = [
            make(BASE, "INFO", "a"),
            make(BASE, "INFO", "a"),
            make(BASE, "INFO", "a"),
            make(BASE, "INFO", "b"),
            make(BASE, "INFO", "b"),
            make(BASE, "INFO", "c"),
        ]
        self.assertEqual(top_messages(records, limit=2), [("a", 3), ("b", 2)])
        self.assertEqual(len(top_messages(records, limit=1)), 1)
        self.assertEqual(top_messages(records, limit=0), [])

    def test_default_limit_is_ten(self):
        records = [
            make(BASE, "INFO", "m%02d" % i) for i in range(15)
        ]
        self.assertEqual(len(top_messages(records)), 10)

    def test_empty_records(self):
        self.assertEqual(top_messages([]), [])


if __name__ == "__main__":
    unittest.main()
