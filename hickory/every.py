from itertools import product
import plistlib
import re


class InvalidInterval(Exception):
    pass


class InvalidWeekday(Exception):
    pass


class InvalidCalendarDay(Exception):
    pass


class InvalidTime(Exception):
    pass


def strip_number(s):
    try:
        return int(re.sub("[^0-9]", "", s))
    except ValueError:
        return None


def contains_number(string):
    return bool(strip_number(string))


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
    elif unit in ["h", "hr", "hrs", "hour", "hours"]:
        seconds = value * 60 * 60
    else:
        raise InvalidInterval(interval) from None
    return seconds


def start_interval(interval):
    return {"StartInterval": interval_to_seconds(interval)}


def day_to_weekday_dict(day):
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
        raise InvalidWeekday(day)
    return {"Weekday": day_number}


def day_to_calendar_day_dict(day):
    number = strip_number(day)
    if not (1 <= number <= 31):
        raise InvalidCalendarDay(day)
    return {"Day": number}


def weekday_to_list():
    return 'm,t,w,th,f'.split(',')


def eom_dict():
    eom_days = [
        (1, 31),
        (2, 28),
        (3, 31),
        (4, 30),
        (5, 31),
        (6, 30),
        (7, 31),
        (8, 31),
        (9, 30),
        (10, 31),
        (11, 30),
        (12, 31),
    ]
    return [{"Day": day, "Month": month} for month, day in eom_days]

def day_to_dict(day):
    if day in ["", "day"]:
        return {}
    # TODO
    # elif day == "weekday":
    #     return "every weekday"
    elif day == "eom":
        return eom_dict()
    elif contains_number(day):
        return day_to_calendar_day_dict(day)
    else:
        return day_to_weekday_dict(day)


def timestamp_to_dict(t):
    rt = re.findall(r"[A-Za-z]+|\d+", t)
    hour = int(rt[0])
    minute = 0
    if len(rt) == 2:
        if rt[1] == "pm":
            hour += 12
        elif rt[1] == "am":
            pass
        else:
            minute = int(rt[1])
    if len(rt) == 3:
        minute = int(rt[1])
        if rt[2] == "am":
            pass
        elif rt[2] == "pm":
            hour += 12
        else:
            raise InvalidTime(t)
    if not ((0 <= hour <= 23) and (0 <= minute <= 59)):
        raise InvalidTime(t)
    return {"Hour": hour, "Minute": minute}

def disjoin(interval):
    days, timestamps = interval.split("@")
    days, timestamps = days.split(","), timestamps.split(",")
    return product(days, timestamps)

def start_calendar_interval(interval):
    blocks = []
    for day, timestamp in disjoin(interval):
        block = {}
        block.update(day_to_dict(day))
        block.update(timestamp_to_dict(timestamp))
        blocks.append(block)
    if len(blocks) > 1:
        value = blocks
    else:
        value = blocks[0]
    return {"StartCalendarInterval": value}


def every(interval):
    interval = str(interval).lower()
    if "@" not in interval:
        return start_interval(interval)
    else:
        return start_calendar_interval(interval)


# # plist dump
# d = {"StartCalendarInterval": {"Hour": int(1), "Minute": int(0)}}
# print(plistlib.dumps(d).decode())
# ############
