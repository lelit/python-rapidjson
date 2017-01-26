==================
 python-rapidjson
==================

Python wrapper around RapidJSON
===============================

RapidJSON_ is an extremely fast C++ JSON serialization library.

We do not support legacy Python versions, you will need to upgrade to Python 3
to use this library.


Getting Started
---------------

First install ``python-rapidjson``:

.. code-block:: bash

    $ pip install python-rapidjson

RapidJSON tries to be compatible with the standard library ``json`` module so
it should be a drop in replacement. Basic usage looks like this:

.. code-block:: python

    >>> import rapidjson
    >>> data = {'foo': 100, 'bar': 'baz'}
    >>> rapidjson.dumps(data)
    '{"bar":"baz","foo":100}'
    >>> rapidjson.loads('{"bar":"baz","foo":100}')
    {'bar': 'baz', 'foo': 100}

If you want to install the development version (maybe to contribute fixes or
enhancements) you may clone the repository:

.. code-block:: bash

    $ git clone --recursive https://github.com/python-rapidjson/python-rapidjson.git

.. note:: The ``--recursive`` option is needed because we use a *submodule* to
          include RapidJSON_ sources. Alternatively you can do a plain
          ``clone`` immediately followed by a ``git submodule update --init``.


Performance
-----------

``python-rapidjson`` tries to be as performant as possible while staying
compatible with the ``json`` module.

The following tables show a comparison between this module and other libraries
with different data sets.  Last row (“overall”) is the total time taken by all
the benchmarks.

Each number show the factor between the time taken by each contender and
``python-rapidjson`` (in other words, they are *normalized* against a value of
1.0 for ``python-rapidjson``): the lower the number, the speedier the
contender.

In **bold** the winner.

Serialization
~~~~~~~~~~~~~

+-----------------------+-----------------+-----------------+-----------------+-----------------+-----------------+
|       serialize       |   native [1]_   |   ujson [2]_    | simplejson [3]_ |   stdlib [4]_   |    yajl [5]_    |
+=======================+=================+=================+=================+=================+=================+
|    100 arrays dict    |    **0.67**     |      1.15       |      5.65       |      2.79       |      1.61       |
+-----------------------+-----------------+-----------------+-----------------+-----------------+-----------------+
|    100 dicts array    |    **0.77**     |      1.04       |      6.50       |      2.62       |      1.53       |
+-----------------------+-----------------+-----------------+-----------------+-----------------+-----------------+
|  **256 Trues array**  |      1.17       |      1.36       |      2.48       |      2.12       |      1.14       |
+-----------------------+-----------------+-----------------+-----------------+-----------------+-----------------+
|    256 ascii array    |      1.03       |    **0.74**     |      1.63       |      1.42       |      1.60       |
+-----------------------+-----------------+-----------------+-----------------+-----------------+-----------------+
| **256 doubles array** |      1.05       |      6.07       |      7.31       |      6.17       |      3.47       |
+-----------------------+-----------------+-----------------+-----------------+-----------------+-----------------+
|   256 unicode array   |      0.91       |      0.55       |      0.70       |      0.76       |    **0.45**     |
+-----------------------+-----------------+-----------------+-----------------+-----------------+-----------------+
|    complex object     |    **0.82**     |      1.87       |      4.80       |      3.07       |      2.41       |
+-----------------------+-----------------+-----------------+-----------------+-----------------+-----------------+
|   composite object    |    **0.69**     |      0.93       |      2.92       |      1.91       |      1.85       |
+-----------------------+-----------------+-----------------+-----------------+-----------------+-----------------+
|        overall        |    **0.67**     |      1.15       |      5.63       |      2.78       |      1.61       |
+-----------------------+-----------------+-----------------+-----------------+-----------------+-----------------+

.. [1] rapidjson with ``native_numbers=True``
.. [2] `ujson 1.35 <https://pypi.python.org/pypi/ujson/1.35>`__
.. [3] `simplejson 3.10.0 <https://pypi.python.org/pypi/simplejson/3.10.0>`__
.. [4] Python 3.6 standard library
.. [5] `yajl 0.3.5 <https://pypi.python.org/pypi/yajl/0.3.5>`__


Deserialization
~~~~~~~~~~~~~~~

+-----------------------+------------+------------+------------+------------+------------+
|      deserialize      |   native   |   ujson    | simplejson |   stdlib   |    yajl    |
+=======================+============+============+============+============+============+
|    100 arrays dict    |  **0.89**  |    0.90    |    1.38    |    1.03    |    1.15    |
+-----------------------+------------+------------+------------+------------+------------+
|    100 dicts array    |    0.90    |  **0.88**  |    1.96    |    1.32    |    1.22    |
+-----------------------+------------+------------+------------+------------+------------+
|  **256 Trues array**  |    1.26    |    1.30    |    2.06    |    1.93    |    2.00    |
+-----------------------+------------+------------+------------+------------+------------+
|  **256 ascii array**  |    1.01    |    1.36    |    1.12    |    1.18    |    1.52    |
+-----------------------+------------+------------+------------+------------+------------+
|   256 doubles array   |  **0.20**  |    0.44    |    0.97    |    0.94    |    0.45    |
+-----------------------+------------+------------+------------+------------+------------+
|   256 unicode array   |    1.12    |  **0.90**  |    4.79    |    5.08    |    2.21    |
+-----------------------+------------+------------+------------+------------+------------+
|    complex object     |  **0.78**  |    0.86    |    1.36    |    1.08    |    1.16    |
+-----------------------+------------+------------+------------+------------+------------+
|   composite object    |    0.84    |  **0.80**  |    1.88    |    1.38    |    1.19    |
+-----------------------+------------+------------+------------+------------+------------+
|        overall        |  **0.89**  |    0.90    |    1.39    |    1.04    |    1.15    |
+-----------------------+------------+------------+------------+------------+------------+


DIY
~~~

To run these tests yourself, clone the repo and run:

.. code-block:: bash

   $ tox -e py34 -- -m benchmark --compare-other-engines

Without the option ``--compare-other-engines`` it will focus only on
``RapidJSON``.  This is particularly handy coupled with the `compare past
runs`__ functionality of ``pytest-benchmark``:

.. code-block:: bash

   $ tox -e py34 -- -m benchmark --benchmark-autosave
   # hack, hack, hack!
   $ tox -e py34 -- -m benchmark --benchmark-compare=0001

   ----------------------- benchmark 'deserialize': 18 tests ------------------------
   Name (time in us)                                                            Min…
   ----------------------------------------------------------------------------------
   test_loads[rapidjson-256 Trues array] (NOW)                         5.2320 (1.0)…
   test_loads[rapidjson-256 Trues array] (0001)                        5.4180 (1.04)…
   …

To reproduce the tables above, use the option ``--benchmark-json`` so that the
the results are written in the specified filename the run the
``benchmark-tables.py`` script giving that filename as the only argument:

.. code-block:: bash

   $ tox -e py36 -- -m benchmark --compare-other-engines --benchmark-json=comparison.json
   $ python3 benchmark-tables.py comparison.json


__ http://pytest-benchmark.readthedocs.org/en/latest/comparing.html


Incompatibility
---------------

Here are things in the standard ``json`` library supports that we have decided
not to support:

* ``separators`` argument. This is mostly used for pretty printing and not
  supported by ``RapidJSON`` so it isn't a high priority. We do support
  ``indent`` kwarg that would get you nice looking JSON anyways.

* Coercing keys when dumping. ``json`` will turn ``True`` into ``'True'`` if
  you dump it out but when you load it back in it'll still be a string. We
  want the dump and load to return the exact same objects so we have decided
  not to do this coercing.

.. _RapidJSON: https://github.com/miloyip/rapidjson
