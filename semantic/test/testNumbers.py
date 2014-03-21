import unittest
from semantic.numbers import NumberService


class TestNumbers(unittest.TestCase):

    def compareNumbers(self, input, target):
        service = NumberService()
        result = service.parse(input)
        self.assertEqual(result, target)

    #
    # Float tests
    #

    def testFloatFracSpecial(self):
        input = "two and a quarter"
        self.compareNumbers(input, 2.25)

    def testFloatFrac(self):
        input = "two and two fifths"
        self.compareNumbers(input, 2.4)

    def testTwoAnds(self):
        input = "twelve thousand and eleven and one third"
        self.compareNumbers(input, 12011 + 1.0 / 3)

    def testFloatPoint(self):
        input = "five hundred and ten point one five"
        self.compareNumbers(input, 510.15)

    #
    # Integer tests
    #

    def testBigInt(self):
        input = "a hundred and fifty six thousand two hundred and twelve"
        self.compareNumbers(input, 156212)

    def testInt(self):
        input = "fifty one million and eleven"
        self.compareNumbers(input, 51000011)

    #
    # Readability tests
    #

    def testFloatCutoff(self):
        input = "five point one three seven seven seven seven seven"
        self.assertEqual(NumberService.parseMagnitude(input), '5.14')

    def testScientific(self):
        input = 5e-05
        self.assertEqual(NumberService.parseMagnitude(input),
                         '5 times ten to the negative 5')


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNumbers)
    unittest.TextTestRunner(verbosity=2).run(suite)
