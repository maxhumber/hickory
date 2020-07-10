import plistlib
import re
from itertools import product

# plist dump
d = {"StartCalendarInterval": {"Hour": int(1), "Minute": int(0)}}
print(plistlib.dumps(d).decode())
############

def interval_to_seconds(interval):
    interval = str(interval)
    l = re.findall(r"[A-Za-z]+|\d+", interval)
    if len(l) == 1:
        seconds = int(l[0])
    elif l[1] in ["s", "sec", "secs", "second", "seconds"]:
        seconds = int(l[0])
    elif l[1] in ["m", "min", "mins", "minute", "minutes"]:
        seconds = int(l[0]) * 60
    elif l[1] in ["h", "hr", "hour", "hours"]:
        seconds = int(l[0]) * 60 * 60
    else:
        raise Exception("Not an Interval")
    return seconds


def day_to_number(day):
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
        raise Exception("Not a day")
    return day_number


def timestamp_to_hour_minute(timestamp):
    hour, minute = timestamp.split(":")
    if "am" in minute:
        minute = minute[:-2]
    if "pm" in minute:
        minute = minute[:-2]
        hour = int(hour) + 12
    return int(hour), int(minute)


def every(string):
    s = str(string)

    if '@' not in s:
        seconds = interval_to_seconds(s)
        return {"StartInterval": seconds}

    days, timestamps = s.split("@")
    days, timestamps = days.split(','), timestamps.split(',')
    combos = product(days, timestamps)

    blocks = []
    for day, timestamp in combos:
        block = {}
        if day:
            block['Weekday'] = day_to_number(day)
        hour, minute = timestamp_to_hour_minute(timestamp)
        block['Hour'] = hour
        block['Minute'] = minute
        blocks.append(block)

    if len(blocks) > 1:
        return {'StartCalendarInterval': blocks}
    else:
        return {'StartCalendarInterval': blocks[0]}

inputs = ["10hr", "10", "m,t@5:30", '@4:30']

for i in inputs:
    d = every(i)
    # print(d)
    print(plistlib.dumps(d).decode())
