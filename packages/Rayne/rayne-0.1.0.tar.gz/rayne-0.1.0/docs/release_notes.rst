Release Notes
=============

0.1.0
-----

New Features
............

#. Add the :py:class:`~benchmark.Benchmark` class (:issue:`2`).

   Developers can write a micro-benchmark as a context manager.
   The manager benchmarks the user's function-under-test automatically during context exit.
#. Add the :py:class:`~benchmark.BenchmarkResults` class (:issue:`10`).

   Encapsulate benchmark results for later use by reporters.
#. Warm up the cache before benchmarking (:issue:`23`).

   Run the function-under-test before benchmarking.
   This loads code and data into the cache before measuring.
