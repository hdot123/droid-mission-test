"""CLI entry point: python -m calc add 1 2 / python -m calc sub 5 3."""

import sys

from calc import add, sub


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) != 3:
        print("usage: python -m calc {add,sub} a b", file=sys.stderr)
        return 2

    op, a_str, b_str = argv
    try:
        a = _parse_number(a_str)
        b = _parse_number(b_str)
    except ValueError:
        print(f"error: invalid number: {a_str} or {b_str}", file=sys.stderr)
        return 2

    if op == "add":
        print(add(a, b))
    elif op == "sub":
        print(sub(a, b))
    else:
        print(f"error: unknown operation: {op}", file=sys.stderr)
        return 2
    return 0


def _parse_number(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


if __name__ == "__main__":
    sys.exit(main())
