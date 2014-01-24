import re


class NumberService(object):
    __ones__ = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
        'eleven': 11,
        'twelve': 12,
        'thirteen': 13,
        'fourteen': 14,
        'fifteen': 15,
        'sixteen': 16,
        'seventeen': 17,
        'eighteen': 18,
        'nineteen': 19}

    __tens__ = {
        'ten':     10,
        'twenty':  20,
        'thirty':  30,
        'forty':   40,
        'fifty':   50,
        'sixty':   60,
        'seventy': 70,
        'eighty':  80,
        'ninety':  90
    }

    __ordinals__ = {
        'first': 'one',
        'second': 'two',
        'third': 'three',
        'fourth': 'four',
        'fifth': 'five',
        'sixth': 'six',
        'seventh': 'seventh',
        'eighth': 'eight',
        'ninth': 'nine',
        'tenth': 'ten',
        'eleventh': 'eleven',
        'twelth': 'twelve',
        'thirteenth': 'thirteen',
        'fifteenth': 'fifteen',
        'sixteenth': 'sixteen',
        'seventeenth': 'seventeen',
        'eighteenth': 'eighteen',
        'nineteenth': 'nineteen',
        'twentieth': 'twenty',
        'thirtieth': 'thirty',
        'fortieth': 'forty',
        'fiftieth': 'fifty',
        'sixtieth': 'sixty',
        'seventieth': 'seventy',
        'eightieth': 'eighty',
        'ninetieth': 'ninety',
        'hundredth': 'hundred'
    }

    __fractions__ = {
        'quarter': 'four',
        'half': 'two',
        'halve': 'two'
    }

    __groups__ = {
        'thousand': 1000,
        'million': 1000000,
        'billion': 1000000000,
        'trillion': 1000000000000}

    # Captures group names
    __groups_re__ = re.compile(
        r'\s?([\w\s]+?)(?:\s((?:%s))|$)' %
        ('|'.join(__groups__)))

    # Captures 'n hundred' expressions in groups
    __hundreds_re__ = re.compile(r'([\w\s]+)\shundred(?:\s(.*)|$)')

    # Captures 'ten ones' pattern in groups
    __tens_and_ones_re__ = re.compile(
        r'((?:%s))(?:\s(.*)|$)' %
        ('|'.join(__tens__.keys())))

    def parse(self, words):
        """
            A general method for parsing word-representations of numbers.
            Supports floats and integers.

            Arguments:
            words -- word representation of a numerical value.

            Returns:
            floating-point representation of the words
        """
        def exact(words):
            """If already represented as float or int, convert."""
            try:
                return int(words)
            except:
                try:
                    return float(words)
                except:
                    return None

        if exact(words):
            return exact(words)

        split = words.split(' ')

        # Replace final ordinal/fraction with number
        if split[-1] in self.__fractions__:
            split[-1] = self.__fractions__[split[-1]]
        elif split[-1] in self.__ordinals__:
            split[-1] = self.__ordinals__[split[-1]]

        parsed_ordinals = ' '.join(split)

        return self.parseFloat(parsed_ordinals)

    def parseFloat(self, words):
        """
            Convert a floating-point number described in words to a double.
            Supports two kinds of descriptions: those with a 'point' (e.g.,
            "one point two five") and those with a fraction (e.g., "one and
            a quarter").

            Arguments:
            words -- description of the floating-point number

            Returns:
            double representation of the words
        """
        def pointFloat(words):
            m = re.search(r'(.*) point (.*)', words)
            if m:
                whole = m.group(1)
                frac = m.group(2)
                total = 0.0
                coeff = 0.10
                for digit in frac.split(' '):
                    total += coeff * self.parse(digit)
                    coeff /= 10.0

                return self.parseInt(whole) + total
            return None

        def fractionFloat(words):
            m = re.search(r'(.*) and (.*)', words)
            if m:
                whole = self.parseInt(m.group(1))
                frac = m.group(2)

                # Replace plurals
                frac = re.sub(r'(\w+)s(\b)', '\g<1>\g<2>', frac)

                # Convert 'a' to 'one' (e.g., 'a third' to 'one third')
                frac = re.sub(r'(\b)a(\b)', '\g<1>one\g<2>', frac)

                split = frac.split(' ')

                # Split fraction into num (regular integer), denom (ordinal)
                num = split[:1]
                denom = split[1:]

                while denom:
                    try:
                        # Test for valid num, denom
                        num_value = self.parse(' '.join(num))
                        denom_value = self.parse(' '.join(denom))
                        return whole + float(num_value) / denom_value
                    except:
                        # Add another word to num
                        num += denom[:1]
                        denom = denom[1:]
            return None

        # Extract "one point two five"-type float
        result = pointFloat(words)
        if result:
            return result

        # Extract "one and a quarter"-type float
        result = fractionFloat(words)
        if result:
            return result

        # Parse as integer
        return self.parseInt(words)

    def parseInt(self, words):
        """
            Parses words to the integer they describe.

            Arguments:
            words -- description of the integer

            Returns:
            integer representation of the words
        """
        # Remove 'and', case-sensitivity
        words = words.replace(" and ", " ").lower()
        # 'a' -> 'one'
        words = re.sub(r'(\b)a(\b)', '\g<1>one\g<2>', words)

        # Build number from 0
        num = 0

        # Loop through number groups
        for group in NumberService.__groups_re__.findall(words):
            # Determine position of group, assuming ones group
            group_multiplier = 1
            if group[1] in NumberService.__groups__:
                group_multiplier = NumberService.__groups__[group[1]]

            group_num = 0

            # Extract hunderds
            hundreds_match = NumberService.__hundreds_re__.match(group[0])

            # Extracting remaining values (tens, ones place)
            tens_and_ones = None

            # Check for 'n hundred' pattern
            if hundreds_match and hundreds_match.group(1):
                group_num = group_num + \
                    (NumberService.__ones__[hundreds_match.group(1)] * 100)
                tens_and_ones = hundreds_match.group(2)
            else:
            # Entire string contains only tens- and ones-place values
                tens_and_ones = group[0]

            if tens_and_ones is None:
                num = num + (group_num * group_multiplier)
                continue

            # Look for tens and ones ('tn1')
            tn1_match = NumberService.__tens_and_ones_re__.match(
                tens_and_ones)

            if tn1_match is not None:
                # Add tens
                group_num = group_num + \
                    NumberService.__tens__[tn1_match.group(1)]
                # Add ones
                if tn1_match.group(2) is not None:
                    group_num = group_num + \
                        NumberService.__ones__[tn1_match.group(2)]
            else:
            # Assume 'tens and ones' contained only ones-place values
                group_num = group_num + NumberService.__ones__[tens_and_ones]
            # Increment total by current group number times its multiplier
            num = num + (group_num * group_multiplier)

        return num

    def isValid(self, input):
        try:
            self.parse(input)
            return True
        except:
            return False
