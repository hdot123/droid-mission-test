import subprocess
import sys
from pathlib import Path

import pytest

from calc import add, sub

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
        (-3, -4, -7),
        (1.5, 2.5, 4.0),
    ],
)
def test_add(a, b, expected):
    assert add(a, b) == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (5, 3, 2),
        (0, 0, 0),
        (3, 5, -2),
        (-2, -2, 0),
        (2.5, 1.0, 1.5),
    ],
)
def test_sub(a, b, expected):
    assert sub(a, b) == expected


def run_calc(*args):
    return subprocess.run(
        [sys.executable, "-m", "calc", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def test_cli_add():
    result = run_calc("add", "1", "2")
    assert result.returncode == 0
    assert result.stdout.strip() == "3"


def test_cli_sub():
    result = run_calc("sub", "5", "3")
    assert result.returncode == 0
    assert result.stdout.strip() == "2"


def test_cli_requires_operands():
    result = run_calc("add", "1")
    assert result.returncode != 0
