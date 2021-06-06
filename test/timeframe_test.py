import unittest
import datetime
import os
import sys

sys.path.append(os.path.abspath('..'))
from src.timeframe import TimeFrame


class TestTimeFrame(unittest.TestCase):
    def test_init_happy_path(self):
        start_time = datetime.datetime.now() - datetime.timedelta(10)
        end_time = datetime.datetime.now() - datetime.timedelta(5)
        update_after = datetime.datetime.now() - datetime.timedelta(9)

        timeframe = TimeFrame(start_time, end_time)

        self.assertEqual(timeframe.get_start_time_string(), start_time.isoformat().split(".")[0])
        self.assertEqual(timeframe.get_end_time_string(), end_time.isoformat().split(".")[0])
        self.assertFalse(timeframe.is_update_after_set())

        timeframe.set_update_after(update_after)
        self.assertTrue(timeframe.is_update_after_set())
        self.assertEqual(timeframe.get_update_after_string(), update_after.isoformat().split(".")[0])

    def test_invalid_range(self):
        # End time is earlier than start time
        start_time = datetime.datetime.now() - datetime.timedelta(10)
        end_time = datetime.datetime.now() - datetime.timedelta(20)

        with self.assertRaises(ValueError):
            timeframe = TimeFrame(start_time, end_time)

    def test_setter(self):
        timeframe = TimeFrame(datetime.datetime(2019, 1, 1), datetime.datetime(2020, 1, 1))
        timeframe.set_start_time(datetime.datetime(2019, 12, 1))
        self.assertEqual(timeframe.get_start_time_string(), datetime.datetime(2019, 12, 1).isoformat().split(".")[0])


if __name__ == '__main__':
    unittest.main()
