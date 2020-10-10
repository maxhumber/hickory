import plistlib
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


from .every_launchd import every
from .format_status import format_status
from .utils import run

from log import write_log
from decouple import config

HICKORY_SERVICE=config('HICKORY_SERVICE')
LAUNCHD_PATH=config('LAUNCHD_PATH')

def _build_dict(
    label: str, working_directory: str, which_python: str, script: str, interval: str
) -> Dict[str, Any]:
    launchd_dict = {
        "Label": label,
        "WorkingDirectory": working_directory,
        "ProgramArguments": [which_python, script],
        "StandardOutPath": f"{working_directory}/hickory.log",
        "StandardErrorPath": f"{working_directory}/hickory.log",
        "RunAtLoad": False,
    }
    launchd_dict.update(every(interval))
    return launchd_dict


def _dump_dict(launchd_dict: Dict[str, Any]) -> str:
    path = f"{LAUNCHD_PATH}/{launchd_dict['Label']}.plist"
    write_log('File Dumped !')
    with open(f"{path}", "wb") as f:
        plistlib.dump(launchd_dict, f)
    return path


def _service_info(path: Path) -> Dict[str, Any]:
    with open(path, "rb") as f:
        launchd_dict = plistlib.load(f)
    script = launchd_dict["Label"]
    split = script.split(".")
    user_id = run("id -u")
    info = run(f"launchctl print gui/{user_id}/{script}")
    interval = launchd_dict.get("StartInterval") or launchd_dict.get(
        "StartCalendarInterval"
    )
    state = re.findall("state = (.*?)\n", info)[0]  # type: ignore
    runs = re.findall("runs = (.*?)\n", info)[0]  # type: ignore
    return {
        "id": split[1],
        "file": ".".join(split[2:]),
        "runs": runs,
        "state": state,
        "interval": interval,
    }


def schedule_launchd(
    label: str, working_directory: str, which_python: str, script: str, interval: str
) -> None:
    launchd_dict = _build_dict(label, working_directory, which_python, script, interval)
    path = _dump_dict(launchd_dict)
    run(f"launchctl load {path}")


def status_launchd() -> str:
    paths = []
    for path in Path(LAUNCHD_PATH).glob(f"*{HICKORY_SERVICE}*"):
        paths.append(path)
    info_dicts = [_service_info(path) for path in paths]
    if info_dicts:
        status = format_status(info_dicts)
        write_log(status)
        return status
    else:
        write_log("No running scripts...")
        return "No running scripts..."


def kill_launchd(id_or_script: str) -> None:
    for file in Path(LAUNCHD_PATH).glob(f"{HICKORY_SERVICE}*{id_or_script}*"):
        run(f"launchctl unload {file}")
        run(f"rm {file}")
