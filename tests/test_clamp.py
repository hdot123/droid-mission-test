from clamp import clamp


def test_clamp_within_range_returns_v():
    assert clamp(5, 1, 10) == 5


def test_clamp_below_lo_returns_lo():
    assert clamp(-3, 0, 100) == 0


def test_clamp_above_hi_returns_hi():
    assert clamp(99, 0, 10) == 10


def test_additional_check_from_work_order_acceptance():
    # Work order acceptance states clamp(7, 0, 10) must equal 10, while the
    # function spec says in-range values return v itself (which is 7 here).
    # Recorded verbatim from the acceptance section as instructed.
    assert clamp(7, 0, 10) == 10
