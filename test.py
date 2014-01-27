import unittest
from dates import DateService
from numbers import NumberService
from solver import MathService
from units import ConversionService
import quantities as pq
import datetime
from math import log, sin, sqrt, e, pi


class TestConversion(unittest.TestCase):

    def compareConversion(self, input, target):
        service = ConversionService()
        result = service.convert(input)
        self.assertEqual(result.magnitude, target.magnitude)
        self.assertEqual(result.units, target.units)

    def testSimple(self):
        input = "55.12 kilograms to pounds"
        target = pq.Quantity(55.12, "kg")
        target.units = "pounds"
        self.compareConversion(input, target)

    def testPer(self):
        input = "fifty one point two kilograms per meter to pounds per foot"
        target = pq.Quantity(51.2, "kg / meter")
        target.units = "pounds / ft"
        self.compareConversion(input, target)

    def testReadability(self):
        input = "convert 0.000013 inches to centimeters"
        target = pq.Quantity(0.000013, "inches")
        target.units = "cm"

        # Correctness of conversion
        self.compareConversion(input, target)

        # Correctness of representation
        service = ConversionService()
        self.assertEqual(service.parseUnits(input),
                         "3.3 times ten to the negative 5 cm")

    def testFloat(self):
        input = "what is eleven and two thirds pounds converted to kilograms"
        target = pq.Quantity(11 + 2.0 / 3, "pounds")
        target.units = "kg"
        self.compareConversion(input, target)


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


class TestDate(unittest.TestCase):

    def compareDate(self, input, target):
        service = DateService()
        result = service.parseDate(input)
        self.assertEqual(result.month, target.month)
        self.assertEqual(result.day, target.day)

    def compareTime(self, input, target):
        service = DateService()
        result = service.parseDate(input)
        self.assertEqual(result.hour, target.hour)
        self.assertEqual(result.minute, target.minute)

    #
    #  Date Tests
    #

    def testExactWords(self):
        input = "Remind me on January Twenty Sixth"
        target = datetime.datetime(2014, 1, 26)
        self.compareDate(input, target)

    def testExactWordsDash(self):
        input = "Remind me on January Twenty-Sixth"
        target = datetime.datetime(2014, 1, 26)
        self.compareDate(input, target)

    def testExactNums(self):
        input = "Remind me on January 26"
        target = datetime.datetime(2014, 1, 26)
        self.compareDate(input, target)

    def testWeekFromExact(self):
        input = "Do x y and z a week from January 26"
        target = datetime.datetime(2014, 1, 26) + datetime.timedelta(days=7)
        self.compareDate(input, target)

    def testNextFriday(self):
        input = "Next Friday, go to the grocery store"
        friday = 4
        num_days_away = (friday - datetime.datetime.today().weekday()) % 7
        target = datetime.datetime.today() + \
            datetime.timedelta(
                days=7 + num_days_away)
        self.compareDate(input, target)

    def testAmbiguousNext(self):
        input = "The next event will take place on Friday"
        friday = 4
        num_days_away = (friday - datetime.datetime.today().weekday()) % 7
        target = datetime.datetime.today() + \
            datetime.timedelta(
                days=num_days_away)
        self.compareDate(input, target)

    def testTomorrow(self):
        input = "Tomorrow morning, go to the grocery store"
        target = datetime.datetime.today() + datetime.timedelta(days=1)
        self.compareDate(input, target)

    def testToday(self):
        input = "Send me an email some time today if you can"
        target = datetime.datetime.today()
        self.compareDate(input, target)

    def testThis(self):
        input = "This morning, I went to the gym"
        target = datetime.datetime.today()
        self.compareDate(input, target)

    def testIllegalDate(self):
        input = "I have a meeting on February 29 at 12:15pm"
        self.assertRaises(ValueError, lambda: DateService().parseDate(input))

    def testMultiple(self):
        input = "Tomorrow, I'll schedule the meeting for June 9 at 1:30pm"
        target = datetime.datetime.today() + datetime.timedelta(days=1)
        self.compareDate(input, target)

    #
    #  Time Tests
    #

    def testExactTime(self):
        input = "Let's go to the park at 12:51pm tomorrow"
        tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
        target = datetime.datetime(
            tomorrow.year, tomorrow.month, tomorrow.day, 12, 51)
        self.compareTime(input, target)

if __name__ == "__main__":
    for runner in (TestConversion, TestMath, TestNumbers, TestDate):
        suite = unittest.TestLoader().loadTestsFromTestCase(runner)
        unittest.TextTestRunner(verbosity=2).run(suite)
