from itertools import product
import plistlib
import re


class InvalidInterval(Exception):
    pass


class InvalidWeekDay(Exception):
    pass


class InvalidMonthDay(Exception):
    pass


def interval_to_lower(interval):
    return str(interval).lower()


def strip_number(s):
    return re.sub("[^0-9]", "", s)


def contains_number(s):
    return bool(strip_number(s))


def interval_to_components(interval):
    c = re.findall(r"[A-Za-z]+|\d+", interval)
    try:
        value = int(c[0])
    except ValueError:
        raise InvalidInterval(interval) from None
    unit = "s" if len(c) == 1 else c[1]
    return value, unit


def interval_to_seconds(interval):
    value, unit = interval_to_components(interval)
    if unit in ["s", "sec", "secs", "second", "seconds"]:
        seconds = value
    elif unit in ["m", "min", "mins", "minute", "minutes"]:
        seconds = value * 60
    elif unit in ["h", "hr", "hour", "hours"]:
        seconds = value * 60 * 60
    else:
        raise InvalidInterval(interval) from None
    return seconds


def day_to_number_in_week(day):
    if day in ["m", "mon", "monday"]:
        day_number = 1
    elif day in ["t", "tue", "tues", "tuesday"]:
        day_number = 2
    elif day in ["w", "wed", "weds", "wednesday"]:
        day_number = 3
    elif day in ["th", "thur", "thurs", "thursday"]:
        day_number = 4
    elif day in ["f", "fri", "friday"]:
        day_number = 5
    elif day in ["s", "sat", "saturday"]:
        day_number = 6
    elif day in ["su", "sun", "sunday"]:
        day_number = 7
    else:
        raise InvalidWeekDay(day)
    return day_number


def day_to_number_in_month(day):
    number = int(strip_number(day))
    if 1 <= number <= 31:
        return number
    else:
        raise InvalidMonthDay(day)


def time_to_hour_minute(t):
    hour, minute = t.split(":")
    if "am" in minute:
        minute = minute[:-2]
    if "pm" in minute:
        minute = minute[:-2]
        hour = hour + 12
    return int(hour), int(minute)


def every(interval):
    s = interval_to_lower(interval)

    if not contains_number(s):
        raise InvalidInterval(s)

    if "@" not in s:
        seconds = interval_to_seconds(s)
        return {"StartInterval": seconds}

    days, timestamps = s.split("@")
    days, timestamps = days.split(","), timestamps.split(",")
    combos = product(days, timestamps)

    blocks = []
    for day, timestamp in combos:
        block = {}
        if day:
            try:
                block["Day"] = day_to_number_in_month(day)
            except ValueError:
                block["Weekday"] = day_to_number_in_week(day)
        hour, minute = timestamp_to_hour_minute(timestamp)
        block["Hour"] = hour
        block["Minute"] = minute
        blocks.append(block)

    if len(blocks) > 1:
        return {"StartCalendarInterval": blocks}
    else:
        return {"StartCalendarInterval": blocks[0]}


#
# inputs = ['lol', "1st,2nd,3rd@2:30", "m,t@5:30", '@4:30']
#
# for i in inputs:
#     d = every(i)
#     print(d)
#     # print(d)
#     print(plistlib.dumps(d).decode())

# # plist dump
# d = {"StartCalendarInterval": {"Hour": int(1), "Minute": int(0)}}
# print(plistlib.dumps(d).decode())
# ############
