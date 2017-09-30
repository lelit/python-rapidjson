.. -*- coding: utf-8 -*-
.. :Project:   python-rapidjson -- load function documentation
.. :Author:    Lele Gaifax <lele@metapensiero.it>
.. :License:   MIT License
.. :Copyright: © 2017 Lele Gaifax
..

=================
 load() function
=================

.. module:: rapidjson

.. testsetup::

   from io import StringIO
   from rapidjson import load

.. function:: load(stream, object_hook=None, number_mode=None, datetime_mode=None, \
                   uuid_mode=None, parse_mode=None, allow_nan=True)

   Decode the given Python file-like `stream` containing a ``JSON`` formatted value
   into Python object.

   :param stream: a file-like object
   :param callable object_hook: an optional function that will be called with the result
                                of any object literal decoded (a :class:`dict`) and should
                                return the value to use instead of the :class:`dict`
   :param int number_mode: enable particular behaviors in handling numbers
   :param int datetime_mode: how should :class:`datetime` and :class:`date` instances be
                             handled
   :param int uuid_mode: how should :class:`UUID` instances be handled
   :param int parse_mode: whether the parser should allow non-standard JSON extensions
   :param bool allow_nan: *compatibility* flag equivalent to ``number_mode=NM_NAN``
   :returns: An equivalent Python object.

   The function has the same behaviour as :func:`loads()`, except for the kind of the
   first argument that is expected to be file-like object instead of a string:

   .. doctest::

      >>> stream = StringIO('["string", {"kind": "object"}, 3.14159]')
      >>> load(stream)
      ["string", {"kind": "object"}, 3.14159]

   Consult the :func:`loads()` documentation for details on all other arguments.
