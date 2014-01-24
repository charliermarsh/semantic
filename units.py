import re
import quantities as pq
from numbers import NumberService


class ConversionService(object):

    @staticmethod
    def preprocess(input):
        # 'per' --> '/'
        input = re.sub(r'\sper\s', r' / ', input)
        return input

    @staticmethod
    def parseMagnitude(m):
        """
            Parses a number m into a human-ready string representation.
            For example, crops off floats if they're too accurate.
        """

        def toDecimalPrecision(n, k):
            return float("%.*f" % (k, round(n, k)))

        # Cast to two digits of precision
        digits = 2
        magnitude = toDecimalPrecision(m, digits)

        # If value is really small, keep going
        while not magnitude:
            digits += 1
            magnitude = toDecimalPrecision(m, digits)

        # If item is less than one, go one beyond 'necessary' number of digits
        if m < 1.0:
            magnitude = toDecimalPrecision(m, digits + 1)

        # Ignore decimal accuracy if irrelevant
        if int(magnitude) == magnitude:
            magnitude = int(magnitude)

        # Adjust for scientific notation
        magString = str(magnitude)
        magString = re.sub(r'(\d)e-(\d+)',
                           '\g<1> times ten to the negative \g<2>', magString)
        magString = re.sub(r'(\d)e\+(\d+)',
                           '\g<1> times ten to the \g<2>', magString)
        magString = re.sub(r'-(\d+)', 'negative \g<1>', magString)
        magString = re.sub(r'\b0(\d+)', '\g<1>', magString)
        return magString

    def parseUnits(self, input):
        """
            Carries out some conversion (represented as a string) and
            returns the result as a human-ready string.
        """
        quantity = self.convert(input)
        units = ' '.join(str(quantity.units).split(' ')[1:])
        return ConversionService.parseMagnitude(quantity.item()) + " " + units

    def convert(self, input):
        """
            Converts a string representation of some quantity of units
            and converts it to a quantities object.
        """
        input = ConversionService.preprocess(input)

        # Collect consecutive runs of units
        def isValidUnit(w):
            if w == 'point':
                return False

            try:
                pq.Quantity(0.0, w)
                return True
            except:
                return w == '/'

        def extractUnits(input):
            units = []
            description = ""
            for w in input.split(' '):
                if isValidUnit(w):
                    if description:
                        description += " "
                    description += w
                else:
                    if description:
                        units.append(description)
                    description = ""

            if description:
                units.append(description)
            return units

        n = NumberService().longestNumber(input)
        units = extractUnits(input)

        # Convert to quantity object, attempt conversion
        quantity = pq.Quantity(float(n), units[0])
        quantity.units = units[1]

        return quantity
