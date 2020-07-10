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

#TODO below

times = ['20', '8', '8am', "8:30", '8:30am', '8:30pm', '20:30']

def to_hour_minute(t):
    # t = '8:30pm'
    retime = re.findall(r"[A-Za-z]+|\d+", t)
    hour = int(retime[0])
    minute = 0
    if len(retime) == 2:
        if retime[1] == 'pm':
            hour += 12
        elif retime[1] == 'am':
            pass
        else:
            minute = int(retime[1])
    if len(retime) == 3:
        minute = int(retime[1])
        if retime[2] == 'am':
            pass
        elif retime[2] == 'pm':
            hour += 12
        else:
            raise InvalidTime(t)
    if not (0 <= hour <= 23) and (0 <= minute <= 59):
        raise InvalidTime(t)
    return hour, minute


for t in times:
    print(t, '->', to_hour_minute(t))

    c = re.findall(r"[A-Za-z]+|\d+", t)
    print(c)
    print("->", t.split(":"))
    print(c, "->", t.split(":"))

t = '8am'
if not ':' in t:
    parsed = re.findall(r"[A-Za-z]+|\d+", t)
hour_minute = t.split(':')
hour = hour_minute[0]


hour = parsed[0]

[hour, minute, abrv]

def time_to_hour_minute_abrv():
    pass



def time_to_hour_minute(t):
    t = '8'
    hour, minute = t.split(":")
    if "am" in minute:
        minute = minute[:-2]
    if "pm" in minute:
        minute = minute[:-2]
        hour = hour + 12
    return int(hour), int(minute)


    # print(time_to_hour_minute(t))

def generate_day_timestamp_combos(s):
    days, timestamps = s.split("@")
    days, timestamps = days.split(","), timestamps.split(",")
    combos = product(days, timestamps)
    return combos

def every(interval):
    s = interval_to_lower(interval)

    if not contains_number(s):
        raise InvalidInterval(s)

    if "@" not in s:
        return {"StartInterval": interval_to_seconds(s)}

    combos = generate_day_timestamp_combos(s)

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
