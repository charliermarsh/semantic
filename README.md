# intent

A Python library for extracting semantic information from text, such as dates and numbers.

# Features

Four main modules, each of which corresponds to a different semantic extractor.

## Dates (_date.py_)
- Extracting relative (e.g., "a week from today") and absolute (e.g., "December 11, 2013") dates from text snippets.
- Converting date objects to human-ready phrasing.

## Numbers (_number.py_)
- Extracting numbers (integers or floats) from text snippets.
	- E.g.: From "Two hundred and six" to 206.
	- E.g.: From "Five point one five" to 5.15.
	- E.g.: From "Eleven and two thirds" to 11.666666666666666.
- Converting numbers to human-readable strings.
	- E.g.: From "7e-05" to "seven to the negative five".

## Math (_solver.py_)
- Performing mathematical operations expressed as words.
	- E.g.: From "Log one hundred and ten" to Log(110) = 4.70048.

## Units (_units.py_)
- Converting between units expressed as words.
	- E.g.: From "Seven and a half kilograms to pounds" to 16.5347.
- Converting units to human-readable strings.
	- E.g., 


# Running

The test suite (_test.py_) contains tons of examples and use-cases for each of the four modules.

The Dates, Numbers, and Math modules can run in isolation (i.e., have no dependencies), while the Units module requires [quantities](https://pypi.python.org/pypi/quantities) and [Numpy](http://www.numpy.org).