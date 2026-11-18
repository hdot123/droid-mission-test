"""Tests for transpose.py (transpose and multiply)."""

import pytest

import transpose


def test_transpose_basic_example():
    assert transpose.transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]


def test_transpose_square():
    matrix = [[1, 2], [3, 4]]
    assert transpose.transpose(matrix) == [[1, 3], [2, 4]]


def test_transpose_empty():
    assert transpose.transpose([]) == []


def test_transpose_single_row():
    assert transpose.transpose([[1, 2, 3]]) == [[1], [2], [3]]


def test_transpose_does_not_modify_input():
    matrix = [[1, 2, 3], [4, 5, 6]]
    original = [row[:] for row in matrix]
    transpose.transpose(matrix)
    assert matrix == original


def test_transpose_inconsistent_rows_raises():
    with pytest.raises(ValueError):
        transpose.transpose([[1, 2], [3]])


def test_multiply_basic_example():
    a = [[1, 2], [3, 4]]
    b = [[5, 6], [7, 8]]
    assert transpose.multiply(a, b) == [[19, 22], [43, 50]]


def test_multiply_identity():
    identity = [[1, 0], [0, 1]]
    matrix = [[1, 2], [3, 4]]
    assert transpose.multiply(matrix, identity) == matrix
    assert transpose.multiply(identity, matrix) == matrix


def test_multiply_rectangular():
    a = [[1, 2, 3]]
    b = [[4], [5], [6]]
    assert transpose.multiply(a, b) == [[32]]
    assert transpose.multiply(b, a) == [[4, 8, 12], [5, 10, 15], [6, 12, 18]]


def test_multiply_inner_dimension_mismatch_raises():
    with pytest.raises(ValueError):
        transpose.multiply([[1, 2, 3]], [[1, 2]])


def test_multiply_does_not_modify_inputs():
    a = [[1, 2], [3, 4]]
    b = [[5, 6], [7, 8]]
    a_orig = [row[:] for row in a]
    b_orig = [row[:] for row in b]
    transpose.multiply(a, b)
    assert a == a_orig
    assert b == b_orig
