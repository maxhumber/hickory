import sys
from pathlib import Path
from uuid import uuid4
from fire import Fire

from .launchd.kill import kill as kill_launchd
from .launchd.schedule import schedule as schedule_launchd
from .launchd.status import status as status_launchd
from .launchd.status import list as list_launchd


def schedule(script, every):
    if not Path(script).exists():
        raise FileNotFoundError(script)

    if sys.platform == "darwin":
        schedule_launchd(script, every)
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


def list():
    if sys.platform == "darwin":
        return list_launchd()
    elif sys.platform == "linux":
        pass
    else:
        raise OSError("Operating System Not Supported")


def main():
    Fire(
        {"schedule": schedule, "list": list, "status": status, "kill": kill,}
    )


if __name__ == "__main__":
    main()
