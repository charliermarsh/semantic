import re
import quantities as pq
from numbers import NumberService


class ConversionService(object):

    @staticmethod
    def preprocess(input):
        # 'per' --> '/'
        input = re.sub(r'\sper\s', r' / ', input)
        return input

    def parseUnits(self, input):
        """
        Carries out some conversion (represented as a string) and
        returns the result as a human-ready string.
        """
        quantity = self.convert(input)
        units = ' '.join(str(quantity.units).split(' ')[1:])
        return NumberService.parseMagnitude(quantity.item()) + " " + units

    def extractUnits(self, input):
        """Collects all the valid units from an input string."""
        input = ConversionService.preprocess(input)

        def isValidUnit(w):
            if w == 'point':
                return False

            try:
                pq.Quantity(0.0, w)
                return True
            except:
                return w == '/'

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

    def convert(self, input):
        """
        Converts a string representation of some quantity of units
        and converts it to a quantities object.
        """
        input = ConversionService.preprocess(input)

        n = NumberService().longestNumber(input)
        units = self.extractUnits(input)

        # Convert to quantity object, attempt conversion
        quantity = pq.Quantity(float(n), units[0])
        quantity.units = units[1]

        return quantity
