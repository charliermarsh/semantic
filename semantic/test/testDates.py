import datetime
import unittest
from semantic.dates import DateService


class TestDate(unittest.TestCase):

    def compareDate(self, in_val, target):
        service = DateService()
        result = service.extractDate(in_val)
        self.assertEqual(result.month, target.month)
        self.assertEqual(result.day, target.day)

    def compareTime(self, in_val, target):
        service = DateService()
        result = service.extractDate(in_val)
        self.assertEqual(result.hour, target.hour)
        self.assertEqual(result.minute, target.minute)

    def compareDates(self, in_val, targets):
        service = DateService()
        results = service.extractDates(in_val)
        for (result, target) in zip(results, targets):
            self.assertEqual(result.month, target.month)
            self.assertEqual(result.day, target.day)

    def compareTimes(self, in_val, targets):
        service = DateService()
        results = service.extractDates(in_val)
        for (result, target) in zip(results, targets):
            self.assertEqual(result.hour, target.hour)
            self.assertEqual(result.minute, target.minute)

    #
    #  Date Tests
    #

    def testExactWords(self):
        in_val = "Remind me on January Twenty Sixth"
        target = datetime.datetime(datetime.datetime.now().year, 1, 26)
        self.compareDate(in_val, target)

    def testExactWordsDash(self):
        in_val = "Remind me on January Twenty-Sixth"
        target = datetime.datetime(datetime.datetime.now().year, 1, 26)
        self.compareDate(in_val, target)

    def testExactNums(self):
        in_val = "Remind me on January 26"
        target = datetime.datetime(datetime.datetime.now().year, 1, 26)
        self.compareDate(in_val, target)

    def testWeekFromExact(self):
        in_val = "Do x y and z a week from January 26"
        target = datetime.datetime(datetime.datetime.now().year, 1, 26) + datetime.timedelta(days=7)
        self.compareDate(in_val, target)

    def testMultipleWeeksFrom(self):
        in_val = "Do x y and z three weeks from January 26"
        target = datetime.datetime(datetime.datetime.now().year, 1, 26) + datetime.timedelta(days=21)
        self.compareDate(in_val, target)

    def testMultiWordDaysFrom(self):
        in_val = "Do x y and z twenty six days from January 26"
        target = datetime.datetime(datetime.datetime.now().year, 1, 26) + datetime.timedelta(days=26)
        self.compareDate(in_val, target)

    def testMultiWordAndDaysFrom(self):
        in_val = "Do x y and z one hundred and twelve days from January 26"
        target = datetime.datetime(datetime.datetime.now().year, 1, 26) + datetime.timedelta(days=112)
        self.compareDate(in_val, target)

    def testNextFriday(self):
        in_val = "Next Friday, go to the grocery store"
        friday = 4
        num_days_away = (friday - datetime.datetime.today().weekday()) % 7
        target = datetime.datetime.today() + \
            datetime.timedelta(
                days=7 + num_days_away)
        self.compareDate(in_val, target)

    def testAmbiguousNext(self):
        in_val = "The next event will take place on Friday"
        friday = 4
        num_days_away = (friday - datetime.datetime.today().weekday()) % 7
        target = datetime.datetime.today() + \
            datetime.timedelta(
                days=num_days_away)
        self.compareDate(in_val, target)

    def testTomorrow(self):
        in_val = "Tomorrow morning, go to the grocery store"
        target = datetime.datetime.today() + datetime.timedelta(days=1)
        self.compareDate(in_val, target)

    def testToday(self):
        in_val = "Send me an email some time today if you can"
        target = datetime.datetime.today()
        self.compareDate(in_val, target)

    def testThis(self):
        in_val = "This morning, I went to the gym"
        target = datetime.datetime.today()
        self.compareDate(in_val, target)

    def testIllegalDate(self):
        in_val = "I have a meeting on February 29 at 12:15pm"
        self.assertRaises(ValueError, lambda: DateService().extractDate(in_val))

    def testMultiple(self):
        in_val = "Tomorrow, I'll schedule the meeting for June 9 at 1:30pm"
        target = datetime.datetime.today() + datetime.timedelta(days=1)
        self.compareDate(in_val, target)

    #
    #  Time Tests
    #

    def testExactTime(self):
        in_val = "Let's go to the park at 12:51pm tomorrow"
        tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
        target = datetime.datetime(
            tomorrow.year, tomorrow.month, tomorrow.day, 12, 51)
        self.compareTime(in_val, target)

    def testInExactTime(self):
        in_val = "I want to leave in two hours and twenty minutes"
        target = datetime.datetime.today() + \
            datetime.timedelta(hours=2, minutes=20)
        self.compareTime(in_val, target)

    #
    # Multi-date tests
    #

    def testTwoDates(self):
        in_val = "From March 13 at 12:30pm to September 2 at 11:15am"
        targets = [datetime.datetime(datetime.datetime.now().year, 3, 13, 12, 30),
                   datetime.datetime(datetime.datetime.now().year, 9, 2, 11, 15)]
        self.compareDates(in_val, targets)
        self.compareTimes(in_val, targets)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDate)
    unittest.TextTestRunner(verbosity=2).run(suite)
