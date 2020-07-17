from configparser import ConfigParser
from pathlib import Path
import sys

try:
    from .constants import HICKORY_SERVICE, SYSTEMD_PATH
except ImportError:
    from hickory.constants import HICKORY_SERVICE, SYSTEMD_PATH


def build_service_config(label, working_directory, which_python, script):
    config = ConfigParser()
    config.optionxform = str
    config["Unit"] = {"Description": label}
    config["Service"] = {
        "Type": "oneshot",
        "WorkingDirectory": working_directory,
        "ExecStart": f"{which_python} -u {script}",
    }
    return config


def build_timer_config(label, interval):
    config = ConfigParser()
    config.optionxform = str
    config["Unit"] = {"Description": label}
    # add interval every here
    config["Timer"] = {
        "Unit": f"{label}.service",
        "Persistent": True,
        "AccuracySec": "1s",
        "OnCalendar": interval,  # *:*:0/10
    }
    config["Install"] = {"WantedBy": "timers.target"}
    return config


def dump_config(path, config):
    with open(path, "w") as configfile:
        config.write(configfile, space_around_delimiters=False)


def schedule_sytemd(label, working_directory, which_python, script, interval):
    service = build_service_config(label, working_directory, which_python, script)
    timer = build_timer_config(label, interval)
    Path(SYSTEMD_PATH).mkdir(parents=True, exist_ok=True)
    dump_config(f"{SYSTEMD_PATH}/{label}.service", service)
    dump_config(f"{SYSTEMD_PATH}/{label}.timer", timer)
    run("systemctl --user daemon-reload")
    run(f"systemctl --user enable {label}.timer")
    run(f"systemctl --user start {label}.timer")


def status_systemd():
    return "TODO"
    # return (systemctl --user status hickory_demo.timer)


def kill_systemd(id_or_script):
    for path in Path(SYSTEMD_PATH).glob(f"{HICKORY_SERVICE}*{id_or_script}*"):
        # path = f'{SYSTEMD_PATH}/hickory.7633.foo.py.timer'
        file = path.split("/")[-1]
        if file.endswith("timer"):
            run(f"systemctl --user stop {file}")
            run(f"systemctl --user disable {file}")
            run(f"rm {path}")
        elif file.endswith("service"):
            run(f"rm {path}")
        else:
            continue


#
