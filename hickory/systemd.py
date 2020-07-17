from configparser import ConfigParser
import io
from pathlib import Path
import sys

from .constants import HICKORY_SERVICE, SYSTEMD_PATH
from .every_systemd import every
from .utils import run


def config_to_string(config):
    with io.StringIO() as f:
        config.write(f, space_around_delimiters=False)
        f.seek(0)
        string = f.getvalue()
    return string


def add_on_calendar_strings(string, interval):
    split = string.split("\n\n")
    timer_section = split[1]
    on_calendars = every(interval)
    new_timer_section = timer_section
    for on_calendar in on_calendars:
        new_timer_section += f"\nOnCalendar={on_calendar}"
    split[1] = new_timer_section
    string = "\n\n".join(split).strip()
    return string


def build_timer_string(label, interval):
    config = ConfigParser()
    config.optionxform = str
    config["Unit"] = {"Description": label}
    config["Timer"] = {
        "Unit": f"{label}.service",
        "Persistent": True,
        "AccuracySec": "1s",
    }
    config["Install"] = {"WantedBy": "timers.target"}
    string = config_to_string(config)
    string = add_on_calendar_strings(string, interval)
    return string


def build_service_string(label, working_directory, which_python, script):
    config = ConfigParser()
    config.optionxform = str
    config["Unit"] = {"Description": label}
    config["Service"] = {
        "Type": "oneshot",
        "WorkingDirectory": working_directory,
        "ExecStart": f"{which_python} -u {script}",
    }
    string = config_to_string(config)
    return string


def dump_string(config_string, path):
    with open(path, "w") as f:
        f.write(config_string)


def schedule_systemd(label, working_directory, which_python, script, interval):
    service = build_service_string(label, working_directory, which_python, script)
    timer = build_timer_string(label, interval)
    Path(SYSTEMD_PATH).mkdir(parents=True, exist_ok=True)
    dump_string(service, f"{SYSTEMD_PATH}/{label}.service")
    dump_string(timer, f"{SYSTEMD_PATH}/{label}.timer")
    run("systemctl --user daemon-reload")
    run(f"systemctl --user enable {label}.timer")
    run(f"systemctl --user start {label}.timer")


def status_systemd():
    return "TODO"
    # cd /home/max/.config/systemd/user                      # stuff is going to be in here
    # systemctl --user status hickory.0d99e7.demo.py         # shows last log
    # systemctl --user status hickory.0d99e7.demo.py.timer   # shows if still active
    # journalctl --user-unit hickory.0d99e7.demo.py          # shows full logs ... timer doesn't work
    # systemctl --user list-timers                           # shows active list
    # journalctl -f | grep python


def kill_systemd(id_or_script):
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
