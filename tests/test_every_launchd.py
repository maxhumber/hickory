import pytest
from hickory.every_launchd import *


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
    with pytest.raises(HickoryError):
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
    with pytest.raises(HickoryError):
        day_to_calendar_day_dict("32")


def test_weekday_list_dict():
    assert weekday_list_dict() == [
        {"Weekday": 1},
        {"Weekday": 2},
        {"Weekday": 3},
        {"Weekday": 4},
        {"Weekday": 5},
    ]


def test_eom_list_dict():
    assert eom_list_dict() == [
        {"Day": 31, "Month": 1},
        {"Day": 28, "Month": 2},
        {"Day": 31, "Month": 3},
        {"Day": 30, "Month": 4},
        {"Day": 31, "Month": 5},
        {"Day": 30, "Month": 6},
        {"Day": 31, "Month": 7},
        {"Day": 31, "Month": 8},
        {"Day": 30, "Month": 9},
        {"Day": 31, "Month": 10},
        {"Day": 30, "Month": 11},
        {"Day": 31, "Month": 12},
    ]


def test_day_to_list_dict():
    days = ["day", "1st", "monday"]
    output = [day_to_list_dict(day) for day in days]
    assert output == [[{}], [{"Day": 1}], [{"Weekday": 1}]]


def test_timestamp_to_dict():
    times = [
        "0:01",
        "1am",
        "1:01am",
        "12:00pm",
        "12pm",
        "12:01pm",
        "1pm",
        "11pm",
        "11:59pm",
    ]
    output = [timestamp_to_dict(t) for t in times]
    assert output == [
        {"Hour": 0, "Minute": 1},
        {"Hour": 1, "Minute": 0},
        {"Hour": 1, "Minute": 1},
        {"Hour": 12, "Minute": 0},
        {"Hour": 12, "Minute": 0},
        {"Hour": 12, "Minute": 1},
        {"Hour": 13, "Minute": 0},
        {"Hour": 23, "Minute": 0},
        {"Hour": 23, "Minute": 59},
    ]


def test_fail_timestamp_to_tuple():
    with pytest.raises(HickoryError):
        timestamp_to_tuple("30:30")


def test_start_calendar_interval():
    intervals = [
        "day@10",
        "@10:10",
        "monday@10:10am",
        "10th@10:10am",
        "10,20@10am",
        "monday,w,fri@9:30am,4:30pm",
        "eom@10:10am",
        "10,eom@10,10pm",
        "weekday@9:30,10pm",
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
        {
            "StartCalendarInterval": [
                {"Day": 31, "Month": 1, "Hour": 10, "Minute": 10},
                {"Day": 28, "Month": 2, "Hour": 10, "Minute": 10},
                {"Day": 31, "Month": 3, "Hour": 10, "Minute": 10},
                {"Day": 30, "Month": 4, "Hour": 10, "Minute": 10},
                {"Day": 31, "Month": 5, "Hour": 10, "Minute": 10},
                {"Day": 30, "Month": 6, "Hour": 10, "Minute": 10},
                {"Day": 31, "Month": 7, "Hour": 10, "Minute": 10},
                {"Day": 31, "Month": 8, "Hour": 10, "Minute": 10},
                {"Day": 30, "Month": 9, "Hour": 10, "Minute": 10},
                {"Day": 31, "Month": 10, "Hour": 10, "Minute": 10},
                {"Day": 30, "Month": 11, "Hour": 10, "Minute": 10},
                {"Day": 31, "Month": 12, "Hour": 10, "Minute": 10},
            ]
        },
        {
            "StartCalendarInterval": [
                {"Day": 10, "Hour": 10, "Minute": 0},
                {"Day": 10, "Hour": 22, "Minute": 0},
                {"Day": 31, "Month": 1, "Hour": 10, "Minute": 0},
                {"Day": 28, "Month": 2, "Hour": 10, "Minute": 0},
                {"Day": 31, "Month": 3, "Hour": 10, "Minute": 0},
                {"Day": 30, "Month": 4, "Hour": 10, "Minute": 0},
                {"Day": 31, "Month": 5, "Hour": 10, "Minute": 0},
                {"Day": 30, "Month": 6, "Hour": 10, "Minute": 0},
                {"Day": 31, "Month": 7, "Hour": 10, "Minute": 0},
                {"Day": 31, "Month": 8, "Hour": 10, "Minute": 0},
                {"Day": 30, "Month": 9, "Hour": 10, "Minute": 0},
                {"Day": 31, "Month": 10, "Hour": 10, "Minute": 0},
                {"Day": 30, "Month": 11, "Hour": 10, "Minute": 0},
                {"Day": 31, "Month": 12, "Hour": 10, "Minute": 0},
                {"Day": 31, "Month": 1, "Hour": 22, "Minute": 0},
                {"Day": 28, "Month": 2, "Hour": 22, "Minute": 0},
                {"Day": 31, "Month": 3, "Hour": 22, "Minute": 0},
                {"Day": 30, "Month": 4, "Hour": 22, "Minute": 0},
                {"Day": 31, "Month": 5, "Hour": 22, "Minute": 0},
                {"Day": 30, "Month": 6, "Hour": 22, "Minute": 0},
                {"Day": 31, "Month": 7, "Hour": 22, "Minute": 0},
                {"Day": 31, "Month": 8, "Hour": 22, "Minute": 0},
                {"Day": 30, "Month": 9, "Hour": 22, "Minute": 0},
                {"Day": 31, "Month": 10, "Hour": 22, "Minute": 0},
                {"Day": 30, "Month": 11, "Hour": 22, "Minute": 0},
                {"Day": 31, "Month": 12, "Hour": 22, "Minute": 0},
            ]
        },
        {
            "StartCalendarInterval": [
                {"Weekday": 1, "Hour": 9, "Minute": 30},
                {"Weekday": 2, "Hour": 9, "Minute": 30},
                {"Weekday": 3, "Hour": 9, "Minute": 30},
                {"Weekday": 4, "Hour": 9, "Minute": 30},
                {"Weekday": 5, "Hour": 9, "Minute": 30},
                {"Weekday": 1, "Hour": 22, "Minute": 0},
                {"Weekday": 2, "Hour": 22, "Minute": 0},
                {"Weekday": 3, "Hour": 22, "Minute": 0},
                {"Weekday": 4, "Hour": 22, "Minute": 0},
                {"Weekday": 5, "Hour": 22, "Minute": 0},
            ]
        },
    ]


def test_every():
    intervals = ["10", "10mins", "@10", "monday@10:00pm"]
    output = [every(i) for i in intervals]
    assert output == [
        {"StartInterval": 10},
        {"StartInterval": 600},
        {"StartCalendarInterval": {"Hour": 10, "Minute": 0}},
        {"StartCalendarInterval": {"Weekday": 1, "Hour": 22, "Minute": 0}},
    ]


def test_hickory_errors():
    with pytest.raises(HickoryError):
        every("")
    with pytest.raises(HickoryError):
        every("z")
    with pytest.raises(HickoryError):
        every("1z")
    with pytest.raises(HickoryError):
        every("z@z")
    with pytest.raises(HickoryError):
        every("@")
    with pytest.raises(HickoryError):
        every("100@100")
    with pytest.raises(HickoryError):
        every("@10:10:10")
    with pytest.raises(HickoryError):
        every("@10@10")
