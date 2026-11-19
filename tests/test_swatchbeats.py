import pytest

from swatchbeats import from_beats, to_beats


def test_to_beats_acceptance_examples():
    assert to_beats(0, 0, 0) == 41.67
    assert to_beats(12, 0, 0) == 541.67
    assert to_beats(23, 0, 0) == 0.0
    assert to_beats(6, 30, 0) == 312.5
    assert to_beats(18, 0, 0) == 791.67
    assert to_beats(23, 59, 59) == 41.66
    assert to_beats(1, 0, 0) == 83.33
    assert to_beats(9, 15, 30) == 427.43


def test_from_beats_acceptance_examples():
    assert from_beats(41.67) == (0, 0, 0)
    assert from_beats(0.0) == (23, 0, 0)
    assert from_beats(500.0) == (11, 0, 0)
    assert from_beats(541.67) == (12, 0, 0)
    assert from_beats(999.99) == (22, 59, 59)


def test_roundtrip_within_0_02():
    for h, m, s in ((0, 0, 0), (5, 45, 30), (12, 0, 0), (18, 20, 10), (23, 59, 0)):
        expected = to_beats(h, m, s)
        assert abs(to_beats(*from_beats(expected)) - expected) <= 0.02


def test_to_beats_out_of_range_raises_value_error():
    for args in ((24, 0, 0), (0, 60, 0), (0, 0, 60), (-1, 0, 0)):
        with pytest.raises(ValueError):
            to_beats(*args)


def test_to_beats_non_int_raises_type_error():
    with pytest.raises(TypeError):
        to_beats(1.5, 0, 0)


def test_to_beats_rejects_bool():
    with pytest.raises(TypeError):
        to_beats(True, 0, 0)
    with pytest.raises(TypeError):
        to_beats(0, False, 0)
    with pytest.raises(TypeError):
        to_beats(0, 0, True)


def test_from_beats_out_of_range_raises_value_error():
    for beats in (1000.0, -1.0):
        with pytest.raises(ValueError):
            from_beats(beats)


def test_from_beats_non_numeric_raises_type_error():
    with pytest.raises(TypeError):
        from_beats("500")


def test_from_beats_rejects_bool():
    with pytest.raises(TypeError):
        from_beats(True)
