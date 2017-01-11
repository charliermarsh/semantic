import unittest
import quantities as pq
from semantic.units import ConversionService


class TestConversion(unittest.TestCase):

    def compareConversion(self, inp, target):
        service = ConversionService()
        result = service.convert(inp)
        self.assertEqual(result.magnitude, target.magnitude)
        self.assertEqual(result.units, target.units)

    def testSimple(self):
        inp = "55.12 kilograms to pounds"
        target = pq.Quantity(55.12, "kg")
        target.units = "pounds"
        self.compareConversion(inp, target)

    def testPer(self):
        inp = "fifty one point two kilograms per meter to pounds per foot"
        target = pq.Quantity(51.2, "kg / meter")
        target.units = "pounds / ft"
        self.compareConversion(inp, target)

    def testReadability(self):
        inp = "convert 0.000013 inches to centimeters"
        target = pq.Quantity(0.000013, "inches")
        target.units = "cm"

        # Correctness of conversion
        self.compareConversion(inp, target)

        # Correctness of representation
        service = ConversionService()
        self.assertEqual(service.parseUnits(inp),
                         "3.3 times ten to the negative 5 cm")

    def testFloat(self):
        inp = "what is eleven and two thirds pounds converted to kilograms"
        target = pq.Quantity(11 + 2.0 / 3, "pounds")
        target.units = "kg"
        self.compareConversion(inp, target)

    def testExtraction(self):
        inp = "I want three pounds of eggs and two inches per squared foot"
        service = ConversionService()
        units = service.extractUnits(inp)
        self.assertEqual(units, ['pounds', 'inches / foot^2'])

    def testExponentiation(self):
        service = ConversionService()
        inp = "I want two squared meters"
        units = service.extractUnits(inp)
        self.assertEqual(units, ['meters^2'])

        inp = "I want two square meters"
        units = service.extractUnits(inp)
        self.assertEqual(units, ['meters^2'])

        inp = "I want two sq meters"
        units = service.extractUnits(inp)
        self.assertEqual(units, ['meters^2'])

        inp = "I want two cubic meters"
        units = service.extractUnits(inp)
        self.assertEqual(units, ['meters^3'])

        inp = "I want two meters cubed"
        units = service.extractUnits(inp)
        self.assertEqual(units, ['meters^3'])

        inp = "I want two meters to the fifth power"
        units = service.extractUnits(inp)
        self.assertEqual(units, ['meters^5'])

        inp = "I want two meters to the fifth"
        units = service.extractUnits(inp)
        self.assertEqual(units, ['meters^5'])

    def testComplex(self):
        inp = "Seven and a half pounds per square ft to kg per meter squared"
        target = pq.Quantity(7.5, "lb/ft**2")
        target.units = "kg/m**2"
        self.compareConversion(inp, target)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestConversion)
    unittest.TextTestRunner(verbosity=2).run(suite)
