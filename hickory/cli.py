import json
from pathlib import Path
import plistlib
import re
import sys
from uuid import uuid4

from fire import Fire

try:
    from .every import every as every_to_dict, HickoryError
    from .run import run
except ImportError:
    # FOR TESTING
    from hickory.every import every as every_to_dict, HickoryError
    from hickory.run import run


USER_HOME = str(Path.home())
LAUNCHD_PATH = f'{USER_HOME}/Library/LaunchAgents'
HICKORY_SERVICE = "hickory"


def generate_launchd_dict(script, every):
    '''
    DOCTODO // Build launchd compatible dictionary
    '''
    which_python = sys.executable
    working_directory = str(Path.cwd())
    hid = uuid4().hex[:6]
    hickory_label = f"{HICKORY_SERVICE}.{hid}.{script}"
    launchd_dict = {
        "Label": hickory_label,
        "Every": every,
        "WorkingDirectory": working_directory,
        "ProgramArguments": [which_python, script],
        "RunAtLoad": False,
        "StandardErrorPath": f"{working_directory}/hickory.log",
        "StandardOutPath": f"{working_directory}/hickory.log",
    }
    launchd_dict.update(every_to_dict(every))
    return launchd_dict


def schedule(script, every):
    '''
    DOCTODO // schedule the actual script!
    '''
    if not Path(script).exists():
        raise FileNotFoundError(script)
    launchd_dict = generate_launchd_dict(script, every)
    path = f"{LAUNCHD_PATH}/{launchd_dict['Label']}.plist"
    with open(f"{path}", "wb") as f:
        plistlib.dump(launchd_dict, f)
    run(f"launchctl load {path}")


def kill(id_or_script):
    '''
    DOCTODO // kill (stop and delete) the scheduler for script name or id
    '''
    for file in Path(LAUNCHD_PATH).glob(f'{HICKORY_SERVICE}*{id_or_script}*'):
        run(f"launchctl unload {file}")
        run(f"rm {file}")


####

uid = run("id -u")
running = run(f"launchctl list | grep {HICKORY_SERVICE}")
scripts = [script.split("\t")[-1] for script in running.split("\n")]
infos = []
script = scripts[0]
for script in scripts:
    infodump = run(f"launchctl print gui/{uid}/{script}")
    print(infodump)
    info = parse_gui_infodump(infodump)
    infos.append(info)
# return json.dumps(infos, indent=2)
return infos





def parse_gui_infodump(info):
    path, stdout, stderr = re.findall("path = (.*?)\n", info)
    plist_name = (
        path.split("/")[-1].replace(f"{HICKORY_SERVICE}.", "").replace(".plist", "")
    )
    return {
        "plist_name": plist_name,
        "hid": plist_name.split(".")[0],
        "script": ".".join(plist_name.split(".")[1:]),
        # need
        "run_interval": re.findall("run interval = (.*?)\n", info)[0],
        "runs": re.findall("runs = (.*?)\n", info)[0],
        "state": re.findall("state = (.*?)\n", info)[0],
        # nice to have
        "script_path": path,
        "last_exit_code": re.findall("last exit code = (.*?)\n", info)[0],
        # probably don't need
        "program": re.findall("program = (.*?)\n", info)[0],
        "working_directory": re.findall("working directory = (.*?)\n", info)[0],
        "environment_path": re.findall("PATH => (.*?)\n", info)[0],
        "stdout": stdout,
        "stderr": stderr,
    }


for file in Path(LAUNCHD_PATH).glob(f'*{HICKORY_SERVICE}*'):
    print(file)





def status():
        # HID   FILE     RUNS   STATE    INTERVAL
        # 3300  bar.py   17     waiting  10 seconds
    infos = all_info()
    terminal_string = "hid - script - runs - state - interval"
    for i in infos:
        s = f"\n{i['hid']} - {i['script']} - {i['runs']} - {i['state']} - {i['run_interval']}"
        terminal_string = terminal_string + s
    return terminal_string


def list():
    return run(f"launchctl list | grep {HICKORY_SERVICE}")


def main():
    Fire(
        {
            "schedule": schedule,
            "list": list,
            "status": status,
            "kill": kill,
        }
    )


if __name__ == "__main__":
    main()
