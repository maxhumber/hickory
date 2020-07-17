import re

from .utils import (
    HickoryError,
    strip_number,
    contains_number,
    interval_to_tuple,
    timestamp_to_tuple,
    disjoin,
)


def interval_to_on_calendar_strings(interval):
    value, unit = interval_to_tuple(interval)
    if unit in ["s", "sec", "secs", "second", "seconds"]:
        string = f"*:*:0/{value}"
    elif unit in ["m", "min", "mins", "minute", "minutes"]:
        string = f"*:0/{value}"
    elif unit in ["h", "hr", "hrs", "hour", "hours"]:
        string = f"0/{value}:00:00"
    else:
        raise HickoryError(f"Invalid interval: {interval}")
    return [string]


def day_to_shorthand(day):
    if day in ["m", "mon", "monday"]:
        day_shorthand = "Mon"
    elif day in ["t", "tue", "tues", "tuesday"]:
        day_shorthand = "Tue"
    elif day in ["w", "wed", "weds", "wednesday"]:
        day_shorthand = "Wed"
    elif day in ["th", "thu", "thur", "thurs", "thursday"]:
        day_shorthand = "Thu"
    elif day in ["f", "fri", "friday"]:
        day_shorthand = "Fri"
    elif day in ["s", "sat", "saturday"]:
        day_shorthand = "Sat"
    elif day in ["su", "sun", "sunday"]:
        day_shorthand = "Sun"
    else:
        raise HickoryError(f"Invalid weekday: {day}")
    return day_shorthand


def day_to_calendar_day(day):
    number = strip_number(day)
    if not (1 <= number <= 31):
        raise HickoryError(f"Invalid calendar day: {day}")
    return f"*-*-{str(number).zfill(2)}"


def day_to_on_calendar_string(day):
    if day in ["", "day"]:
        return "*-*-*"
    elif day == "weekday":
        return "Mon..Fri"
    elif day == "eom":
        return "*-*~01"
    elif contains_number(day):
        return day_to_calendar_day(day)
    else:
        return day_to_shorthand(day)


def timestamp_to_on_calendar_string(t):
    hour, minute = timestamp_to_tuple(t)
    string = f"{str(hour).zfill(2)}:{str(minute).zfill(2)}:00"
    return string


def datetime_interval_to_on_calendar_strings(interval):
    on_calendar_strings = []
    for day, timestamp in disjoin(interval):
        day = day_to_on_calendar_string(day)
        timestamp = timestamp_to_on_calendar_string(timestamp)
        on_calendar_strings.append(f"{day} {timestamp}")
    return on_calendar_strings


def every(interval):
    interval = str(interval).lower()
    if "@" not in interval:
        return interval_to_on_calendar_strings(interval)
    else:
        return datetime_interval_to_on_calendar_strings(interval)
