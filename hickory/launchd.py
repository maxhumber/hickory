from pathlib import Path
import plistlib
import re

from .constants import HICKORY_SERVICE, LAUNCHD_PATH
from .every_launchd import every
from .utils import run


def _build_dict(label, working_directory, which_python, script, interval):
    ldd = {
        "Label": label,
        "WorkingDirectory": working_directory,
        "ProgramArguments": [which_python, script],
        "StandardOutPath": f"{working_directory}/hickory.log",
        "StandardErrorPath": f"{working_directory}/hickory.log",
        "RunAtLoad": False,
    }
    ldd.update(every(interval))
    return ldd


def _dump_dict(ldd):
    path = f"{LAUNCHD_PATH}/{ldd['Label']}.plist"
    with open(f"{path}", "wb") as f:
        plistlib.dump(ldd, f)
    return path


def _info_from_path(path):
    with open(path, "rb") as f:
        ldd = plistlib.load(f)
    script = ldd["Label"]
    split = script.split(".")
    user_id = run("id -u")
    info = run(f"launchctl print gui/{user_id}/{script}")
    interval = ldd.get("StartInterval") or ldd.get("StartCalendarInterval")
    state = re.findall("state = (.*?)\n", info)[0]
    return {
        "id": split[1],
        "file": ".".join(split[2:]),
        "runs": re.findall("runs = (.*?)\n", info)[0],
        "state": state,
        "interval": interval,
    }


def schedule_launchd(label, working_directory, which_python, script, interval):
    ldd = _build_dict(label, working_directory, which_python, script, interval)
    path = _dump_dict(ldd)
    run(f"launchctl load {path}")


def status_launchd():
    terminal_string = "id     - file   - state   - runs - interval".upper()
    for path in Path(LAUNCHD_PATH).glob(f"*{HICKORY_SERVICE}*"):
        i = _info_from_path(path)
        s = f"\n{i['id']} - {i['file']} - {i['state']} - {i['runs']} - {i['interval']}"
        terminal_string = terminal_string + s
    return terminal_string


def kill_launchd(id_or_script):
    for file in Path(LAUNCHD_PATH).glob(f"{HICKORY_SERVICE}*{id_or_script}*"):
        run(f"launchctl unload {file}")
        run(f"rm {file}")
