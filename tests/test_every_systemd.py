import pytest
from hickory.every_systemd import *

def test_interval_to_on_calendar_string():
    intervals = ["10seconds", "10minutes", "10hours"]
    interval_to_on_calendar_string(i)

day_to_shorthand("monday")
day_to_shorthand("th")
day_to_shorthand("saturday")


day_to_calendar_day("2")
day_to_calendar_day("13")
day_to_calendar_day("31")


day_to_on_calendar_string("monday")
day_to_on_calendar_string("31")
day_to_on_calendar_string("weekday")
day_to_on_calendar_string("eom")


timestamp_to_on_calendar_string("0:01")
timestamp_to_on_calendar_string("12:01am") # broken
timestamp_to_on_calendar_string("1:01am")
timestamp_to_on_calendar_string("12:01pm")
timestamp_to_on_calendar_string("10:01pm")
