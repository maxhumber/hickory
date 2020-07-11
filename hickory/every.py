from itertools import product
import plistlib
import re


class HickoryError(Exception):
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
    except (ValueError, IndexError):
        raise HickoryError(f"Invalid interval: {interval}") from None
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
        raise HickoryError(f"Invalid interval: {interval}")
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
        raise HickoryError(f"Invalid weekday: {day}")
    return {"Weekday": day_number}


def day_to_calendar_day_dict(day):
    number = strip_number(day)
    if not (1 <= number <= 31):
        raise HickoryError(f"Invalid calendar day: {day}")
    return {"Day": number}


def weekday_list_dict():
    return [{"Weekday": i} for i in range(1, 5 + 1)]


def eom_list_dict():
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


def day_to_list_dict(day):
    if day in ["", "day"]:
        return [{}]
    elif day == "weekday":
        return weekday_list_dict()
    elif day == "eom":
        return eom_list_dict()
    elif contains_number(day):
        return [day_to_calendar_day_dict(day)]
    else:
        return [day_to_weekday_dict(day)]


def timestamp_to_dict(t):
    rt = re.findall(r"[A-Za-z]+|\d+", t)
    try:
        hour = int(rt[0])
    except (ValueError, IndexError):
        raise HickoryError(f"Invalid time: {t}") from None
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
            raise HickoryError(f"Invalid time: {t}")
    if not ((0 <= hour <= 23) and (0 <= minute <= 59)):
        raise HickoryError(f"Invalid time: {t}")
    return {"Hour": hour, "Minute": minute}


def disjoin(interval):
    try:
        days, timestamps = interval.split("@")
    except ValueError:
        raise HickoryError(f"Invalid time: {interval}") from None
    days, timestamps = days.split(","), timestamps.split(",")
    return product(days, timestamps)


def start_calendar_interval(interval):
    blocks = []
    for day, timestamp in disjoin(interval):
        days = day_to_list_dict(day)
        timestamp = timestamp_to_dict(timestamp)
        for day in days:
            block = {}
            block.update(day)
            block.update(timestamp)
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
