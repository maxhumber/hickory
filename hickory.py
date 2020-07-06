import plistlib
import io
import subprocess
import uuid
import sys
from pathlib import Path

from fire import Fire # to remove... eventually

hickory_identifier = "hickory"

def run(command, output=True, silent=False):
    if silent:
        command += ' --quiet'
    if output:
        s = subprocess.run(command, capture_output=True, shell=True)
        o = s.stdout.decode('utf-8').strip()
        return o
    subprocess.run(command, shell=True)

def schedule(file_name, interval=10, run_at_load=True):
    which_python = sys.executable
    working_directory = str(Path.cwd())
    home = str(Path.home())
    # create the plist file
    d = {
        "Label": f"{hickory_identifier}.{file_name}", # use filename
        "WorkingDirectory": working_directory, # add working directory
        "ProgramArguments": [which_python, file_name],
        "StartInterval": interval,
        "RunAtLoad": run_at_load,
        "StandardErrorPath": f"{working_directory}/hickory.log",
        "StandardOutPath": f"{working_directory}/hickory.log"
    }
    # write the plist file
    with open(f"{home}/Library/LaunchAgents/{d['Label']}.plist", "wb") as f:
        plistlib.dump(d, f)
    # schedule
    run(f"launchctl load {home}/Library/LaunchAgents/{hickory_identifier}.{file_name}.plist")

def list():
    return run(f"launchctl list | grep {hickory_identifier}")

def kill(id):
    home = str(Path.home())
    # unload from launchd
    unload = f"launchctl unload {home}/Library/LaunchAgents/{hickory_identifier}.{id}.plist"
    run(unload)
    # delete the plist file
    run(f"rm {home}/Library/LaunchAgents/{hickory_identifier}.{id}.plist")

if __name__ == "__main__":
    Fire()
