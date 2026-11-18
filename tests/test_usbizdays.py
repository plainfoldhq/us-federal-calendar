import os, sys, unittest
from datetime import date
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
import usbizdays as b

class T(unittest.TestCase):
    def test_federal(self):
        self.assertFalse(b.is_business_day("2026-11-26"))
        self.assertFalse(b.is_business_day("2021-12-31"))
        self.assertEqual(b.add_business_days("2026-11-25", 3), date(2026, 12, 1))
        self.assertEqual(b.business_days_between("2026-11-01", "2026-12-01"), 19)
    def test_nyse_fed(self):
        self.assertFalse(b.is_business_day("2026-04-03", calendar="nyse"))
        self.assertTrue(b.is_business_day("2026-04-03", calendar="fed"))
        self.assertTrue(b.is_business_day("2021-12-31", calendar="nyse"))
        self.assertTrue(b.is_business_day("2026-07-03", calendar="fed"))
        self.assertFalse(b.is_business_day("2026-07-03", calendar="nyse"))

class DatetimeInput(unittest.TestCase):
    def test_datetime_is_treated_as_its_date(self):
        from datetime import datetime
        self.assertFalse(b.is_business_day(datetime(2026, 11, 26, 9, 30)))
        self.assertEqual(b.holiday_name(datetime(2026, 11, 26)), b.holiday_name(date(2026, 11, 26)))
        self.assertEqual(b.add_business_days(datetime(2026, 11, 25), 1), date(2026, 11, 27))
        self.assertEqual(b.business_days_between(datetime(2026, 11, 1), datetime(2026, 12, 1)), 19)

if __name__ == "__main__":
    unittest.main()
