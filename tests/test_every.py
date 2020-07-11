import pytest
from hickory.every import *


def test_interval_to_lower():
    s = "MONDAY@9:00AM"
    assert "monday@9:00am" == interval_to_lower(s)


def test_strip_number():
    strings = ["1", "1l", "l"]
    output = [strip_number(s) for s in strings]
    assert output == ["1", "1", ""]


def test_contains_number():
    strings = ["1", "1l", "l"]
    output = [contains_number(s) for s in strings]
    assert output == [True, True, False]


def test_interval_to_components():
    intervals = ["5", "5s", "5ss", "5s5"]
    output = [interval_to_components(i) for i in intervals]
    assert all([len(o) == 2 for o in output])


def test_fail_interval_to_components():
    with pytest.raises(InvalidInterval):
        interval_to_components("s5")


def test_seconds_interval_to_seconds():
    intervals = ["10", "10s", "10sec", "10secs", "10seconds"]
    seconds = [interval_to_seconds(i) for i in intervals]
    assert all([s == 10 for s in seconds])


def test_minutes_interval_to_seconds():
    intervals = ["30m", "30min", "30mins", "30minutes"]
    seconds = [interval_to_seconds(i) for i in intervals]
    assert all([s == 1800 for s in seconds])


def test_hours_interval_to_seconds():
    intervals = ["2h", "2hr", "2hrs", "2hour", "2hours"]
    seconds = [interval_to_seconds(i) for i in intervals]
    assert all([s == 7200 for s in seconds])


def test_fail_interval_to_seconds():
    with pytest.raises(InvalidInterval):
        interval_to_seconds("5secondz")


def test_day_to_number_in_week():
    days = ["m", "tue", "weds", "thursday", "f", "sat", "sunday"]
    output = [day_to_number_in_week(d) for d in days]
    assert output == [1, 2, 3, 4, 5, 6, 7]


def test_day_to_number_in_month():
    days = ["1", "1st", "2", "2nd", "3", "3rd", "4", "4th", "31", "31st"]
    output = [day_to_number_in_month(d) for d in days]
    assert output == [1, 1, 2, 2, 3, 3, 4, 4, 31, 31]


def test_fail_day_to_number_in_month():
    with pytest.raises(InvalidMonthDay):
        day_to_number_in_month("32")


def test_time_to_hour_minute():
    times = ["20", "8", "8am", "8:30", "8:30am", "8:30pm", "20:30"]
    output = [time_to_hour_minute(t) for t in times]
    assert output == [(20, 0), (8, 0), (8, 0), (8, 30), (8, 30), (20, 30), (20, 30)]


def test_fail_time_to_hour_minute():
    with pytest.raises(InvalidTime):
        time_to_hour_minute("30:30")


def test_disjoin():
    strings = [
        "tuesday@5:30pm",
        "@9:30am",
        "@8:30,8:30pm",
        "m,t@8:30",
        "th,f@8:30,4:30pm",
    ]
    output = [list(disjoin(s)) for s in strings]
    assert output == [
        [("tuesday", "5:30pm")],
        [("", "9:30am")],
        [("", "8:30"), ("", "8:30pm")],
        [("m", "8:30"), ("t", "8:30")],
        [("th", "8:30"), ("th", "4:30pm"), ("f", "8:30"), ("f", "4:30pm")],
    ]
