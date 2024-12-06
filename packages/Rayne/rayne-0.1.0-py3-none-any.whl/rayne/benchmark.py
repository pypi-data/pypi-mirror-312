"""Provide micro benchmarking functionality"""

import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional


@dataclass
class BenchmarkResults:
    """Benchmark name and associated run times."""

    name: str
    run_times: List[int]


class Benchmark:
    """
    Create and run a microbenchmark.

    Use this class as a context manager. Create the :py:class:`Benchmark` and set the test subject
    with :py:meth:`set_user_code`. Rayne automatically measures and prints the test subject's
    execution time when the context manager exits.

    .. code-block:: python

       with Benchmark() as benchmark:
           benchmark.set_user_code(fibonacci, n=10)

    Attributes:
        name: Rayne assigns a name to each :py:class:`Benchmark`. Rayne uses the name in the output
            to differentiate multiple benchmarks within a single benchmarking script. The default
            name is the string representation of the test subject.

            >>> with Benchmark() as benchmark:
            >>>     benchmark.set_user_code(fibonacci, n=10)
            >>> print(benchmark.name)
            fibonacci

            You can assign a custom name to the :py:class:`Benchmark`.

            .. tab:: Initialization

               >>> with Benchmark(name="Recursive") as benchmark:
               >>>     benchmark.set_user_code(fibonacci, n=10)
               >>> print(benchmark.name)
               Recursive

            .. tab:: Post Initialization

               >>> with Benchmark() as benchmark:
               >>>     benchmark.name = "Recursive"
               >>>     benchmark.set_user_code(fibonacci, n=10)
               >>> print(benchmark.name)
               Recursive

        runs: Rayne runs the test subject several times to build a statistical model of the
            execution time. The :py:attr:`runs` attribute controls how many times Rayne runs the
            test subject. You can modify this value before the :py:class:`Benchmark` context
            manager exits. For example, to run the test subject 2000 times:

            .. tab:: Initialization

               .. code-block:: python

                  with Benchmark(runs=2000) as benchmark:
                      benchmark.subject = fibonacci

            .. tab:: Post Initialization

               .. code-block:: python

                   with Benchmark() as benchmark:
                       benchmark.runs = 2000
                       benchmark.subject = fibonacci
    """

    def __init__(self, name: Optional[str] = None, runs: int = 1000):
        self.name = name
        self.runs = runs
        self.__fut: Optional[Callable] = None  # fut -> function under test
        self.__fut_args: Dict[str, Any]
        self.__run_times: List[int] = []
        self.__clock_latency = 0

    def set_user_code(self, function, **kwargs):
        """
        Set the user code to benchmark.

        Args:
            function (Callable): The benchmark measures the execution time of this function.
            kwargs: The benchmark passes these arguments to ``function``.
        """
        self.__fut = function
        self.__fut_args = kwargs
        if not self.name:
            self.name = function.__name__

    @property
    def run_time(self) -> float:
        """The average execution time, in nanoseconds, of the subject function."""
        if not self.__run_times:
            raise RuntimeError("No user code was measured.")
        return sum(self.__run_times) // self.runs

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.__fut is None:
            raise RuntimeError("No user code was specified to measure.")
        self.__measure_clock_latency()
        self.__warm_up()
        self.__run_benchmark()
        print(f"{self.name}: {self.run_time} ns")
        return True

    def __measure_clock_latency(self):
        """
        Measure the clock latency

        It takes time to call time.perf_counter_ns(). A benchmark should not include that time
        within; it's not part of executing the function under test. This function measures the
        latency the same number of times as the benchmark runs, and stores the floor of the mean
        latency. Later, the benchmark will subtract this mean latency from each timing measurement.
        """
        total_latency = 0
        for _ in range(0, self.runs):
            start_time = time.perf_counter_ns()
            end_time = time.perf_counter_ns()
            total_latency += end_time - start_time
        self.__clock_latency = total_latency // self.runs

    def __warm_up(self):
        self.__fut(**self.__fut_args)

    def __run_benchmark(self):
        self.__run_times = [0 for _ in range(0, self.runs)]
        for i in range(0, self.runs):
            start_time = time.perf_counter_ns()
            self.__fut(**self.__fut_args)
            end_time = time.perf_counter_ns()
            self.__run_times[i] = max(end_time - start_time - self.__clock_latency, 0)
