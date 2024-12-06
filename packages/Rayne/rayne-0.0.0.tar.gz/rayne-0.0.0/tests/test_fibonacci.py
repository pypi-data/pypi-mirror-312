"""Unit tests for the Fibonacci example functions."""

# pylint: disable=missing-function-docstring

import pytest
from docs.fibonacci import closed_form, recursive

TEST_CASES = [
    (0, 0),
    (1, 1),
    (2, 1),
    (3, 2),
    (4, 3),
    (5, 5),
    (6, 8),
    (7, 13),
    (8, 21),
    (9, 34),
    (10, 55),
    (11, 89),
    (12, 144),
    (13, 233),
    (14, 377),
    (15, 610),
    (16, 987),
    (17, 1597),
    (18, 2584),
    (19, 4181),
]


@pytest.mark.parametrize("n,expected", TEST_CASES)
def test_recursive(n: int, expected: int) -> None:
    assert recursive(n) == expected


@pytest.mark.parametrize("n,expected", TEST_CASES)
def test_closed_form(n: int, expected: int) -> None:
    assert closed_form(n) == expected
