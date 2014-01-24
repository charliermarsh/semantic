# PyContext

A Python library for extracting semantic information from text, such as dates and numbers.

# Features

Four main modules, each of which corresponds to a different semantic extractor.

## Dates
- Extracting relative (e.g., "a week from today") and absolute (e.g., "December 11, 2013") dates from text snippets.
- Converting date objects to human-ready phrasing.

## Numbers
- Extracting numbers (integers or floats) from text snippets.
	- E.g.: From "Two hundred and six" to 206.
	- E.g.: From "Five point one five" to 5.15.
- Converting numbers from words to floats.
	- E.g.: From "One hundred and 20" to 120.

## Math
- Performing mathematical operations expressed as words.
	- E.g.: From "Log one hundred and ten" to Log(110) = 4.70048.

## Units
- Converting between units expressed as words
	- E.g.: From "Seven and a half kilograms to pounds" to 3.whatever.
