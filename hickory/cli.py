import argparse
import sys
from pathlib import Path
from uuid import uuid4

from .colors import Fore

from .constants import HICKORY_SERVICE
from .launchd import kill_launchd, schedule_launchd, status_launchd
from .systemd import kill_systemd, schedule_systemd, status_systemd
from .utils import pretty_print_exception


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
        raise FileNotFoundError(script)

    id = uuid4().hex[:6]
    label = f"{HICKORY_SERVICE}.{id}.{script}"
    working_directory = str(Path.cwd())
    which_python = sys.executable

    if sys.platform == "darwin":
        schedule_launchd(label, working_directory, which_python, script, every)
    elif sys.platform == "linux":
        schedule_systemd(label, working_directory, which_python, script, every)
    else:
        raise OSError("Operating System Not Supported", sys.platform)


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
        kill_launchd(id_or_script)
    elif sys.platform == "linux":
        kill_systemd(id_or_script)
    else:
        raise OSError("Operating System Not Supported", sys.platform)


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
        raise OSError("Operating System Not Supported", sys.platform)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("function", choices=("schedule", "status", "kill"))
    parser.add_argument("script", nargs="?")
    parser.add_argument("-e", "--every", nargs="?")

    args = parser.parse_args()

    try:
        if args.function == "schedule" and args.script and args.every:
            schedule(args.script, args.every)
            print(f"{Fore.GREEN}%s{Fore.RESET}" % f"Scheduled {args.script}")
        if args.function == "status":
            return status()
        if args.function == "kill" and args.script:
            kill(args.script)
            print(Fore.GREEN @ f"Killed {args.script}")

    except Exception as e:
        pretty_print_exception(e)
        exit(1)


if __name__ == "__main__":
    main()
