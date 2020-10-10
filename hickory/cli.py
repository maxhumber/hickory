import argparse
import sys
from pathlib import Path
from uuid import uuid4

from .launchd import kill_launchd, schedule_launchd, status_launchd
from .systemd import kill_systemd, schedule_systemd, status_systemd

from log import write_log
from decouple import config


HICKORY_SERVICE = config('HICKORY_SERVICE')

def schedule(script: str, every: str) -> None:
    """Schedule a Python script to repeat <every>

    Params:
    - script: a Python file
    - every: an "every" interval

    Examples:
    ```
    hickory schedule foo.py --every=10m
    hickory schedule foo.py --every=m,t@10:10am
    ```
    """
    if not Path(script).exists():
        write_log('FileNotFoundError ',script)
        raise FileNotFoundError(script)

    id = uuid4().hex[:6]
    label = f"{HICKORY_SERVICE}.{id}.{script}"
    working_directory = str(Path.cwd())
    which_python = sys.executable

    if sys.platform == "darwin":
        schedule_launchd(label, working_directory, which_python, script, every)
        write_log('Sys Platform - Darwin')
    elif sys.platform == "linux":
        schedule_systemd(label, working_directory, which_python, script, every)
        write_log('Sys Platform - Linux')
    else:
        write_log("Operating System Not Supported")
        raise OSError("Operating System Not Supported")


def kill(id_or_script: str) -> None:
    """Stop and delete a schedule for a Python script

    Params:
    - id_or_script: schedule id or Python script

    Examples:
    ```
    hickory kill foo.py
    hickory kill 8ae4f2
    ```
    """
    if sys.platform == "darwin":
        write_log('Killed darwin')
        kill_launchd(id_or_script)
    elif sys.platform == "linux":
        write_log('Killed linux')
        kill_systemd(id_or_script)
    else:
        write_log('Operating System Not Supported')
        raise OSError("Operating System Not Supported")


def status() -> str:
    """Check the status of all scheduled Python scripts

    Example:
    ```
    hickory status
    ```
    """
    if sys.platform == "darwin":
        return status_launchd()
    elif sys.platform == "linux":
        return status_systemd()
    else:
        raise OSError("Operating System Not Supported")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("function", choices=("schedule", "status", "kill"))
    parser.add_argument("script", nargs="?")
    parser.add_argument("-e", "--every", nargs="?")
    args = parser.parse_args()
    if args.function == "schedule" and args.script and args.every:
        schedule(args.script, args.every)
        write_log(f"Scheduled {args.script}")
        print(f"Scheduled {args.script}")
    if args.function == "status":
        return status()
    if args.function == "kill" and args.script:
        kill(args.script)
        write_log(f"Killed {args.script}")
        print(f"Killed {args.script}")


if __name__ == "__main__":
    main()
