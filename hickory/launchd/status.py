from pathlib import Path
import plistlib
import re

from ..constants import HICKORY_SERVICE, USER_ID, LAUNCHD_PATH
from ..shared import run


def info_from_path(path):
    with open(path, "rb") as f:
        launchd_dict = plistlib.load(f)
    script = launchd_dict["Label"]
    split = script.split(".")
    info = run(f"launchctl print gui/{USER_ID}/{script}")
    return {
        "hid": split[1],
        "file": ".".join(split[2:]),
        "every": launchd_dict["Every"],
        "runs": re.findall("runs = (.*?)\n", info)[0],
        "state": re.findall("state = (.*?)\n", info)[0],
    }


def status():
    """
    # HID   FILE     RUNS   STATE    INTERVAL
    # 3300  bar.py   17     waiting  10 seconds
    """
    terminal_string = "hid    - file   - state   - runs - interval".upper()
    for path in Path(LAUNCHD_PATH).glob(f"*{HICKORY_SERVICE}*"):
        i = info_from_path(path)
        s = f"\n{i['hid']} - {i['file']} - {i['state']} - {i['runs']} - {i['every']}"
        terminal_string = terminal_string + s
    return terminal_string


def list():
    return run(f"launchctl list | grep {HICKORY_SERVICE}")
