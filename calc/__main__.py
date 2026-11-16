"""Command line interface for the calc package."""

import argparse

from calc import add, sub


def _number(text):
    """Parse ``text`` as an int when possible, otherwise as a float."""
    try:
        return int(text)
    except ValueError:
        return float(text)


def _result(value):
    """Drop the trailing ``.0`` from whole floats so output stays readable."""
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m calc")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="add two numbers")
    add_parser.add_argument("a", type=_number)
    add_parser.add_argument("b", type=_number)

    sub_parser = subparsers.add_parser("sub", help="subtract two numbers")
    sub_parser.add_argument("a", type=_number)
    sub_parser.add_argument("b", type=_number)

    args = parser.parse_args(argv)
    operation = add if args.command == "add" else sub
    print(_result(operation(args.a, args.b)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
