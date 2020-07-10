import json # for pretty print
from pathlib import Path
import plistlib
import re
import sys
from uuid import uuid4

from fire import Fire  # to remove... eventually

try:
    from .run import run
except ImportError:
    from hickory.run import run

HICKORY_SERVICE = "hickory"

def schedule(file_name, every=10, run_now=False):
    which_python = sys.executable
    working_directory = str(Path.cwd())
    home = str(Path.home())
    hid = uuid4().hex[:6] # hickory_id
    hickory_name = f"{HICKORY_SERVICE}.{hid}.{file_name}"
    # create the plist file
    d = {
        "Label": hickory_name,
        "WorkingDirectory": working_directory,
        "ProgramArguments": [which_python, file_name],
        "StartInterval": every,
        "RunAtLoad": run_now,
        "StandardErrorPath": f"{working_directory}/hickory.log",
        "StandardOutPath": f"{working_directory}/hickory.log",
    }
    # write the plist file
    with open(f"{home}/Library/LaunchAgents/{hickory_name}.plist", "wb") as f:
        plistlib.dump(d, f)
    # schedule
    run(
        f"launchctl load {home}/Library/LaunchAgents/{hickory_name}.plist"
    )


def parse_gui_infodump(info):
    path, stdout, stderr = re.findall("path = (.*?)\n", info)
    name = (
        path.split("/")[-1].replace(f"{HICKORY_SERVICE}.", "").replace(".plist", "")
    )
    return {
        # need
        "name": name,
        "run_interval": re.findall("run interval = (.*?)\n", info)[0],
        "runs": re.findall("runs = (.*?)\n", info)[0],
        "state": re.findall("state = (.*?)\n", info)[0],
        # nice to have
        "script_path": path,
        "last_exit_code": re.findall("last exit code = (.*?)\n", info)[0],
        # probably don't need
        "program": re.findall("program = (.*?)\n", info)[0],
        "working_directory": re.findall("working directory = (.*?)\n", info)[0],
        "environment_path": re.findall("PATH => (.*?)\n", info)[0],
        "stdout": stdout,
        "stderr": stderr,
    }

def all_info():
    uid = run("id -u")
    running = run(f"launchctl list | grep {HICKORY_SERVICE}")
    scripts = [script.split("\t")[-1] for script in running.split("\n")]
    infos = []
    for script in scripts:
        infodump = run(f"launchctl print gui/{uid}/{script}")
        info = parse_gui_infodump(infodump)
        infos.append(info)
    print(json.dumps(infos, indent=2))

def info():
    return run(f"launchctl list | grep {HICKORY_SERVICE}")


def kill(id):
    home = str(Path.home())
    # unload from launchd
    unload = (
        f"launchctl unload {home}/Library/LaunchAgents/{HICKORY_SERVICE}.{id}.plist"
    )
    run(unload)
    # delete the plist file
    run(f"rm {home}/Library/LaunchAgents/{HICKORY_SERVICE}.{id}.plist")


def main():
    Fire({
        "schedule": schedule,
        "list": list,
        "info": all_info,
        "kill": kill
    })


if __name__ == "__main__":
    main()
