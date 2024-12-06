"""Unit tests for the Benchmark class."""

# pylint: disable=missing-function-docstring

import pytest
from rayne import Benchmark


def test_benchmark_default_init() -> None:
    b = Benchmark()
    assert b.name is None
    assert b.runs == 1000
    with pytest.raises(RuntimeError):
        assert b.run_time is None


def test_benchmark_custom_init() -> None:
    b = Benchmark(runs=9876, name="Hamlet")
    assert b.name == "Hamlet"
    assert b.runs == 9876
    with pytest.raises(RuntimeError):
        assert b.run_time is None


def test_context() -> None:
    class _RunTest:
        def __init__(self):
            self.__was_run = False

        @property
        def was_run(self) -> bool:
            return self.__was_run

        def __call__(self) -> None:
            self.__was_run = True

    s = _RunTest()
    with Benchmark() as b:
        b.set_user_code(s)
    assert s.was_run
    assert b.run_time > 0


def test_no_subject() -> None:
    with pytest.raises(RuntimeError):
        with Benchmark():
            pass  # Just need to exit the context manager
