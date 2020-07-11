from itertools import product
import plistlib
import re


class InvalidInterval(Exception):
    pass


class InvalidWeekDay(Exception):
    pass


class InvalidMonthDay(Exception):
    pass


class InvalidTime(Exception):
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
    elif unit in ["h", "hr", "hrs", "hour", "hours"]:
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
    retime = re.findall(r"[A-Za-z]+|\d+", t)
    hour = int(retime[0])
    minute = 0
    if len(retime) == 2:
        if retime[1] == "pm":
            hour += 12
        elif retime[1] == "am":
            pass
        else:
            minute = int(retime[1])
    if len(retime) == 3:
        minute = int(retime[1])
        if retime[2] == "am":
            pass
        elif retime[2] == "pm":
            hour += 12
        else:
            raise InvalidTime(t)
    if not ((0 <= hour <= 23) and (0 <= minute <= 59)):
        raise InvalidTime(t)
    return hour, minute


def disjoin(s):
    days, timestamps = s.split("@")
    days, timestamps = days.split(","), timestamps.split(",")
    return product(days, timestamps)


# special cases
# - day
# - weekday
# - eom

d = {"hi": "bye"}
d.update({})
d


def sort_day(day):
    if day in ["", "day"]:
        return {}
    elif day == "weekday":  # hard
        return "every weekday"
    elif day == "eom":  # hard
        return "End of month"
    elif contains_number(day):
        return "contains number!"
    else:
        return "text day?"


def interval_to_calendar_interval():
    pass


day = "1st"
dir(day)


def every(interval):
    s = interval_to_lower(interval)

    if not contains_number(s):
        raise InvalidInterval(s)

    if "@" not in s:
        return {"StartInterval": interval_to_seconds(s)}

    blocks = []
    for day, timestamp in disjoin(s):
        block = {}
        if day:
            try:
                block["Day"] = day_to_number_in_month(day)
            except ValueError:
                block["Weekday"] = day_to_number_in_week(day)
        hour, minute = time_to_hour_minute(timestamp)
        block["Hour"] = hour
        block["Minute"] = minute
        blocks.append(block)

    if len(blocks) > 1:
        value = blocks
    else:
        value = blocks[0]

    return {"StartCalendarInterval": value}


#
# inputs = ["1st,2nd,3rd@2:30", "m,t@5:30", '@4:30']
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
