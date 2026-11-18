"""Matrix utilities: transpose and multiply for list-of-lists matrices."""


def transpose(matrix):
    """Return the transpose of `matrix` as a new list of lists.

    - Empty list returns an empty list.
    - Raises ValueError if rows have inconsistent lengths.
    - The input matrix is not modified.
    """
    if not matrix:
        return []
    row_len = len(matrix[0])
    for row in matrix:
        if len(row) != row_len:
            raise ValueError("rows have inconsistent lengths")
    return [list(col) for col in zip(*matrix)]


def multiply(a, b):
    """Return the matrix product a x b.

    Raises ValueError if the inner dimensions do not match
    (columns of a must equal rows of b).
    """
    if not a and not b:
        return []
    if not a or not b:
        raise ValueError("inner dimensions do not match")
    cols_b = len(b[0])
    for row in b:
        if len(row) != cols_b:
            raise ValueError("rows of b have inconsistent lengths")
    inner = len(a[0])
    for row in a:
        if len(row) != inner:
            raise ValueError("rows of a have inconsistent lengths")
    if inner != len(b):
        raise ValueError("inner dimensions do not match")
    return [
        [sum(x * y for x, y in zip(row_a, col_b)) for col_b in zip(*b)]
        for row_a in a
    ]
