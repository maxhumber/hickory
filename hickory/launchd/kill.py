from pathlib import Path

from ..constants import LAUNCHD_PATH, HICKORY_SERVICE
from ..shared import run


def kill(id_or_script):
    """Kill (stop and delete) the id or script"""
    for file in Path(LAUNCHD_PATH).glob(f"{HICKORY_SERVICE}*{id_or_script}*"):
        run(f"launchctl unload {file}")
        run(f"rm {file}")
