import quantities as pq
from numbers import NumberService


class ConversionService(object):

    @staticmethod
    def preprocess(input):
        # 'per' --> '/'
        input = re.sub(r'\sper\s', r'\s/\s', input)
        # 'one hundred and eleven' --> 'one hundred eleven'
        input = re.sub(r'\sand\s', r' ', input)
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
        return magString

    def parseUnits(self, input):
        """
            Carries out some conversion (represented as a string) and
            returns the result as a human-ready string.
        """
        quantity = self.convert(input)
        return ConversionService.parseMagnitude(quantity.item()) + " " + quantity.units

    def convert(self, input):
        """
            Converts a string representation of some quantity of units
            and converts it to a quantities object.
        """
        split = ConversionService.preprocess(input).split(' ')

        # Collect consecutive runs of units
        def isValidUnit(w):
            try:
                pq.Quantity(0.0, w)
                return True
            except:
                return w == '/'

        units = []
        desc = ""
        for w in split:
            if isValidUnit(w):
                if desc:
                    desc += " "
                desc += w
            else:
                if desc:
                    units.append(desc)
                desc = ""

        if desc:
            units.append(desc)

        # Collect consecutive runs of numbers
        def isNumber(s):
            try:
                converter = NumberService()
                converter.parse(s)
                return True
            except:
                return False

        desc = ""
        for i, w in enumerate(split):
            if isNumber(w):
                desc = w

                for w2 in split[i+1:]:
                    if isNumber(desc + " " + w2):
                        desc += " " + w2
                    else:
                        break
                break

        n = converter.parse(desc)

        # Convert to quantity object, attempt conversion
        quantity = pq.Quantity(float(n), units[0])
        quantity.units = units[1]

        return quantity
