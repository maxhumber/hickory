import re
import plistlib
import subprocess
import sys
from pathlib import Path

from fire import Fire  # to remove... eventually

hickory_identifier = "hickory"


def run(command, output=True, silent=False):
    if silent:
        command += " --quiet"
    if output:
        s = subprocess.run(command, capture_output=True, shell=True)
        o = s.stdout.decode("utf-8").strip()
        return o
    subprocess.run(command, shell=True)


def parse_gui_infodump(info):
    path, stdout, stderr = re.findall("path = (.*?)\n", info)
    name = (
        path.split("/")[-1].replace(f"{hickory_identifier}.", "").replace(".plist", "")
    )
    return {
        # need
        "name": name,
        "run_interval": re.findall("run interval = (.*?)\n", info)[0],
        "runs": re.findall("runs = (.*?)\n", info)[0],
        "state": re.findall("state = (.*?)\n", info)[0],
        # nice to have
        "script_path": path,
        "last_exit_code": int(re.findall("last exit code = (.*?)\n", info)[0]),
        # probably don't need
        "program": re.findall("program = (.*?)\n", info)[0],
        "working_directory": re.findall("working directory = (.*?)\n", info)[0],
        "environment_path": re.findall("PATH => (.*?)\n", info)[0],
        "stdout": stdout,
        "stderr": stderr,
    }


def all_info():
    uid = run("id -u")
    running = run(f"launchctl list | grep {hickory_identifier}")
    scripts = [script.split("\t")[-1] for script in running.split("\n")]
    infos = []
    for script in scripts:
        infodump = run(f"launchctl print gui/{uid}/{script}")
        info = parse_gui_infodump(infodump)
        infos.append(info)
    return infos


def schedule(file_name, every=10, run_now=False):
    which_python = sys.executable
    working_directory = str(Path.cwd())
    home = str(Path.home())
    # create the plist file
    d = {
        "Label": f"{hickory_identifier}.{file_name}",  # use filename
        "WorkingDirectory": working_directory,  # add working directory
        "ProgramArguments": [which_python, file_name],
        "StartInterval": every,
        "RunAtLoad": run_now,
        "StandardErrorPath": f"{working_directory}/hickory.log",
        "StandardOutPath": f"{working_directory}/hickory.log",
    }
    # write the plist file
    with open(f"{home}/Library/LaunchAgents/{d['Label']}.plist", "wb") as f:
        plistlib.dump(d, f)
    # schedule
    run(
        f"launchctl load {home}/Library/LaunchAgents/{hickory_identifier}.{file_name}.plist"
    )


def list():
    return run(f"launchctl list | grep {hickory_identifier}")


def kill(id):
    home = str(Path.home())
    # unload from launchd
    unload = (
        f"launchctl unload {home}/Library/LaunchAgents/{hickory_identifier}.{id}.plist"
    )
    run(unload)
    # delete the plist file
    run(f"rm {home}/Library/LaunchAgents/{hickory_identifier}.{id}.plist")


def main():
    Fire({"schedule": schedule, "list": list, "kill": kill})


if __name__ == "__main__":
    main()
