"""Tests for the Stack class and eval_rpn in stack.py."""

import pytest

from stack import Stack, eval_rpn


class TestStack:
    def test_push_pop(self):
        s = Stack()
        s.push(1)
        s.push(2)
        assert s.pop() == 2
        assert s.pop() == 1

    def test_peek(self):
        s = Stack()
        s.push("a")
        assert s.peek() == "a"
        assert len(s) == 1
        assert s.pop() == "a"

    def test_is_empty(self):
        s = Stack()
        assert s.is_empty()
        s.push(1)
        assert not s.is_empty()
        s.pop()
        assert s.is_empty()

    def test_len(self):
        s = Stack()
        assert len(s) == 0
        s.push(1)
        s.push(2)
        assert len(s) == 2
        s.pop()
        assert len(s) == 1

    def test_pop_empty_raises_index_error(self):
        with pytest.raises(IndexError):
            Stack().pop()

    def test_peek_empty_raises_index_error(self):
        with pytest.raises(IndexError):
            Stack().peek()


class TestEvalRpn:
    def test_example_multiplication(self):
        assert eval_rpn(["2", "1", "+", "3", "*"]) == 9

    def test_example_division(self):
        assert eval_rpn(["4", "13", "5", "/", "+"]) == 6

    def test_example_negative_division(self):
        assert eval_rpn(["-7", "2", "/"]) == -3

    def test_negative_operands(self):
        assert eval_rpn(["-1", "-2", "+"]) == -3
        assert eval_rpn(["-7", "2", "*"]) == -14
        assert eval_rpn(["3", "-4", "-"]) == 7

    def test_division_truncates_toward_zero(self):
        assert eval_rpn(["-7", "2", "/"]) == -3
        assert eval_rpn(["7", "-2", "/"]) == -3
        assert eval_rpn(["-8", "3", "/"]) == -2

    def test_results_are_ints(self):
        result = eval_rpn(["2", "1", "+", "3", "*"])
        assert isinstance(result, int)

    def test_division_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            eval_rpn(["1", "0", "/"])
        with pytest.raises(ZeroDivisionError):
            eval_rpn(["0", "0", "/"])
        with pytest.raises(ZeroDivisionError):
            eval_rpn(["1", "2", "2", "-", "/"])  # 1 / (2 - 2) = 1 / 0

    def test_empty_tokens(self):
        with pytest.raises(ValueError):
            eval_rpn([])

    def test_not_enough_operands(self):
        with pytest.raises(ValueError):
            eval_rpn(["1", "+"])
        with pytest.raises(ValueError):
            eval_rpn(["+"])

    def test_leftover_operands(self):
        with pytest.raises(ValueError):
            eval_rpn(["1", "2", "3"])
        with pytest.raises(ValueError):
            eval_rpn(["1", "2", "+", "3", "4"])

    def test_invalid_token(self):
        with pytest.raises(ValueError):
            eval_rpn(["1", "2", "%"])
