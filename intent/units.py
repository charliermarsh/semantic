import re
import quantities as pq
from numbers import NumberService


class ConversionService(object):

    __exponents__ = {
        'square': 2,
        'squared': 2,
        'cubed': 3
    }

    def preprocess(self, input):
        def handleExponents(input):
            m = re.search(r'\bsquare (\w+)', input)
            if m and self.isValidUnit(m.group(1)):
                input = re.sub(r'\bsquare (\w+)', r'\g<1>^2', input)

            m = re.search(r'\bsquared (\w+)', input)
            if m and self.isValidUnit(m.group(1)):
                input = re.sub(r'\bsquared (\w+)', r'\g<1>^2', input)

            m = re.search(r'\b(\w+) squared', input)
            if m and self.isValidUnit(m.group(1)):
                input = re.sub(r'\b(\w+) squared', r'\g<1>^2', input)

            m = re.search(r'\bsq (\w+)', input)
            if m and self.isValidUnit(m.group(1)):
                input = re.sub(r'\bsq (\w+)', r'\g<1>^2', input)

            m = re.search(r'\b(\w+) cubed', input)
            if m and self.isValidUnit(m.group(1)):
                input = re.sub(r'\b(\w+) cubed', r'\g<1>^3', input)

            m = re.search(r'\bcubic (\w+)', input)
            if m and self.isValidUnit(m.group(1)):
                input = re.sub(r'\bcubic (\w+)', r'\g<1>^3', input)

            service = NumberService()
            m = re.search(r'\b(\w+) to the (\w+)( power)?', input)
            if m and self.isValidUnit(m.group(1)):
                if m.group(2) in service.__ordinals__:
                    exp = service.parseMagnitude(m.group(2))
                    input = re.sub(r'\b(\w+) to the (\w+)( power)?',
                                   r'\g<1>^' + str(exp), input)

            return input

        input = re.sub(r'\sper\s', r' / ', input)
        input = handleExponents(input)

        return input

    def parseUnits(self, input):
        """
        Carries out some conversion (represented as a string) and
        returns the result as a human-ready string.
        """
        quantity = self.convert(input)
        units = ' '.join(str(quantity.units).split(' ')[1:])
        return NumberService.parseMagnitude(quantity.item()) + " " + units

    def isValidUnit(self, w):
        bad = set(['point', 'a'])
        if w in bad:
            return False

        try:
            pq.Quantity(0.0, w)
            return True
        except:
            return w == '/'

    def extractUnits(self, input):
        """Collects all the valid units from an input string."""
        input = self.preprocess(input)

        units = []
        description = ""
        for w in input.split(' '):
            if self.isValidUnit(w) or w == '/':
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
        input = self.preprocess(input)

        n = NumberService().longestNumber(input)
        units = self.extractUnits(input)

        # Convert to quantity object, attempt conversion
        quantity = pq.Quantity(float(n), units[0])
        quantity.units = units[1]

        return quantity
