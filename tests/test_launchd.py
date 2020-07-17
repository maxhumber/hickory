from pathlib import Path
import sys
import pytest
from hickory.launchd import _build_dict


def test__build_dict():
    script = 'foo.py'
    label = f'hickory.000000.{script}'
    working_directory = str(Path.cwd())
    which_python = sys.executable
    interval = '@10:00pm'
    ldd = _build_dict(label, working_directory, which_python, script, interval)
    assert ldd == {
        'Label': 'hickory.000000.foo.py',
        'WorkingDirectory': working_directory,
        'ProgramArguments': [which_python, 'foo.py'],
        'StandardOutPath': f'{working_directory}/hickory.log',
        'StandardErrorPath': f'{working_directory}/hickory.log',
        'RunAtLoad': False,
        'StartCalendarInterval': {'Hour': 22, 'Minute': 0}
    }
