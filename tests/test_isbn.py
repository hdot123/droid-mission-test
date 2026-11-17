"""Tests for isbn.is_valid_isbn10 (this module only)."""

from isbn import is_valid_isbn10


def test_valid_plain():
    assert is_valid_isbn10('0306406152')


def test_valid_with_hyphens_and_spaces():
    assert is_valid_isbn10('0-306-40615-2')
    assert is_valid_isbn10('0 306 40615 2')


def test_valid_trailing_x():
    # 10*0+9*8+8*0+7*4+6*4+5*2+4*9+3*5+2*7+1*10 = 209 = 11*19
    assert is_valid_isbn10('080442957X')
    assert is_valid_isbn10('0-8044-2957-X')


def test_wrong_check_digit_rejected():
    assert not is_valid_isbn10('0306406153')
    assert not is_valid_isbn10('0804429571')


def test_wrong_length_rejected():
    assert not is_valid_isbn10('030640615')
    assert not is_valid_isbn10('03064061522')


def test_x_not_last_rejected():
    assert not is_valid_isbn10('X306406152')
    assert not is_valid_isbn10('0X06406152')


def test_x_with_wrong_value_rejected():
    # X at the end but the sum is not divisible by 11
    assert not is_valid_isbn10('030640615X')


def test_empty_and_garbage_rejected():
    assert not is_valid_isbn10('')
    assert not is_valid_isbn10('abcdefghij')
    assert not is_valid_isbn10('0306-406-15!')
