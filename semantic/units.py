import re
import quantities as pq
from .numbers import NumberService


class ConversionService(object):

    __exponents__ = {
        'square': 2,
        'squared': 2,
        'cubed': 3
    }

    def _preprocess(self, inp):
        def handleExponents(inp):
            m = re.search(r'\bsquare (\w+)', inp)
            if m and self.isValidUnit(m.group(1)):
                inp = re.sub(r'\bsquare (\w+)', r'\g<1>^2', inp)

            m = re.search(r'\bsquared (\w+)', inp)
            if m and self.isValidUnit(m.group(1)):
                inp = re.sub(r'\bsquared (\w+)', r'\g<1>^2', inp)

            m = re.search(r'\b(\w+) squared', inp)
            if m and self.isValidUnit(m.group(1)):
                inp = re.sub(r'\b(\w+) squared', r'\g<1>^2', inp)

            m = re.search(r'\bsq (\w+)', inp)
            if m and self.isValidUnit(m.group(1)):
                inp = re.sub(r'\bsq (\w+)', r'\g<1>^2', inp)

            m = re.search(r'\b(\w+) cubed', inp)
            if m and self.isValidUnit(m.group(1)):
                inp = re.sub(r'\b(\w+) cubed', r'\g<1>^3', inp)

            m = re.search(r'\bcubic (\w+)', inp)
            if m and self.isValidUnit(m.group(1)):
                inp = re.sub(r'\bcubic (\w+)', r'\g<1>^3', inp)

            service = NumberService()
            m = re.search(r'\b(\w+) to the (\w+)( power)?', inp)
            if m and self.isValidUnit(m.group(1)):
                if m.group(2) in service.__ordinals__:
                    exp = service.parseMagnitude(m.group(2))
                    inp = re.sub(r'\b(\w+) to the (\w+)( power)?',
                                   r'\g<1>^' + str(exp), inp)

            return inp

        inp = re.sub(r'\sper\s', r' / ', inp)
        inp = handleExponents(inp)

        return inp

    def parseUnits(self, inp):
        """Carries out a conversion (represented as a string) and returns the
        result as a human-readable string.

        Args:
            inp (str): Text representing a unit conversion, which should
                include a magnitude, a description of the initial units,
                and a description of the target units to which the quantity
                should be converted.

        Returns:
            A quantities object representing the converted quantity and its new
            units.
        """
        quantity = self.convert(inp)
        units = ' '.join(str(quantity.units).split(' ')[1:])
        return NumberService.parseMagnitude(quantity.item()) + " " + units

    def isValidUnit(self, w):
        """Checks if a string represents a valid quantities unit.

        Args:
            w (str): A string to be tested against the set of valid
                quantities units.

        Returns:
            True if the string can be used as a unit in the quantities
            module.
        """
        bad = set(['point', 'a'])
        if w in bad:
            return False

        try:
            pq.Quantity(0.0, w)
            return True
        except:
            return w == '/'

    def extractUnits(self, inp):
        """Collects all the valid units from an inp string. Works by
        appending consecutive words from the string and cross-referncing
        them with a set of valid units.

        Args:
            inp (str): Some text which hopefully contains descriptions
                of different units.

        Returns:
            A list of strings, each entry in which is a valid quantities
            unit.
        """
        inp = self._preprocess(inp)

        units = []
        description = ""
        for w in inp.split(' '):
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

    def convert(self, inp):
        """Converts a string representation of some quantity of units into a
        quantities object.

        Args:
            inp (str): A textual representation of some quantity of units,
                e.g., "fifty kilograms".

        Returns:
            A quantities object representing the described quantity and its
            units.
        """
        inp = self._preprocess(inp)

        n = NumberService().longestNumber(inp)
        units = self.extractUnits(inp)

        # Convert to quantity object, attempt conversion
        quantity = pq.Quantity(float(n), units[0])
        quantity.units = units[1]

        return quantity
