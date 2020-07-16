import sys
from pathlib import Path
from uuid import uuid4

from fire import Fire

from .constants import HICKORY_SERVICE
from .launchd import schedule_launchd, kill_launchd, status_launchd
from .systemd import schedule_systemd, kill_systemd, status_systemd

def schedule(script, every):
    if not Path(script).exists():
        raise FileNotFoundError(script)

    id = uuid4().hex[:6]
    label = f"{HICKORY_SERVICE}.{id}.{script}"
    working_directory = str(Path.cwd())
    which_python = sys.executable

    if sys.platform == "darwin":
        schedule_launchd(label, working_directory, which_python, script, every)
    elif sys.platform == "linux":
        pass  # schedule_systemd
    else:
        raise OSError("Operating System Not Supported")


def kill(id_or_script):
    if sys.platform == "darwin":
        kill_launchd(id_or_script)
    elif sys.platform == "linux":
        pass  # kill_systemd
    else:
        raise OSError("Operating System Not Supported")


def status():
    if sys.platform == "darwin":
        return status_launchd()
    elif sys.platform == "linux":
        pass  # status_systemd()
    else:
        raise OSError("Operating System Not Supported")


def main():
    Fire(
        {"schedule": schedule, "status": status, "kill": kill}
    )


if __name__ == "__main__":
    main()
