import pytest

from parity2d import add_parity, locate_error

BASE = ["1010", "0101", "1111"]


def flip(block, row, col):
    lines = list(block)
    chars = list(lines[row])
    chars[col] = "1" if chars[col] == "0" else "0"
    lines[row] = "".join(chars)
    return lines


def test_add_parity_example():
    assert add_parity(["101", "010"]) == ["1010", "0101", "1111"]


def test_add_parity_does_not_mutate_input():
    rows = ["101", "010"]
    out = add_parity(rows)
    assert rows == ["101", "010"]
    assert out is not rows


def test_locate_clean_block_returns_none():
    assert locate_error(add_parity(["101", "010"])) is None
    assert locate_error(BASE) is None


def test_locate_single_data_flip():
    assert locate_error(flip(BASE, 0, 1)) == (0, 1)


def test_locate_check_row_flip():
    flipped = flip(BASE, 2, 2)
    assert locate_error(flipped) == (2, 2)


def test_locate_check_column_flip():
    assert locate_error(flip(BASE, 0, 3)) == (0, 3)


def test_locate_corner_flip():
    assert locate_error(flip(BASE, 2, 3)) == (2, 3)


def test_all_single_bit_flips_located():
    block = add_parity(["1100", "1001", "0110", "1010"])
    for r in range(len(block)):
        for c in range(len(block[0])):
            assert locate_error(flip(block, r, c)) == (r, c)


def test_output_all_rows_and_columns_even():
    block = add_parity(["11010", "10101", "00111", "11100"])
    for line in block:
        assert line.count("1") % 2 == 0
    for j in range(len(block[0])):
        assert sum(block[i][j] == "1" for i in range(len(block))) % 2 == 0


def test_add_parity_unequal_lengths():
    with pytest.raises(ValueError):
        add_parity(["10", "1"])


def test_add_parity_empty_list():
    with pytest.raises(ValueError):
        add_parity([])


def test_add_parity_invalid_characters():
    with pytest.raises(ValueError):
        add_parity(["1a0", "010"])
    with pytest.raises(ValueError):
        add_parity(["10", "0x"])


def test_add_parity_empty_row():
    with pytest.raises(ValueError):
        add_parity([""])


def test_add_parity_single_row_and_column():
    assert add_parity(["0"]) == ["00", "00"]
    assert add_parity(["1"]) == ["11", "11"]
    assert locate_error(add_parity(["1"])) is None
    assert locate_error(flip(add_parity(["1"]), 0, 0)) == (0, 0)


def test_locate_two_errors_same_row():
    with pytest.raises(ValueError):
        locate_error(flip(flip(BASE, 0, 0), 0, 1))


def test_locate_two_errors_same_column():
    with pytest.raises(ValueError):
        locate_error(flip(flip(BASE, 0, 1), 1, 1))


def test_locate_two_errors_scattered():
    with pytest.raises(ValueError):
        locate_error(flip(flip(BASE, 0, 0), 1, 2))


def test_locate_malformed_block():
    with pytest.raises(ValueError):
        locate_error([])
    with pytest.raises(ValueError):
        locate_error(["101", "01"])
    with pytest.raises(ValueError):
        locate_error(["12", "34"])
    with pytest.raises(ValueError):
        locate_error(["0"])
