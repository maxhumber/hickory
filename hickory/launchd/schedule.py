from pathlib import Path
import plistlib
import sys
from uuid import uuid4

from ..constants import HICKORY_SERVICE, LAUNCHD_PATH
from ..launchd.every import every as every_to_dict
from ..shared import run


def generate_launchd_dict(script, every):
    which_python = sys.executable
    working_directory = str(Path.cwd())
    id = uuid4().hex[:6]
    hickory_label = f"{HICKORY_SERVICE}.{id}.{script}"
    launchd_dict = {
        "Label": hickory_label,
        "Every": every,
        "WorkingDirectory": working_directory,
        "ProgramArguments": [which_python, script],
        "RunAtLoad": False,
        "StandardErrorPath": f"{working_directory}/hickory.log",
        "StandardOutPath": f"{working_directory}/hickory.log",
    }
    every_dict = every_to_dict(every)
    launchd_dict.update(every_dict)
    return launchd_dict


def schedule(script, every):
    """DOCTODO // schedule the actual script!"""
    launchd_dict = generate_launchd_dict(script, every)
    path = f"{LAUNCHD_PATH}/{launchd_dict['Label']}.plist"
    with open(f"{path}", "wb") as f:
        plistlib.dump(launchd_dict, f)
    run(f"launchctl load {path}")
