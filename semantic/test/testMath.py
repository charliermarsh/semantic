from math import log, sin, sqrt, e, pi
import unittest
from semantic.solver import MathService


class TestMath(unittest.TestCase):

    def compareSolution(self, input, target):
        service = MathService()
        result = service.parseEquation(input)

        def close(x, y, EPSILON=1e-5):
            return abs(x - y) < EPSILON
        self.assertTrue(close(result, target))

    def testAddition(self):
        input = "five plus twenty one and a fifth"
        self.compareSolution(input, 5 + 21.2)

    def testUnary(self):
        input = "log sin eleven hundred"
        self.compareSolution(input, log(sin(1100)))

    def testPower(self):
        input = "fifteen to the eleven point five power"
        self.compareSolution(input, 15 ** 11.5)

    def testDividedBy(self):
        input = "3 divided by sqrt twenty five"
        self.compareSolution(input, 3 / sqrt(25))

    def testComplex(self):
        input = "one and a quarter divided by two point two to the sixth power"
        self.compareSolution(input, 1.25 / (2.2 ** 6))

    def testConstants(self):
        input = "E plus sqrt one plus tangent two times pi"
        self.compareSolution(input, e + 1)

    def testImplicitMultiplication(self):
        input = "eleven plus five log two hundred and six"
        self.compareSolution(input, 11 + 5 * log(206))

    def testImplicitConstantMultiplication(self):
        input = "two pie"
        self.compareSolution(input, 2 * pi)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMath)
    unittest.TextTestRunner(verbosity=2).run(suite)
