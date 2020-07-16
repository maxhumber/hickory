from pathlib import Path
from .shared import run


HICKORY_SERVICE = "hickory"

USER_HOME = str(Path.home())
USER_ID = run("id -u")

LAUNCHD_PATH = f"{USER_HOME}/Library/LaunchAgents"
