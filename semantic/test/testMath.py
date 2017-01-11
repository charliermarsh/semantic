from math import log, sin, sqrt, e, pi
import unittest
from semantic.solver import MathService


class TestMath(unittest.TestCase):

    def compareSolution(self, inp, target):
        service = MathService()
        result = service.parseEquation(inp)

        def close(x, y, EPSILON=1e-5):
            return abs(x - y) < EPSILON
        self.assertTrue(close(result, target))

    def testAddition(self):
        inp = "five plus twenty one and a fifth"
        self.compareSolution(inp, 5 + 21.2)

    def testUnary(self):
        inp = "log sin eleven hundred"
        self.compareSolution(inp, log(sin(1100)))

    def testPower(self):
        inp = "fifteen to the eleven point five power"
        self.compareSolution(inp, 15 ** 11.5)

    def testDividedBy(self):
        inp = "3 divided by sqrt twenty five"
        self.compareSolution(inp, 3 / sqrt(25))

    def testComplex(self):
        inp = "one and a quarter divided by two point two to the sixth power"
        self.compareSolution(inp, 1.25 / (2.2 ** 6))

    def testConstants(self):
        inp = "E plus sqrt one plus tangent two times pi"
        self.compareSolution(inp, e + 1)

    def testImplicitMultiplication(self):
        inp = "eleven plus five log two hundred and six"
        self.compareSolution(inp, 11 + 5 * log(206))

    def testImplicitConstantMultiplication(self):
        inp = "two pie"
        self.compareSolution(inp, 2 * pi)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMath)
    unittest.TextTestRunner(verbosity=2).run(suite)
