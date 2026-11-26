"""Tests for deque.Deque (R55 并发 B 单 · 队列件)."""

import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from deque import Deque


# --- 验收要点: 空队列基本状态 -------------------------------------------------

def test_empty_is_empty():
    assert Deque().is_empty() is True


def test_empty_len_zero():
    assert len(Deque()) == 0


# --- 验收要点: append / appendleft / to_list / len ---------------------------

def test_append_appendleft_to_list_len():
    d = Deque()
    d.append(1)
    d.append(2)
    d.appendleft(0)
    assert d.to_list() == [0, 1, 2]
    assert len(d) == 3


# --- 验收要点: peek / peekleft ------------------------------------------------

def test_peek_and_peekleft():
    d = Deque()
    d.append(1)
    d.append(2)
    d.appendleft(0)
    assert d.peek() == 2
    assert d.peekleft() == 0
    # peek 不移除
    assert d.to_list() == [0, 1, 2]


# --- 验收要点: pop / popleft --------------------------------------------------

def test_pop_popleft():
    d = Deque()
    d.append(1)
    d.append(2)
    d.appendleft(0)
    assert d.pop() == 2
    assert d.popleft() == 0
    assert d.to_list() == [1]


# --- 验收要点: 可迭代对象初始化 ------------------------------------------------

def test_init_from_list():
    assert Deque([5, 6, 7]).to_list() == [5, 6, 7]


def test_init_from_string():
    assert Deque("ab").to_list() == ["a", "b"]


# --- 验收要点: clear ----------------------------------------------------------

def test_clear():
    d = Deque([1, 2, 3])
    d.clear()
    assert d.is_empty() is True
    assert d.to_list() == []


# --- 验收要点: 模型一致性（长序列混合操作） ------------------------------------

def test_model_consistency_long_mixed_sequence():
    rng = random.Random(20260226)
    d = Deque()
    model: list = []
    for _ in range(600):
        op = rng.choice(["append", "appendleft", "pop", "popleft", "peek", "peekleft", "clear", "len"])
        if op == "append":
            v = rng.randrange(1000)
            d.append(v)
            model.append(v)
        elif op == "appendleft":
            v = rng.randrange(1000)
            d.appendleft(v)
            model.insert(0, v)
        elif op == "pop":
            if model:
                assert d.pop() == model.pop()
            else:
                with pytest.raises(IndexError):
                    d.pop()
        elif op == "popleft":
            if model:
                assert d.popleft() == model.pop(0)
            else:
                with pytest.raises(IndexError):
                    d.popleft()
        elif op == "peek":
            if model:
                assert d.peek() == model[-1]
            else:
                with pytest.raises(IndexError):
                    d.peek()
        elif op == "peekleft":
            if model:
                assert d.peekleft() == model[0]
            else:
                with pytest.raises(IndexError):
                    d.peekleft()
        elif op == "clear":
            d.clear()
            model.clear()
        else:  # len
            assert len(d) == len(model)
        # 每步 to_list() 与模型一致
        assert d.to_list() == model
        assert d.is_empty() is (len(model) == 0)


# --- 验收要点: 空队列上 pop/popleft/peek/peekleft 抛 IndexError ----------------

def test_empty_pop_raises_indexerror():
    with pytest.raises(IndexError):
        Deque().pop()


def test_empty_popleft_raises_indexerror():
    with pytest.raises(IndexError):
        Deque().popleft()


def test_empty_peek_raises_indexerror():
    with pytest.raises(IndexError):
        Deque().peek()


def test_empty_peekleft_raises_indexerror():
    with pytest.raises(IndexError):
        Deque().peekleft()
