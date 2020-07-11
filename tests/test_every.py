import pytest
from hickory.every import *


def test_strip_number():
    strings = ["1", "1l", "l"]
    output = [strip_number(s) for s in strings]
    assert output == [1, 1, None]


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


def test_start_interval():
    intervals = ["10seconds", "10minutes", "10hours"]
    output = [start_interval(i) for i in intervals]
    assert output == [
        {"StartInterval": 10},
        {"StartInterval": 600},
        {"StartInterval": 36000},
    ]


def test_day_to_weekday_dict():
    days = ["m", "tue", "weds", "thursday", "f", "sat", "sunday"]
    output = [day_to_weekday_dict(d) for d in days]
    assert output == [
        {"Weekday": 1},
        {"Weekday": 2},
        {"Weekday": 3},
        {"Weekday": 4},
        {"Weekday": 5},
        {"Weekday": 6},
        {"Weekday": 7},
    ]


def test_day_to_calendar_day_dict():
    days = ["1", "1st", "2", "2nd", "3", "3rd", "4", "4th", "31", "31st"]
    output = [day_to_calendar_day_dict(d) for d in days]
    assert output == [
        {"Day": 1},
        {"Day": 1},
        {"Day": 2},
        {"Day": 2},
        {"Day": 3},
        {"Day": 3},
        {"Day": 4},
        {"Day": 4},
        {"Day": 31},
        {"Day": 31},
    ]


def test_fail_day_to_calendar_day_dict():
    with pytest.raises(InvalidCalendarDay):
        day_to_calendar_day_dict("32")


def test_day_to_dict():
    days = ["day", "1st", "monday"]
    output = [day_to_dict(day) for day in days]
    assert output == [{}, {"Day": 1}, {"Weekday": 1}]


def test_timestamp_to_dict():
    times = ["20", "8", "8am", "8:30", "8:30am", "8:30pm", "20:30"]
    output = [timestamp_to_dict(t) for t in times]
    assert output == [
        {"Hour": 20, "Minute": 0},
        {"Hour": 8, "Minute": 0},
        {"Hour": 8, "Minute": 0},
        {"Hour": 8, "Minute": 30},
        {"Hour": 8, "Minute": 30},
        {"Hour": 20, "Minute": 30},
        {"Hour": 20, "Minute": 30},
    ]


def test_fail_timestamp_to_dict():
    with pytest.raises(InvalidTime):
        timestamp_to_dict("30:30")


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


def test_start_calendar_interval():
    intervals = [
        "day@10",
        "@10:10",
        "monday@10:10am",
        "10th@10:10am",
        "10,20@10am",
        "monday,w,fri@9:30am,4:30pm"
        # 'eom@10:10am',
        # '10,eom@10,10pm'
    ]
    output = [start_calendar_interval(i) for i in intervals]
    assert output == [
        {"StartCalendarInterval": {"Hour": 10, "Minute": 0}},
        {"StartCalendarInterval": {"Hour": 10, "Minute": 10}},
        {"StartCalendarInterval": {"Weekday": 1, "Hour": 10, "Minute": 10}},
        {"StartCalendarInterval": {"Day": 10, "Hour": 10, "Minute": 10}},
        {
            "StartCalendarInterval": [
                {"Day": 10, "Hour": 10, "Minute": 0},
                {"Day": 20, "Hour": 10, "Minute": 0},
            ]
        },
        {
            "StartCalendarInterval": [
                {"Weekday": 1, "Hour": 9, "Minute": 30},
                {"Weekday": 1, "Hour": 16, "Minute": 30},
                {"Weekday": 3, "Hour": 9, "Minute": 30},
                {"Weekday": 3, "Hour": 16, "Minute": 30},
                {"Weekday": 5, "Hour": 9, "Minute": 30},
                {"Weekday": 5, "Hour": 16, "Minute": 30},
            ]
        },
    ]


#
