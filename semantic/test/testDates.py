import datetime
import unittest
from semantic.dates import DateService


class TestDate(unittest.TestCase):

    def compareDate(self, inp, target):
        service = DateService()
        result = service.extractDate(inp)
        self.assertEqual(result.month, target.month)
        self.assertEqual(result.day, target.day)

    def compareTime(self, inp, target):
        service = DateService()
        result = service.extractDate(inp)
        self.assertEqual(result.hour, target.hour)
        self.assertEqual(result.minute, target.minute)

    def compareDates(self, inp, targets):
        service = DateService()
        results = service.extractDates(inp)
        for (result, target) in zip(results, targets):
            self.assertEqual(result.month, target.month)
            self.assertEqual(result.day, target.day)

    def compareTimes(self, inp, targets):
        service = DateService()
        results = service.extractDates(inp)
        for (result, target) in zip(results, targets):
            self.assertEqual(result.hour, target.hour)
            self.assertEqual(result.minute, target.minute)

    #
    #  Date Tests
    #

    def testExactWords(self):
        inp = "Remind me on January Twenty Sixth"
        target = datetime.datetime(datetime.datetime.now().year, 1, 26)
        self.compareDate(inp, target)

    def testExactWordsDash(self):
        inp = "Remind me on January Twenty-Sixth"
        target = datetime.datetime(datetime.datetime.now().year, 1, 26)
        self.compareDate(inp, target)

    def testExactNums(self):
        inp = "Remind me on January 26"
        target = datetime.datetime(datetime.datetime.now().year, 1, 26)
        self.compareDate(inp, target)

    def testWeekFromExact(self):
        inp = "Do x y and z a week from January 26"
        target = datetime.datetime(datetime.datetime.now().year, 1, 26) + datetime.timedelta(days=7)
        self.compareDate(inp, target)

    def testMultipleWeeksFrom(self):
        inp = "Do x y and z three weeks from January 26"
        target = datetime.datetime(datetime.datetime.now().year, 1, 26) + datetime.timedelta(days=21)
        self.compareDate(inp, target)

    def testMultiWordDaysFrom(self):
        inp = "Do x y and z twenty six days from January 26"
        target = datetime.datetime(datetime.datetime.now().year, 1, 26) + datetime.timedelta(days=26)
        self.compareDate(inp, target)

    def testMultiWordAndDaysFrom(self):
        inp = "Do x y and z one hundred and twelve days from January 26"
        target = datetime.datetime(datetime.datetime.now().year, 1, 26) + datetime.timedelta(days=112)
        self.compareDate(inp, target)

    def testNextFriday(self):
        inp = "Next Friday, go to the grocery store"
        friday = 4
        num_days_away = (friday - datetime.datetime.today().weekday()) % 7
        target = datetime.datetime.today() + \
            datetime.timedelta(
                days=7 + num_days_away)
        self.compareDate(inp, target)

    def testAmbiguousNext(self):
        inp = "The next event will take place on Friday"
        friday = 4
        num_days_away = (friday - datetime.datetime.today().weekday()) % 7
        target = datetime.datetime.today() + \
            datetime.timedelta(
                days=num_days_away)
        self.compareDate(inp, target)

    def testTomorrow(self):
        inp = "Tomorrow morning, go to the grocery store"
        target = datetime.datetime.today() + datetime.timedelta(days=1)
        self.compareDate(inp, target)

    def testToday(self):
        inp = "Send me an email some time today if you can"
        target = datetime.datetime.today()
        self.compareDate(inp, target)

    def testThis(self):
        inp = "This morning, I went to the gym"
        target = datetime.datetime.today()
        self.compareDate(inp, target)

    def testIllegalDate(self):
        inp = "I have a meeting on February 29 at 12:15pm"
        self.assertRaises(ValueError, lambda: DateService().extractDate(inp))

    def testMultiple(self):
        inp = "Tomorrow, I'll schedule the meeting for June 9 at 1:30pm"
        target = datetime.datetime.today() + datetime.timedelta(days=1)
        self.compareDate(inp, target)

    #
    #  Time Tests
    #

    def testExactTime(self):
        inp = "Let's go to the park at 12:51pm tomorrow"
        tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
        target = datetime.datetime(
            tomorrow.year, tomorrow.month, tomorrow.day, 12, 51)
        self.compareTime(inp, target)

    def testInExactTime(self):
        inp = "I want to leave in two hours and twenty minutes"
        target = datetime.datetime.today() + \
            datetime.timedelta(hours=2, minutes=20)
        self.compareTime(inp, target)

    #
    # Multi-date tests
    #

    def testTwoDates(self):
        inp = "From March 13 at 12:30pm to September 2 at 11:15am"
        targets = [datetime.datetime(datetime.datetime.now().year, 3, 13, 12, 30),
                   datetime.datetime(datetime.datetime.now().year, 9, 2, 11, 15)]
        self.compareDates(inp, targets)
        self.compareTimes(inp, targets)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDate)
    unittest.TextTestRunner(verbosity=2).run(suite)
