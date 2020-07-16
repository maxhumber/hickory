from configparser import ConfigParser
from pathlib import Path
import sys

try:
    from .constants import HICKORY_SERVICE, SYSTEMD_PATH
except ImportError:
    from hickory.constants import HICKORY_SERVICE, SYSTEMD_PATH


label = 'hickory.foo.py'
working_directory = '/user/max'
which_python = '/home/max/miniconda3/bin/python'
script = 'foo.py'
interval = 'hi'

def build_service_config(label, working_directory, which_python, script):
    config = ConfigParser()
    config.optionxform = str
    config["Unit"] = {"Description": label}
    config["Service"] = {
        "Type": "oneshot",
        "WorkingDirectory": working_directory,
        "ExecStart": f"{which_python} -u {script}"
    }
    return config

def build_timer_dict(label, interval):
    config = ConfigParser()
    config.optionxform = str
    config["Unit"] = {"Description": label}
    config["Timer"] = {
        "Unit": f"{label}.service",
        'Persistent': True,
        'AccuracySec': "1s",
        "OnCalendar": interval # *:*:0/10
    }
    config["Install"] = {"WantedBy": "timers.target"}
    return config


build_timer_dict("foo.py", "*:*:0/10")

def dump_config(label, config):
    path = f'{SYSTEMD_PATH}/{label}.timer'
    with open(path, 'w') as configfile:
        timer.write(configfile)


def schedule_sytemd():
    pass

def status_systemd():
    pass

def kill_systemd():
    pass



## SERVICE



with open('example.service', 'w') as configfile:
    service.write(configfile)

## TIMER
