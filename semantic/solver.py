import re
from math import sqrt, sin, cos, log, tan, acos, asin, atan, e, pi
from operator import add, sub, div, mul, pow
from numbers import NumberService


class MathService(object):

    __constants__ = {
        'e': e,
        'E': e,
        'EE': e,
        'pi': pi,
        'pie': pi
    }

    __unaryOperators__ = {
        'log': log,
        'sine': sin,
        'sin': sin,
        'cosine': cos,
        'cos': cos,
        'tan': tan,
        'tangent': tan,
        'arcsine': asin,
        'arcsin': asin,
        'asin': asin,
        'arccosine': acos,
        'arccos': acos,
        'acos': acos,
        'arctanget': atan,
        'arctan': atan,
        'atan': atan,
        'sqrt': sqrt
    }

    __binaryOperators__ = {
        'plus': add,
        'add': add,
        'sum': add,
        'minus': sub,
        'sub': sub,
        'subtract': sub,
        'less': sub,
        'over': div,
        'divide': div,
        'times': mul,
        'multiply': mul,
        'to': pow
    }

    @staticmethod
    def _applyBinary(a, b, op):
        a = float(a)
        b = float(b)
        return op(a, b)

    @staticmethod
    def _applyUnary(a, op):
        a = float(a)
        return op(a)

    @staticmethod
    def _preprocess(input):
        """Revise wording to match canonical and expected forms."""
        input = re.sub(r'(\b)a(\b)', r'\g<1>one\g<2>', input)
        input = re.sub(r'to the (.*) power', r'to \g<1>', input)
        input = re.sub(r'to the (.*?)(\b)', r'to \g<1>\g<2>', input)
        input = re.sub(r'log of', r'log', input)
        input = re.sub(r'(square )?root( of)?', r'sqrt', input)
        input = re.sub(r'squared', r'to two', input)
        input = re.sub(r'cubed', r'to three', input)
        input = re.sub(r'divided?( by)?', r'divide', input)
        input = re.sub(r'(\b)over(\b)', r'\g<1>divide\g<2>', input)
        input = re.sub(r'(\b)EE(\b)', r'\g<1>e\g<2>', input)
        input = re.sub(r'(\b)E(\b)', r'\g<1>e\g<2>', input)
        input = re.sub(r'(\b)pie(\b)', r'\g<1>pi\g<2>', input)
        input = re.sub(r'(\b)PI(\b)', r'\g<1>pi\g<2>', input)

        def findImplicitMultiplications(input):
            """Replace omitted 'times' references."""

            def findConstantMultiplications(input):
                split = input.split(' ')
                revision = ""

                converter = NumberService()
                for i, w in enumerate(split):
                    if i > 0 and w in MathService.__constants__:
                        if converter.isValid(split[i - 1]):
                            revision += " times"
                    if not revision:
                        revision = w
                    else:
                        revision += " " + w

                return revision

            def findUnaryMultiplications(input):
                split = input.split(' ')
                revision = ""

                for i, w in enumerate(split):
                    if i > 0 and w in MathService.__unaryOperators__:
                        last_op = split[i - 1]

                        binary = last_op in MathService.__binaryOperators__
                        unary = last_op in MathService.__unaryOperators__

                        if last_op and not (binary or unary):
                            revision += " times"
                    if not revision:
                        revision = w
                    else:
                        revision += " " + w

                return revision

            return findUnaryMultiplications(findConstantMultiplications(input))

        return findImplicitMultiplications(input)

    @staticmethod
    def _calculate(numbers, symbols):
        """Calculates a final value given a set of numbers and symbols."""
        if len(numbers) is 1:
            return numbers[0]

        precedence = [[pow], [mul, div], [add, sub]]

        # Find most important operation
        for op_group in precedence:
            for i, op in enumerate(symbols):
                if op in op_group:
                    # Apply operation
                    a = numbers[i]
                    b = numbers[i + 1]
                    result = MathService._applyBinary(a, b, op)
                    new_numbers = numbers[:i] + [result] + numbers[i + 2:]
                    new_symbols = symbols[:i] + symbols[i + 1:]

                    return MathService._calculate(new_numbers, new_symbols)

    def parseEquation(self, input):
        """Solves the equation specified by the input string.

        Args:
            input (str): An equation, specified in words, containing some
                combination of numbers, binary, and unary operations.

        Returns:
            The floating-point result of carrying out the computation.
        """
        input = MathService._preprocess(input)
        split = input.split(' ')

        # Recursive call on unary operators
        for i, w in enumerate(split):
            if w in self.__unaryOperators__:
                op = self.__unaryOperators__[w]

                # Split equation into halves
                eq1 = ' '.join(split[:i])
                eq2 = ' '.join(split[i + 1:])

                # Calculate second half
                result = MathService._applyUnary(self.parseEquation(eq2), op)

                return self.parseEquation(eq1 + " " + str(result))

        def extractNumbersAndSymbols(input):
            numbers = []
            symbols = []

            # Divide into values (numbers), operators (symbols)
            next_number = ""
            for w in input.split(' '):
                if w in self.__binaryOperators__:
                    symbols.append(self.__binaryOperators__[w])

                    if next_number:
                        numbers.append(next_number)
                        next_number = ""

                else:
                    if next_number:
                        next_number += " "
                    next_number += w

            if next_number:
                numbers.append(next_number)

            # Cast numbers from words to integers
            def convert(n):
                if n in self.__constants__:
                    return self.__constants__[n]

                converter = NumberService()
                return converter.parse(n)

            numbers = [convert(n) for n in numbers]

            return numbers, symbols

        numbers, symbols = extractNumbersAndSymbols(input)

        return MathService._calculate(numbers, symbols)


def parseEquation(self, input):
    """Solves the equation specified by the input string. This is a convenience
    method which would only be used if you'd rather not initialize a
    NumberService object.

    Args:
        input (str): An equation, specified in words, containing some
            combination of numbers, binary, and unary operations.

    Returns:
        The floating-point result of carrying out the computation.
    """

    service = NumberService()
    return service.parseEquation(input)
