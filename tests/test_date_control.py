import time

from BigCalendar.utility.date_control import *


def test_date_to_unixtime():
    date_to_unixtime(year=2018, month=3, day=16)
    print(time.time())
