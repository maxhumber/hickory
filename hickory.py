import plistlib
import io
import subprocess
import uuid
import sys
from pathlib import Path

from fire import Fire # to remove

hickory_identifier = "local.hickory"

def run(command, output=True, silent=False):
    if silent:
        command += ' --quiet'
    if output:
        s = subprocess.run(command, capture_output=True, shell=True)
        o = s.stdout.decode('utf-8').strip()
        return o
    subprocess.run(command, shell=True)

def schedule(file_name, interval=10):
    which_python = sys.executable
    working_directory = str(Path.cwd())
    home = str(Path.home())
    d = {
        "Label": f"{hickory_identifier}.{file_name}", # use filename
        "WorkingDirectory": working_directory, # add working directory
        "ProgramArguments": [which_python, file_name],
        "StartInterval": interval,
        "RunAtLoad": True,
        "StandardErrorPath": f"{working_directory}/stderr.log",
        "StandardOutPath": f"{working_directory}/stdout.log"
    }
    with open(f"{home}/Library/LaunchAgents/{d['Label']}.plist", "wb") as f:
        plistlib.dump(d, f)

def list():
    return run(f"launchctl list | grep {hickory_identifier}")

def kill(id):
    home = str(Path.home())
    unload = f"launchctl unload ~/Library/LaunchAgents/{hickory_identifier}.{id}.plist"
    run(unload)
    run(f"rm {home}/Library/LaunchAgents/{hickory_identifier}.{id}.plist")

if __name__ == "__main__":
    Fire()
