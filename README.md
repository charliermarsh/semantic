Semantic
========

Semantic is a Python library for extracting semantic information from text, such as dates and numbers. Full documentation is available on [PyPI](https://pythonhosted.org/semantic/), with a list of primary features and uses-cases below.

[![Build Status](https://travis-ci.org/crm416/semantic.png)](https://travis-ci.org/crm416/semantic.png)

[![PyPI version](https://badge.fury.io/py/semantic.png)](http://badge.fury.io/py/semantic)

## Installation

Installing semantic is simple:

    $ pip install semantic

## Features

Semantic consists of four main modules, each of which corresponds to a different semantic extractor. The test suite (_test.py_) contains tons of examples for each of the four modules, but some sample use-cases are described below.

### Dates (*date.py*)

Useful for:

* Extracting relative (e.g., "a week from today") and absolute (e.g., "December 11, 2013") dates from text snippets.
* Converting date objects to human-ready phrasing.

### Numbers (*number.py*)

Useful for:

* Extracting numbers (integers or floats) from text snippets.
* Converting numbers to human-readable strings.

Example usage:

    #!/usr/bin/env python
    from semantic.numbers import NumberService

    service = NumberService()

    print service.parse("Two hundred and six")
    # 206

    print service.parse("Five point one five")
    # 5.15

    print service.parse("Eleven and two thirds")
    # 11.666666666666666

    print service.parseMagnitude("7e-05")
    # "seven to the negative five"


### Math (*solver.py*)

Useful for performing mathematical operations expressed as words.

Example usage:

    #!/usr/bin/env python
    from semantic.solver import MathService

    service = MathService()

    print service.parseEquation("Log one hundred and ten")
    # 4.70048

### Units (*units.py*)

Useful for converting between units expressed as words.

Example usage:

    #!/usr/bin/env python
    from semantic.units import ConversionService

    service = ConversionService()

    print service.convert("Seven and a half kilograms to pounds")
    # (16.534, 'lbs')

    print service.convert("Seven and a half pounds per square foot to kilograms per meter squared")
    # (36.618, 'kg/m**2')

## Dependencies

The Dates, Numbers, and Math modules can run in isolation (i.e., without any dependencies), while the Units module requires [quantities](https://pypi.python.org/pypi/quantities) and [Numpy](http://www.numpy.org).

## License

MIT © [Charles Marsh](http://www.princeton.edu/~crmarsh)