import os
from pathlib import Path
import sys
import pytest
import subprocess
from hickory.launchd import _build_dict

os.chdir("tests")
Path.cwd()


def setup():
    foo = """import datetime
import time

stamp = datetime.datetime.now().strftime("%H:%M:%S")
time.sleep(5)

print(f"Foo - {stamp} + 5 seconds")"""
    with open("foo.py", "w") as f:
        f.write(foo)


def teardown():
    subprocess.run("rm foo.py hickory.log", shell=True)


setup()
subprocess.run("hickory schedule foo.py --every=10seconds", shell=True)
subprocess.run("hickory status", shell=True, capture_output=True).stdout.decode()
subprocess.run("hickory kill foo.py", shell=True)
(Path.cwd() / "hickory.log").exists()
teardown()


def test__build_dict():
    script = "foo.py"
    label = f"hickory.000000.{script}"
    working_directory = str(Path.cwd())
    which_python = sys.executable
    interval = "@10:00pm"
    ldd = _build_dict(label, working_directory, which_python, script, interval)
    assert ldd == {
        "Label": "hickory.000000.foo.py",
        "WorkingDirectory": working_directory,
        "ProgramArguments": [which_python, "foo.py"],
        "StandardOutPath": f"{working_directory}/hickory.log",
        "StandardErrorPath": f"{working_directory}/hickory.log",
        "RunAtLoad": False,
        "StartCalendarInterval": {"Hour": 22, "Minute": 0},
    }
