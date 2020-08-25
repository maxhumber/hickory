import pytest
from hickory.format_status import format_status


def test_format_status():
    info_dicts = [{
        'id': '0f98e6',
        'file': 'foo.py',
        'runs': '396',
        'state': 'waiting',
        'interval': 5
    }]
    string = 'ID      FILE    STATE    RUNS  INTERVAL\n0f98e6  foo.py  waiting  396   5'
    assert string == format_status(info_dicts)
