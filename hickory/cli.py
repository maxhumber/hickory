import json
from pathlib import Path
import plistlib
import re
import sys
from uuid import uuid4

from fire import Fire

try:
    from .every import every as every_to_dict
    from .run import run
except ImportError:
    # FOR TESTING
    from hickory.every import every as every_to_dict
    from hickory.run import run


USER_HOME = str(Path.home())
USER_ID = run("id -u")
LAUNCHD_PATH = f"{USER_HOME}/Library/LaunchAgents"
HICKORY_SERVICE = "hickory"


def generate_launchd_dict(script, every):
    """
    DOCTODO // Build launchd compatible dictionary
    """
    which_python = sys.executable
    working_directory = str(Path.cwd())
    hid = uuid4().hex[:6]
    hickory_label = f"{HICKORY_SERVICE}.{hid}.{script}"
    launchd_dict = {
        "Label": hickory_label,
        "Every": every,
        "WorkingDirectory": working_directory,
        "ProgramArguments": [which_python, script],
        "RunAtLoad": False,
        "StandardErrorPath": f"{working_directory}/hickory.log",
        "StandardOutPath": f"{working_directory}/hickory.log",
    }
    launchd_dict.update(every_to_dict(every))
    return launchd_dict


def schedule(script, every):
    """
    DOCTODO // schedule the actual script!
    """
    if not Path(script).exists():
        raise FileNotFoundError(script)
    launchd_dict = generate_launchd_dict(script, every)
    path = f"{LAUNCHD_PATH}/{launchd_dict['Label']}.plist"
    with open(f"{path}", "wb") as f:
        plistlib.dump(launchd_dict, f)
    run(f"launchctl load {path}")


def kill(id_or_script):
    """
    DOCTODO // kill (stop and delete) the scheduler for script name or id
    """
    for file in Path(LAUNCHD_PATH).glob(f"{HICKORY_SERVICE}*{id_or_script}*"):
        run(f"launchctl unload {file}")
        run(f"rm {file}")


def info_from_path(path):
    """
    DOCTODO // Info abnout the running script
    """
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


def main():
    Fire(
        {
            "schedule": schedule,
            "list": list,  # for debugging
            "status": status,
            "kill": kill,
        }
    )


if __name__ == "__main__":
    main()
