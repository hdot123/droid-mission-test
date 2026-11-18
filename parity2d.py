"""Two-dimensional even parity checking for blocks of '0'/'1' strings."""


def _validate(rows: list[str], min_rows: int, min_cols: int) -> int:
    """Check block shape/content; return the block width."""
    if not rows:
        raise ValueError("block must contain at least one row")
    width = len(rows[0])
    for row in rows:
        if len(row) != width:
            raise ValueError("all rows must have the same length")
        for ch in row:
            if ch not in ("0", "1"):
                raise ValueError("rows may only contain '0' and '1'")
    if width < min_cols:
        raise ValueError("block must contain at least %d column(s)" % min_cols)
    if len(rows) < min_rows:
        raise ValueError("block must contain at least %d row(s)" % min_rows)
    return width


def _parity_bit(count: int) -> str:
    """Even parity bit for a count of '1's: '0' when even, '1' when odd."""
    return "1" if count % 2 else "0"


def add_parity(rows: list[str]) -> list[str]:
    """Append a row-parity bit to each row, then append a column-parity row.

    Input rows must be non-empty, equal-length strings of '0'/'1' (at least
    1 row and 1 column); otherwise ValueError is raised.  Every row and every
    column of the result has even parity, the corner cell (check row, check
    column) being the parity of the whole block.
    """
    width = _validate(rows, min_rows=1, min_cols=1)
    checked = [row + _parity_bit(row.count("1")) for row in rows]
    col_bits = [
        _parity_bit(sum(1 for row in rows if row[j] == "1"))
        for j in range(width)
    ]
    col_bits.append(_parity_bit(col_bits.count("1")))
    checked.append("".join(col_bits))
    return checked


def locate_error(block: list[str]) -> tuple[int, int] | None:
    """Locate a single flipped bit in a checked block (add_parity output).

    Returns None when every row and column check passes, (row, col) when
    exactly one row check and one column check fail (the intersection is the
    flipped bit, in the data region or the check region), and raises
    ValueError for any other failure pattern or malformed block.
    """
    width = _validate(block, min_rows=2, min_cols=2)
    n_rows = len(block)
    # A row/column check fails exactly when that row/column holds an odd
    # number of '1's (check bit disagrees with the parity of its data bits).
    bad_rows = [i for i, row in enumerate(block) if row.count("1") % 2]
    bad_cols = [
        j
        for j in range(width)
        if sum(block[i][j] == "1" for i in range(n_rows)) % 2
    ]
    if not bad_rows and not bad_cols:
        return None
    if len(bad_rows) == 1 and len(bad_cols) == 1:
        return (bad_rows[0], bad_cols[0])
    raise ValueError(
        "cannot locate error: failing rows %s, failing columns %s"
        % (bad_rows, bad_cols)
    )
