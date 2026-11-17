"""Tests for the fizzbuzz module."""

from fizzbuzz import generate


def test_required_example():
    assert generate(5) == ["1", "2", "Fizz", "4", "Buzz"]


def test_n_less_than_one_returns_empty_list():
    assert generate(0) == []
    assert generate(-3) == []


def test_multiple_of_15_is_fizzbuzz():
    assert generate(15)[-1] == "FizzBuzz"


def test_multiples_of_3_are_fizz():
    assert generate(3) == ["1", "2", "Fizz"]
    assert generate(6)[-1] == "Fizz"


def test_multiples_of_5_are_buzz():
    assert generate(5)[-1] == "Buzz"
    assert generate(10)[-1] == "Buzz"


def test_plain_numbers_as_strings():
    assert generate(4) == ["1", "2", "Fizz", "4"]
    assert all(isinstance(item, str) for item in generate(7))
