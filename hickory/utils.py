import re
import sys
import traceback
import subprocess
from itertools import product
from typing import List, Optional, Tuple, Type
from colorama import Fore, Style


class HickoryError(Exception):
    pass


def run(command: str, output: bool = True, silent: bool = False) -> Optional[str]:
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
    return None


def strip_number(s: str) -> Optional[int]:
    try:
        return int(re.sub("[^0-9]", "", s))
    except ValueError:
        return None


def contains_number(string: str) -> bool:
    return bool(strip_number(string))


def interval_to_tuple(interval: str) -> Tuple[int, str]:
    c = re.findall(r"[A-Za-z]+|\d+", interval)
    try:
        value = int(c[0])
    except (ValueError, IndexError):
        raise HickoryError(f"Invalid interval: {interval}") from None
    unit = "s" if len(c) == 1 else c[1]
    return value, unit


def timestamp_to_tuple(t: str) -> Tuple[int, int]:
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


def disjoin(interval: str) -> List[Tuple[str, str]]:
    try:
        days, timestamps = interval.split("@")
    except ValueError:
        raise HickoryError(f"Invalid time: {interval}") from None
    list_days, list_timestamps = days.split(","), timestamps.split(",")
    return list(product(list_days, list_timestamps))


def pretty_print_exception(
    e: Exception,
    eligible: Tuple[Type[Exception], ...] = (OSError, FileNotFoundError, HickoryError)
):
    msg, *args = e.args
    if not isinstance(e, eligible):
        print(*traceback.format_exc().split('\n')[:-2], sep='\n')
    print(
        f"{Fore.LIGHTRED_EX}[{Style.BRIGHT}%s{Style.NORMAL}] %s%s{Fore.RESET}" % (
            type(e).__name__, msg, args and f': {str(args).strip("[]")}' or ''
        ),
        file=sys.stderr
    )
