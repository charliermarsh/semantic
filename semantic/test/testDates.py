import datetime
import unittest
from freezegun import freeze_time
from semantic.dates import DateService


@freeze_time('2014-01-01 00:00')
class TestDate(unittest.TestCase):

    def compareDate(self, input, target):
        service = DateService()
        result = service.extractDate(input)
        self.assertEqual(target, result)

    def compareTime(self, input, target):
        service = DateService()
        result = service.extractDate(input)
        self.assertEqual(target, result)

    def compareDates(self, input, targets):
        service = DateService()
        results = service.extractDates(input)
        for (result, target) in zip(results, targets):
            self.assertEqual(target, result)

    def compareTimes(self, input, targets):
        service = DateService()
        results = service.extractDates(input)
        for (result, target) in zip(results, targets):
            self.assertEqual(target.time(), result.time())

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

    def testOrdinalNums(self):
        input = "Remind me on January 2nd"
        target = datetime.datetime(2014, 1, 2)
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
        target = datetime.datetime(2014, 1, 2, 8, 0)
        self.compareDate(input, target)

    def testToday(self):
        input = "Send me an email some time today if you can"
        target = datetime.datetime.today()
        self.compareDate(input, target)

    def testThis(self):
        input = "This morning, I went to the gym"
        target = datetime.datetime(2014, 1, 1, 8, 0)
        self.compareDate(input, target)

    def testIllegalDate(self):
        input = "I have a meeting on February 29 at 12:15pm"
        self.assertRaises(ValueError, lambda: DateService().extractDate(input))

    def testMultiple(self):
        input = "Tomorrow, I'll schedule the meeting for June 9 at 1:30pm"
        target = datetime.datetime(2014, 1, 2, 13, 30)
        self.compareDate(input, target)

    #
    #  Time Tests
    #

    def testExactTime(self):
        input = "Let's go to the park at 12:51pm tomorrow"
        target = datetime.datetime(2014, 1, 2, 12, 51)
        self.compareTime(input, target)

    def testInExactTime(self):
        input = "I want to leave in two hours and twenty minutes"
        target = datetime.datetime.today() + \
            datetime.timedelta(hours=2, minutes=20)
        self.compareTime(input, target)

    def testTimeNoMinutes(self):
        input = "Let's go to the park at 8pm tomorrow"
        target = datetime.datetime(2014, 1, 2, 20, 0)
        self.compareTime(input, target)

    def testAmbiguousTime(self):
        input = "Let's go to the park at 8 tomorrow"
        target = datetime.datetime(2014, 1, 2, 8, 0)
        self.compareTime(input, target)

    def testMilitaryMorningTime(self):
        input = "Let's go to the park at 08:00 tomorrow"
        target = datetime.datetime(2014, 1, 2, 8, 0)
        self.compareTime(input, target)

    def testMilitaryAfternoonTime(self):
        input = "Let's go to the park at 20:00 tomorrow"
        target = datetime.datetime(2014, 1, 2, 20, 0)
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
