"""Tests for tally.verdict."""

from tally import verdict


def test_verdict_pass_at_pass_line():
    assert verdict(70) == "pass"


def test_verdict_fail_below_pass_line():
    assert verdict(65) == "fail"


def test_verdict_fail_just_below_pass_line():
    assert verdict(59) == "fail"


def test_verdict_fail_at_zero():
    assert verdict(0) == "fail"
