import pytest
from hickory.utils import *


def test_run():
    assert run("echo hi") == "hi"


def test_strip_number():
    strings = ["1", "1l", "l"]
    assert [strip_number(s) for s in strings] == [1, 1, None]


def test_contains_number():
    strings = ["1", "1l", "l"]
    assert [contains_number(s) for s in strings] == [True, True, False]


def test_interval_to_tuple():
    intervals = ["5", "5s", "5ss", "5s5"]
    output = [interval_to_tuple(i) for i in intervals]
    assert all([len(o) == 2 for o in output])


def test_fail_interval_to_tuple():
    with pytest.raises(HickoryError):
        interval_to_tuple("s5")


def test_timestamp_to_tuple():
    times = [
        "0:01",
        "12:01am",
        "1am",
        "1:01am",
        "12:00pm",
        "12pm",
        "12:01pm",
        "1pm",
        "11pm",
        "11:59pm",
    ]
    assert [timestamp_to_tuple(t) for t in times] == [
        (0, 1),
        (0, 1),
        (1, 0),
        (1, 1),
        (12, 0),
        (12, 0),
        (12, 1),
        (13, 0),
        (23, 0),
        (23, 59),
    ]


def test_disjoin():
    strings = [
        "tuesday@5:30pm",
        "@9:30am",
        "@8:30,8:30pm",
        "m,t@8:30",
        "th,f@8:30,4:30pm",
    ]
    output = [disjoin(s) for s in strings]
    assert output == [
        [("tuesday", "5:30pm")],
        [("", "9:30am")],
        [("", "8:30"), ("", "8:30pm")],
        [("m", "8:30"), ("t", "8:30")],
        [("th", "8:30"), ("th", "4:30pm"), ("f", "8:30"), ("f", "4:30pm")],
    ]
