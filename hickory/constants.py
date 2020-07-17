from pathlib import Path

HICKORY_SERVICE = "hickory"
HOME = str(Path.home())
LAUNCHD_PATH = f"{HOME}/Library/LaunchAgents"
SYSTEMD_PATH = f"{HOME}/.config/systemd/user"
