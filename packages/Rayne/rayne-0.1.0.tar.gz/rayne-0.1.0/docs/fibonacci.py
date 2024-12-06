"""Example use of Rayne"""

from math import sqrt
from rayne import Benchmark


def closed_form(n: int) -> int:
    """Calculate F(n) using the closed form equation."""
    phi = (1 + sqrt(5)) / 2
    psi = (1 - sqrt(5)) / 2
    return int((phi**n - psi**n) / sqrt(5))


def recursive(n: int) -> int:
    """Calculate F(n) using recursion."""
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return recursive(n - 1) + recursive(n - 2)


if __name__ == "__main__":
    with Benchmark() as benchmark:
        benchmark.set_user_code(closed_form, n=5)

    with Benchmark() as benchmark:
        benchmark.set_user_code(recursive, n=5)
