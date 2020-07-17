from itertools import product
import re
import subprocess


class HickoryError(Exception):
    pass


def run(command, output=True, silent=False):
    if silent:
        command += " --quiet"
    if output:
        s = subprocess.run(command, capture_output=True, shell=True)
        subprocess.run("id -u", capture_output=True, shell=True).stdout.decode(
            "utf-8"
        ).strip()
        o = s.stdout.decode("utf-8").strip()
        return o
    subprocess.run(command, shell=True)


def strip_number(s):
    try:
        return int(re.sub("[^0-9]", "", s))
    except ValueError:
        return None


def contains_number(string):
    return bool(strip_number(string))


def interval_to_tuple(interval):
    c = re.findall(r"[A-Za-z]+|\d+", interval)
    try:
        value = int(c[0])
    except (ValueError, IndexError):
        raise HickoryError(f"Invalid interval: {interval}") from None
    unit = "s" if len(c) == 1 else c[1]
    return value, unit


def timestamp_to_tuple(t):
    rt = re.findall(r"[A-Za-z]+|\d+", t)
    try:
        hour = int(rt[0])
    except (ValueError, IndexError):
        raise HickoryError(f"Invalid time: {t}") from None
    minute = 0
    if len(rt) == 2:
        if rt[1] == "pm":
            if hour != 12:
                hour += 12
        elif rt[1] == "am":
            if hour == 12:
                hour = 0
        else:
            minute = int(rt[1])
    if len(rt) == 3:
        minute = int(rt[1])
        if rt[2] == "am":
            if hour == 12:
                hour = 0
        elif rt[2] == "pm":
            if hour != 12:
                hour += 12
        else:
            raise HickoryError(f"Invalid time: {t}")
    if not ((0 <= hour <= 23) and (0 <= minute <= 59)):
        raise HickoryError(f"Invalid time: {t}")
    return hour, minute


def disjoin(interval):
    try:
        days, timestamps = interval.split("@")
    except ValueError:
        raise HickoryError(f"Invalid time: {interval}") from None
    days, timestamps = days.split(","), timestamps.split(",")
    return list(product(days, timestamps))
