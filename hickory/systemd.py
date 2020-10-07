import io
import re
import subprocess
import sys
from configparser import ConfigParser
from pathlib import Path
from typing import Any, Dict, List, Tuple

from .constants import HICKORY_SERVICE, SYSTEMD_PATH
from .every_systemd import every
from .format_status import format_status
from .utils import run

HOME = str(Path.home())


def config_to_string(config: ConfigParser) -> str:
    with io.StringIO() as f:
        config.write(f, space_around_delimiters=False)
        f.seek(0)
        string = f.getvalue()
    return string


def add_on_calendar_strings(string: str, interval: str) -> str:
    split = string.split("\n\n")
    timer_section = split[1]
    on_calendars = every(interval)
    new_timer_section = timer_section
    for on_calendar in on_calendars:
        new_timer_section += f"\nOnCalendar={on_calendar}"
    split[1] = new_timer_section
    string = "\n\n".join(split).strip()
    return string


def build_timer_string(label: str, interval: str) -> str:
    config = ConfigParser()
    config.optionxform = str  # type: ignore
    config["Unit"] = {"Description": label}
    config["Timer"] = {
        "Unit": f"{label}.service",
        "Persistent": True,  # type: ignore
        "AccuracySec": "1s",
    }
    config["Install"] = {"WantedBy": "timers.target"}
    string = config_to_string(config)
    string = add_on_calendar_strings(string, interval)
    return string


def build_service_string(
    label: str, working_directory: str, which_python: str, script: str
) -> str:
    config = ConfigParser()
    config.optionxform = str  # type: ignore
    config["Unit"] = {"Description": label}
    config["Service"] = {
        "Type": "oneshot",
        "WorkingDirectory": working_directory,
        "ExecStart": f"{which_python} -u {script}",
    }
    string = config_to_string(config)
    return string


def dump_string(config_string: str, path: str) -> None:
    with open(path, "w") as f:
        f.write(config_string)


def schedule_systemd(
    label: str, working_directory: str, which_python: str, script: str, interval: str
) -> None:
    service = build_service_string(label, working_directory, which_python, script)
    timer = build_timer_string(label, interval)
    Path(SYSTEMD_PATH).mkdir(parents=True, exist_ok=True)
    dump_string(service, f"{SYSTEMD_PATH}/{label}.service")
    dump_string(timer, f"{SYSTEMD_PATH}/{label}.timer")
    run("systemctl --user daemon-reload")
    run(f"systemctl --user enable {label}.timer")
    run(f"systemctl --user start {label}.timer")


def _find_all_hickory_services() -> List[str]:
    services = []
    for path in Path(SYSTEMD_PATH).glob(f"*{HICKORY_SERVICE}*service"):
        services.append(path)
    return [str(s) for s in services]


def _find_interval(service: str) -> str:
    timer = subprocess.run(
        f"cat {service.replace('.service', '.timer')}", shell=True, capture_output=True
    )
    timer_str = timer.stdout.decode()
    interval = re.findall("OnCalendar=(.*?)\n", timer_str)[0]
    return interval


def _extract_metadata(service: str) -> Tuple[str, str, str]:
    short = service.split(".service")[0].split("user/")[-1]
    _, id, file, extension = short.split(".")
    script = f"{file}.{extension}"
    return short, id, script


def _find_state(short: str) -> str:
    output = subprocess.run(
        f"systemctl --user status {short}.timer", shell=True, capture_output=True
    )
    status = output.stdout.decode("utf-8")
    state = re.findall("Active: (.*?)\n", status)[0]
    state = state.split(" since ")[0]
    return state


def _find_runs(id: str) -> str:
    output = subprocess.run(
        f"journalctl | grep Starting | grep {id} | wc -l",
        shell=True,
        capture_output=True,
    )
    runs = output.stdout.decode("utf-8").strip()
    return runs


def _service_info(service: str) -> Dict[str, str]:
    short, id, file = _extract_metadata(service)
    state = _find_state(short)
    runs = _find_runs(id)
    interval = _find_interval(service)
    return {"id": id, "file": file, "state": state, "runs": runs, "interval": interval}


def status_systemd() -> str:
    services = _find_all_hickory_services()
    info_dicts = [_service_info(s) for s in services]
    if info_dicts:
        status = format_status(info_dicts)
        return status
    else:
        return "No running scripts..."


def kill_systemd(id_or_script: str) -> None:
    for path in Path(SYSTEMD_PATH).glob(f"{HICKORY_SERVICE}*{id_or_script}*"):
        file = str(path).split("/")[-1]
        if file.endswith("timer"):
            run(f"systemctl --user stop {file}")
            run(f"systemctl --user disable {file}")
            run(f"rm {path}")
        elif file.endswith("service"):
            run(f"rm {path}")
        else:
            continue
