import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

os.chdir("tests")


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


def test_cli_launchd():
    setup()
    subprocess.run("hickory schedule foo.py --every=5seconds", shell=True)
    status = subprocess.run(
        "hickory status", shell=True, capture_output=True
    ).stderr.decode()
    assert "foo.py" in status.split("\n")[1]
    time.sleep(5)
    kill_status = subprocess.run("hickory kill foo.oy", shell=True, capture_output=True).stdout.decode()
    assert kill_status.rstrip() == "Kill failed. foo.oy not found."
    kill_status = subprocess.run("hickory kill foo.py", shell=True, capture_output=True).stdout.decode()
    assert kill_status.rstrip() == "Killed foo.py"
    assert (Path.cwd() / "hickory.log").exists()
    teardown()
