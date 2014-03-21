import unittest
import quantities as pq
from semantic.units import ConversionService


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

    def testExtraction(self):
        input = "I want three pounds of eggs and two inches per squared foot"
        service = ConversionService()
        units = service.extractUnits(input)
        self.assertEqual(units, ['pounds', 'inches / foot^2'])

    def testExponentiation(self):
        service = ConversionService()
        input = "I want two squared meters"
        units = service.extractUnits(input)
        self.assertEqual(units, ['meters^2'])

        input = "I want two square meters"
        units = service.extractUnits(input)
        self.assertEqual(units, ['meters^2'])

        input = "I want two sq meters"
        units = service.extractUnits(input)
        self.assertEqual(units, ['meters^2'])

        input = "I want two cubic meters"
        units = service.extractUnits(input)
        self.assertEqual(units, ['meters^3'])

        input = "I want two meters cubed"
        units = service.extractUnits(input)
        self.assertEqual(units, ['meters^3'])

        input = "I want two meters to the fifth power"
        units = service.extractUnits(input)
        self.assertEqual(units, ['meters^5'])

        input = "I want two meters to the fifth"
        units = service.extractUnits(input)
        self.assertEqual(units, ['meters^5'])

    def testComplex(self):
        input = "Seven and a half pounds per square ft to kg per meter squared"
        target = pq.Quantity(7.5, "lb/ft**2")
        target.units = "kg/m**2"
        self.compareConversion(input, target)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestConversion)
    unittest.TextTestRunner(verbosity=2).run(suite)
