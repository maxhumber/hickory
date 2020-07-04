from fire import Fire
import plistlib
import io
import subprocess
import uuid
import sys
from pathlib import Path

def run(command, output=False, silent=False):
    if silent:
        command += ' --quiet'
    if output:
        s = subprocess.run(command, capture_output=True, shell=True)
        output = s.stdout.decode('utf-8').strip()
        return output
    subprocess.run(command, shell=True)

def create_plist(file_name, interval=10):
    which_python = sys.executable
    working_directory = str(Path.cwd())
    d = {
        "Label": f"local.hickory.{file_name}", # use filename
        "WorkingDirectory": working_directory, # add working directory
        "ProgramArguments": [which_python, file_name],
        "StartInterval": interval,
        "RunAtLoad": True,
        "StandardErrorPath": f"{working_directory}/stderr.log",
        "StandardOutPath": f"{working_directory}/stdout.log"
    }
    f = io.BytesIO()
    plistlib.dump(d, f)
    print(f.getvalue().decode('utf-8'))

if __name__ == "__main__":
    Fire(create_plist)
