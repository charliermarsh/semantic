import datetime
import unittest
from semantic.dates import DateService


class TestDate(unittest.TestCase):

    def compareDate(self, input, target):
        service = DateService()
        result = service.extractDate(input)
        self.assertEqual(result.month, target.month)
        self.assertEqual(result.day, target.day)

    def compareTime(self, input, target):
        service = DateService()
        result = service.extractDate(input)
        self.assertEqual(result.hour, target.hour)
        self.assertEqual(result.minute, target.minute)

    def compareDates(self, input, targets):
        service = DateService()
        results = service.extractDates(input)
        for (result, target) in zip(results, targets):
            self.assertEqual(result.month, target.month)
            self.assertEqual(result.day, target.day)

    def compareTimes(self, input, targets):
        service = DateService()
        results = service.extractDates(input)
        for (result, target) in zip(results, targets):
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

    def testMultipleWeeksFrom(self):
        input = "Do x y and z three weeks from January 26"
        target = datetime.datetime(2014, 1, 26) + datetime.timedelta(days=21)
        self.compareDate(input, target)

    def testMultiWordDaysFrom(self):
        input = "Do x y and z twenty six days from January 26"
        target = datetime.datetime(2014, 1, 26) + datetime.timedelta(days=26)
        self.compareDate(input, target)

    def testMultiWordAndDaysFrom(self):
        input = "Do x y and z one hundred and twelve days from January 26"
        target = datetime.datetime(2014, 1, 26) + datetime.timedelta(days=112)
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
        self.assertRaises(ValueError, lambda: DateService().extractDate(input))

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

    def testInExactTime(self):
        input = "I want to leave in two hours and twenty minutes"
        target = datetime.datetime.today() + \
            datetime.timedelta(hours=2, minutes=20)
        self.compareTime(input, target)

    #
    # Multi-date tests
    #

    def testTwoDates(self):
        input = "From March 13 at 12:30pm to September 2 at 11:15am"
        targets = [datetime.datetime(2014, 3, 13, 12, 30),
                   datetime.datetime(2014, 9, 2, 11, 15)]
        self.compareDates(input, targets)
        self.compareTimes(input, targets)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDate)
    unittest.TextTestRunner(verbosity=2).run(suite)
