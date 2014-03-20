===========
Intent
===========

Intent is a Python library for extracting semantic information from text, including dates, numbers, mathematical equations, and unit conversions.

For each of these four semantic types, Intent provides a service module. Typical usage often looks like this::

    #!/usr/bin/env python
    from intent.dates import DateService

    service = DateService()
    date = service.extractDate("On March 3 at 12:15pm...")
    ...

Features
========

Intent contains four main modules, each of which corresponds to a different semantic extractor.

Dates (*date.py*)
-----------------

Useful for:

* Extracting relative (e.g., "a week from today") and absolute (e.g., "December 11, 2013") dates from text snippets.
* Converting date objects to human-ready phrasing.

Numbers (*number.py*)
---------------------

Useful for:

* Extracting numbers (integers or floats) from text snippets.
* Converting numbers to human-readable strings.

Example usage::

    #!/usr/bin/env python
    from intent.numbers import NumberService

    service = NumberService()

    print service.parse("Two hundred and six")
    # 206

    print service.parse("Five point one five")
    # 5.15

    print service.parse("Eleven and two thirds")
    # 11.666666666666666

    print service.parseMagnitude("7e-05")
    # "seven to the negative five"


Math (*solver.py*)
------------------

Useful for performing mathematical operations expressed as words.

Example usage::

    #!/usr/bin/env python
    from intent.solver import MathService

    service = MathService()

    print service.parseEquation("Log one hundred and ten")
    # 4.70048

Units (*units.py*)
------------------

Useful for converting between units expressed as words.

Example usage::

    #!/usr/bin/env python
    from intent.solver import ConversionService

    service = ConversionService()

    print service.convert("Seven and a half kilograms to pounds")
    # (16.534, 'lbs')

    print service.convert("Seven and a half pounds per square foot to kilograms per meter squared")
    # (36.618, 'kg/m**2')


Testing
=======

The test suite (*test.py*) contains tons of examples and use-cases for each of the four modules.

Requirements
============

The Dates, Numbers, and Math modules can run in isolation (i.e., without any dependencies), while the Units module requires `quantities <https://pypi.python.org/pypi/quantities>`_ and `Numpy <http://www.numpy.org>`_.

License
=======

MIT © `Charles Marsh <http://www.princeton.edu/~crmarsh>`_