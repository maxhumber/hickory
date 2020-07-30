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


def find_maxlens(info_dicts):
    keys = info_dicts[0].keys()
    maxlens = {key: len(key) for key in keys}
    for info in info_dicts:
        for key in keys:
            current = maxlens[key]
            new = len(str(info[key]))
            if current < new:
                maxlens[key] = new
    return maxlens


def build_strings(keys, info_dicts, maxlens, spacer=2):
    strings = []
    for info in info_dicts:
        string = ""
        for key in keys:
            value = info[key]
            string_part = str(value).ljust(maxlens[key])
            string += string_part + " " * spacer
        strings.append(string.strip())
    return strings


def build_terminal_string(keys, strings, maxlens, spacer=2):
    terminal_string = ""
    for key in keys:
        string_part = key.ljust(maxlens[key])
        terminal_string += string_part + " " * spacer
    terminal_string = terminal_string.upper().strip() + "\n"
    terminal_string += "\n".join(strings)
    return terminal_string


def status_launchd():
    info_dicts = []
    for path in Path(LAUNCHD_PATH).glob(f"*{HICKORY_SERVICE}*"):
        info = _info_from_path(path)
        info_dicts.append(info)
    if info_dicts:
        spacer = 2
        maxlens = find_maxlens(info_dicts)
        keys = ["id", "file", "state", "runs", "interval"]
        strings = build_strings(keys, info_dicts, maxlens, spacer)
        return build_terminal_string(keys, strings, maxlens, spacer)
    else:
        return "No running scripts"


def kill_launchd(id_or_script):
    for file in Path(LAUNCHD_PATH).glob(f"{HICKORY_SERVICE}*{id_or_script}*"):
        run(f"launchctl unload {file}")
        run(f"rm {file}")
