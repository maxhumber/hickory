import plistlib
import re


d = {
    "StartCalendarInterval": {"Hour": int(1), "Minute": int(0)}
}

print(plistlib.dumps(d).decode())

every = [
    "@4:00", "@04:00", "@4:00am", "@4:00pm", "@16:00",
]

def parse_clock(every):
    day, time = every.split("@")
    hour, minute = time.split(":")
    if "am" in minute:
        minute = minute[:-2]
    if "pm" in minute:
        minute = minute[:-2]
        hour = int(hour) + 12
    return {
        "Hour": int(hour),
        "Minute": int(minute)
    }

for e in every:
    r = parse_clock(e)
    print(e, r)

def parse_day(every):
    day, time = every.split("@")
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
        raise Error("Not a day")
    return {'Weekday': int(day_number)}




## every intervals

every = [
    10,"10","10s","10sec", "10secs", "10seconds",
    "30m", "30min", "30mins", "30minutes",
    "2h", "2hour", "2hours"
]

def parse_interval(interval):
    interval = str(interval)
    r = re.findall(r'[A-Za-z]+|\d+', interval)
    if len(r) == 1:
        seconds = int(r[0])
    elif r[1] in ["s", "sec", "secs", "second", "seconds"]:
        seconds = int(r[0])
    elif r[1] in ["m", "min", "mins", "minute", "minutes"]:
        seconds = int(r[0]) * 60
    elif r[1] in ["h", "hour", "hours"]:
        seconds = int(r[0]) * 60 * 60
    else:
        raise Error("Not an interval")
    return seconds

for e in every:
    seconds = parse_interval(e)
    print(e, seconds)



#
