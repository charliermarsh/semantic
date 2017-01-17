import re
import datetime
try:
    from itertools import zip_longest
except:
    from itertools import izip_longest as zip_longest
from .numbers import NumberService


class DateService(object):

    """Initialize a DateService for extracting dates from text.

    Args:
        tz: An optional Pytz timezone. All datetime objects returned will
            be relative to the supplied timezone, or timezone-less if none
            is supplied.
        now: The time to which all returned datetime objects should be
            relative. For example, if the text is "In 5 hours", the
            datetime returned will be now + datetime.timedelta(hours=5).
            Uses datetime.datetime.now() if none is supplied.

    Returns:
        A DateService which uses tz and now for all of its computations.
    """

    def __init__(self, tz=None, now=None):
        self.tz = tz
        if now:
            self.now = now
        else:
            self.now = datetime.datetime.now(tz=self.tz)

    __months__ = ['january', 'february', 'march', 'april', 'may', 'june',
                  'july', 'august', 'september', 'october', 'november',
                  'december']

    __shortMonths__ = ['jan', 'feb', 'mar', 'apr', 'may',
                       'jun', 'jul', 'aug', 'sept', 'oct', 'nov', 'dec']

    __daysOfWeek__ = ['monday', 'tuesday', 'wednesday',
                      'thursday', 'friday', 'saturday', 'sunday']

    __relativeDates__ = ['tomorrow', 'tonight', 'next']

    __todayMatches__ = ['tonight', 'today', 'this morning',
                        'this evening', 'this afternoon']

    __tomorrowMatches__ = ['tomorrow', 'next morning',
                           'next evening', 'next afternoon']

    __dateDescriptors__ = {
        'one': 1,
        'first': 1,
        'two': 2,
        'second': 2,
        'three': 3,
        'third': 3,
        'four': 4,
        'fourth': 4,
        'five': 5,
        'fifth': 5,
        'six': 6,
        'sixth': 6,
        'seven': 7,
        'seventh': 7,
        'eight': 8,
        'eighth': 8,
        'nine': 9,
        'ninth': 9,
        'ten': 10,
        'tenth': 10,
        'eleven': 11,
        'eleventh': 11,
        'twelve': 12,
        'twelth': 12,
        'thirteen': 13,
        'thirteenth': 13,
        'fourteen': 14,
        'fourteenth': 14,
        'fifteen': 15,
        'fifteenth': 15,
        'sixteen': 16,
        'sixteenth': 16,
        'seventeen': 17,
        'seventeenth': 17,
        'eighteen': 18,
        'eighteenth': 18,
        'nineteen': 19,
        'nineteenth': 19,
        'twenty': 20,
        'twentieth': 20,
        'twenty one': 21,
        'twenty first': 21,
        'twenty two': 22,
        'twenty second': 22,
        'twenty three': 23,
        'twenty third': 23,
        'twenty four': 24,
        'twenty fourth': 24,
        'twenty five': 25,
        'twenty fifth': 25,
        'twenty six': 26,
        'twenty sixth': 26,
        'twenty seven': 27,
        'twenty seventh': 27,
        'twenty eight': 28,
        'twenty eighth': 28,
        'twenty nine': 29,
        'twenty ninth': 29,
        'thirty': 30,
        'thirtieth': 30,
        'thirty one': 31,
        'thirty first': 31
    }

    _dayRegex = re.compile(
        r"""(?ix)
        ((week|day)s?\ from\ )?
        (
            tomorrow
            |tonight
            |today
            |(next|this)[\ \b](morning|afternoon|evening|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)
            |(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)
            |(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sept(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\ (\w+)((\s|\-)?\w*)
        )
        """)

    _timeRegex = re.compile(
        r"""(?ix)
        .*?
        (
            morning
            |afternoon
            |evening
            |(\d{1,2}\:\d{2})\ ?(am|pm)?
            |in\ (.+?)\ (hours|minutes)(\ (?:and\ )?(.+?)\ (hours|minutes))?
        )
        .*?""")

    def _preprocess(self, inp):
        return inp.replace('-', ' ').lower()

    def extractDays(self, inp):
        """Extracts all day-related information from an input string.
        Ignores any information related to the specific time-of-day.

        Args:
            inp (str): Input string to be parsed.

        Returns:
            A list of datetime objects containing the extracted date from the
            input snippet, or an empty list if none found.
        """
        inp = self._preprocess(inp)

        def extractDayOfWeek(dayMatch):
            if dayMatch.group(5) in self.__daysOfWeek__:
                return self.__daysOfWeek__.index(dayMatch.group(5))
            elif dayMatch.group(6) in self.__daysOfWeek__:
                return self.__daysOfWeek__.index(dayMatch.group(6))

        def extractMonth(dayMatch):
            if dayMatch.group(7) in self.__months__:
                return self.__months__.index(dayMatch.group(7)) + 1
            elif dayMatch.group(7) in self.__shortMonths__:
                return self.__shortMonths__.index(dayMatch.group(7)) + 1

        def extractDay(dayMatch):
            combined = dayMatch.group(8) + dayMatch.group(9)
            if combined in self.__dateDescriptors__:
                return self.__dateDescriptors__[combined]
            elif dayMatch.group(8) in self.__dateDescriptors__:
                return self.__dateDescriptors__[dayMatch.group(8)]
            elif int(dayMatch.group(8)) in self.__dateDescriptors__.values():
                return int(dayMatch.group(8))

        def extractDaysFrom(dayMatch):
            if not dayMatch.group(1):
                return 0

            def numericalPrefix(dayMatch):
                # Grab 'three' of 'three weeks from'
                prefix = inp.split(dayMatch.group(1))[0].strip().split(' ')
                prefix.reverse()
                prefix = list(filter(lambda s: s != 'and', prefix))

                # Generate best guess number
                service = NumberService()
                num = prefix[0]
                if service.isValid(num):
                    for n in prefix[1:]:
                        inc = n + " " + num
                        if service.isValid(inc):
                            num = inc
                        else:
                            break
                    return service.parse(num)
                return 1

            factor = numericalPrefix(dayMatch)

            if dayMatch.group(2) == 'week':
                return factor * 7
            elif dayMatch.group(2) == 'day':
                return factor * 1

        def handleMatch(dayMatch):
            def safe(exp):
                """For safe evaluation of regex groups"""
                try:
                    return exp()
                except:
                    return False

            days_from = safe(lambda: extractDaysFrom(dayMatch))
            today = safe(lambda: dayMatch.group(3) in self.__todayMatches__)
            tomorrow = safe(lambda: dayMatch.group(3)
                            in self.__tomorrowMatches__)
            next_week = safe(lambda: dayMatch.group(4) == 'next')
            day_of_week = safe(lambda: extractDayOfWeek(dayMatch))
            month = safe(lambda: extractMonth(dayMatch))
            day = safe(lambda: extractDay(dayMatch))

            # Convert extracted terms to datetime object
            if not dayMatch:
                return None
            elif today:
                d = self.now
            elif tomorrow:
                d = self.now + datetime.timedelta(days=1)
            elif type(day_of_week) == int:
                current_day_of_week = self.now.weekday()
                num_days_away = (day_of_week - current_day_of_week) % 7

                if next_week:
                    num_days_away += 7

                d = self.now + \
                    datetime.timedelta(days=num_days_away)
            elif month and day:
                d = datetime.datetime(
                    self.now.year, month, day,
                    self.now.hour, self.now.minute)

            if days_from:
                d += datetime.timedelta(days=days_from)

            return d

        matches = self._dayRegex.finditer(inp)
        return [handleMatch(dayMatch) for dayMatch in matches]

    def extractDay(self, inp):
        """Returns the first time-related date found in the input string,
        or None if not found."""
        day = self.extractDay(inp)
        if day:
            return day[0]
        return None

    def extractTimes(self, inp):
        """Extracts time-related information from an input string.
        Ignores any information related to the specific date, focusing
        on the time-of-day.

        Args:
            inp (str): Input string to be parsed.

        Returns:
            A list of datetime objects containing the extracted times from the
            input snippet, or an empty list if none found.
        """
        def handleMatch(time):
            relative = False

            if not time:
                return None

            # Default times: 8am, 12pm, 7pm
            elif time.group(1) == 'morning':
                h = 8
                m = 0
            elif time.group(1) == 'afternoon':
                h = 12
                m = 0
            elif time.group(1) == 'evening':
                h = 19
                m = 0
            elif time.group(4) and time.group(5):
                h, m = 0, 0

                # Extract hours difference
                converter = NumberService()
                try:
                    diff = converter.parse(time.group(4))
                except:
                    return None

                if time.group(5) == 'hours':
                    h += diff
                else:
                    m += diff

                # Extract minutes difference
                if time.group(6):
                    converter = NumberService()
                    try:
                        diff = converter.parse(time.group(7))
                    except:
                        return None

                    if time.group(8) == 'hours':
                        h += diff
                    else:
                        m += diff

                relative = True
            else:
                # Convert from "HH:MM pm" format
                t = time.group(2)
                h, m = int(t.split(':')[0]) % 12, int(t.split(':')[1])

                try:
                    if time.group(3) == 'pm':
                        h += 12
                except IndexError:
                    pass

            if relative:
                return self.now + datetime.timedelta(hours=h, minutes=m)
            else:
                return datetime.datetime(
                    self.now.year, self.now.month, self.now.day, h, m
                )

        inp = self._preprocess(inp)
        return [handleMatch(time) for time in self._timeRegex.finditer(inp)]

    def extractTime(self, inp):
        """Returns the first time-related date found in the input string,
        or None if not found."""
        times = self.extractTimes(inp)
        if times:
            return times[0]
        return None

    def extractDates(self, inp):
        """Extract semantic date information from an input string.
        In effect, runs both parseDay and parseTime on the input
        string and merges the results to produce a comprehensive
        datetime object.

        Args:
            inp (str): Input string to be parsed.

        Returns:
            A list of datetime objects containing the extracted dates from the
            input snippet, or an empty list if not found.
        """
        def merge(param):
            day, time = param
            if not (day or time):
                return None

            if not day:
                return time
            if not time:
                return day

            return datetime.datetime(
                day.year, day.month, day.day, time.hour, time.minute
            )

        days = self.extractDays(inp)
        times = self.extractTimes(inp)
        return map(merge, zip_longest(days, times, fillvalue=None))

    def extractDate(self, inp):
        """Returns the first date found in the input string, or None if not
        found."""
        dates = self.extractDates(inp)
        for date in dates:
            return date
        return None

    def convertDay(self, day, prefix="", weekday=False):
        """Convert a datetime object representing a day into a human-ready
        string that can be read, spoken aloud, etc.

        Args:
            day (datetime.date): A datetime object to be converted into text.
            prefix (str): An optional argument that prefixes the converted
                string. For example, if prefix="in", you'd receive "in two
                days", rather than "two days", while the method would still
                return "tomorrow" (rather than "in tomorrow").
            weekday (bool): An optional argument that returns "Monday, Oct. 1"
                if True, rather than "Oct. 1".

        Returns:
            A string representation of the input day, ignoring any time-related
            information.
        """
        def sameDay(d1, d2):
            d = d1.day == d2.day
            m = d1.month == d2.month
            y = d1.year == d2.year
            return d and m and y

        tom = self.now + datetime.timedelta(days=1)

        if sameDay(day, self.now):
            return "today"
        elif sameDay(day, tom):
            return "tomorrow"

        if weekday:
            dayString = day.strftime("%A, %B %d")
        else:
            dayString = day.strftime("%B %d")

        # Ex) Remove '0' from 'August 03'
        if not int(dayString[-2]):
            dayString = dayString[:-2] + dayString[-1]

        return prefix + " " + dayString

    def convertTime(self, time):
        """Convert a datetime object representing a time into a human-ready
        string that can be read, spoken aloud, etc.

        Args:
            time (datetime.date): A datetime object to be converted into text.

        Returns:
            A string representation of the input time, ignoring any day-related
            information.
        """
        # if ':00', ignore reporting minutes
        m_format = ""
        if time.minute:
            m_format = ":%M"

        timeString = time.strftime("%I" + m_format + " %p")

        # if '07:30', cast to '7:30'
        if not int(timeString[0]):
            timeString = timeString[1:]

        return timeString

    def convertDate(self, date, prefix="", weekday=False):
        """Convert a datetime object representing into a human-ready
        string that can be read, spoken aloud, etc. In effect, runs
        both convertDay and convertTime on the input, merging the results.

        Args:
            date (datetime.date): A datetime object to be converted into text.
            prefix (str): An optional argument that prefixes the converted
                string. For example, if prefix="in", you'd receive "in two
                days", rather than "two days", while the method would still
                return "tomorrow" (rather than "in tomorrow").
            weekday (bool): An optional argument that returns "Monday, Oct. 1"
                if True, rather than "Oct. 1".

        Returns:
            A string representation of the input day and time.
        """
        dayString = self.convertDay(
            date, prefix=prefix, weekday=weekday)
        timeString = self.convertTime(date)
        return dayString + " at " + timeString


def extractDates(inp, tz=None, now=None):
    """Extract semantic date information from an input string.
    This is a convenience method which would only be used if
    you'd rather not initialize a DateService object.

    Args:
        inp (str): The input string to be parsed.
        tz: An optional Pytz timezone. All datetime objects returned will
            be relative to the supplied timezone, or timezone-less if none
            is supplied.
        now: The time to which all returned datetime objects should be
            relative. For example, if the text is "In 5 hours", the
            datetime returned will be now + datetime.timedelta(hours=5).
            Uses datetime.datetime.now() if none is supplied.

    Returns:
        A list of datetime objects extracted from input.
    """
    service = DateService(tz=tz, now=now)
    return service.extractDates(inp)
