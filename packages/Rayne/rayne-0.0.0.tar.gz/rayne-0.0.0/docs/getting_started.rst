Getting Started
===============

.. note::
   The commands in this tutorial are for Python 3 on Linux.
   For other platforms, adjust the commands accordingly.
   Rayne should work on any platform.

Install Rayne
-------------

Start by installing Rayne from `PyPI <https://pypi.org/project/rayne/>`_.
Add it to your requirements or pyproject file, or install it manually with

.. code-block:: bash

   pip3 install rayne

Write Your Code
---------------

.. _fibonacci.py: https://github.com/brobeson/Rayne/blob/main/docs/fibonacci.py

For this tutorial, we'll benchmark two Fibonacci implementations: a recursive function and the closed form equation. [1]_
The full code for this example is in the `repository <https://github.com/brobeson/Rayne/blob/main/docs/fibonacci.py>`_.
Rayne requires that you encapsulate your code in a ``Callable`` object.

.. literalinclude:: fibonacci.py
   :caption: User code in `fibonacci.py`_
   :lines: 7-18
   :linenos:

Write Your Benchmarks
---------------------

Rayne is designed as a context manager.
Instantiate a :py:class:`~benchmark.Benchmark` object, set the code to execute, and exit the context manager.
When the context manager exits, Rayne runs your code and measures the run time.

.. literalinclude:: fibonacci.py
   :caption: Benchmark code in `fibonacci.py`_
   :lines: 4,5,21-
   :linenos:

Run Your Benchmarks
-------------------

Run the benchmark script with Python.
By default, Rayne runs your code 1000 times.
Rayne prints the average run time in nanoseconds.

.. code-block:: bash

   $ python3 fibonacci.py 
   closed_form: 1578 ns
   recursive: 1956 ns

Next Steps
----------

#. Read the :py:class:`~benchmark.Benchmark` reference documentation

----

.. [1] https://en.wikipedia.org/wiki/Fibonacci_sequence#Closed-form_expression