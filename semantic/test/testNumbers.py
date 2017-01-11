import unittest
from semantic.numbers import NumberService


class TestNumbers(unittest.TestCase):

    def compareNumbers(self, inp, target):
        service = NumberService()
        result = service.parse(inp)
        self.assertEqual(result, target)

    #
    # Float tests
    #

    def testFloatFracSpecial(self):
        inp = "two and a quarter"
        self.compareNumbers(inp, 2.25)

    def testFloatFrac(self):
        inp = "two and two fifths"
        self.compareNumbers(inp, 2.4)

    def testTwoAnds(self):
        inp = "twelve thousand and eleven and one third"
        self.compareNumbers(inp, 12011 + 1.0 / 3)

    def testFloatPoint(self):
        inp = "five hundred and ten point one five"
        self.compareNumbers(inp, 510.15)

    #
    # Integer tests
    #

    def testBigInt(self):
        inp = "a hundred and fifty six thousand two hundred and twelve"
        self.compareNumbers(inp, 156212)

    def testInt(self):
        inp = "fifty one million and eleven"
        self.compareNumbers(inp, 51000011)

    #
    # Readability tests
    #

    def testFloatCutoff(self):
        inp = "five point one three seven seven seven seven seven"
        self.assertEqual(NumberService.parseMagnitude(inp), '5.14')

    def testScientific(self):
        inp = 5e-05
        self.assertEqual(NumberService.parseMagnitude(inp),
                         '5 times ten to the negative 5')


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNumbers)
    unittest.TextTestRunner(verbosity=2).run(suite)
