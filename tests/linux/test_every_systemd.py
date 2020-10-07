import pytest

from hickory.every_systemd import *


def test_interval_to_on_calendar_strings():
    intervals = ["10seconds", "10minutes", "10hours"]
    result = [interval_to_on_calendar_strings(i) for i in intervals]
    assert result == [["*:*:0/10"], ["*:0/10"], ["0/10:00:00"]]


def test_fail_interval_to_on_calendar_strings():
    with pytest.raises(HickoryError):
        interval_to_on_calendar_strings("10zz10")


def test_day_to_shorthand():
    days = "monday", "tues", "w", "th", "f", "sat", "sunday"
    assert [day_to_shorthand(day) for day in days] == [
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
        "Sun",
    ]


def test_fail_day_to_shorthand():
    with pytest.raises(HickoryError):
        day_to_shorthand("maxday")


def test_day_to_calendar_day():
    days = ["2", "10", "31"]
    assert [day_to_calendar_day(day) for day in days] == ["*-*-02", "*-*-10", "*-*-31"]


def test_fail_day_to_calendar_day():
    with pytest.raises(HickoryError):
        day_to_calendar_day("32")


def test_day_to_on_calendar_string():
    days = ["monday", "31", "weekday", "eom"]
    result = [day_to_on_calendar_string(day) for day in days]
    assert result == ["Mon", "*-*-31", "Mon..Fri", "*-*~01"]


def timestamp_to_on_calendar_string():
    timestamps = ["0:01", "12:01am", "1:01am", "12:01pm", "10:01pm"]
    result = [timestamp_to_on_calendar_string(t) for t in timestamps]
    assert result == ["00:01:00", "00:01:00", "01:01:00", "12:01:00", "22:01:00"]


def test_datetime_interval_to_on_calendar_strings():
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
    result = [datetime_interval_to_on_calendar_strings(i) for i in intervals]
    assert result == [
        ["*-*-* 10:00:00"],
        ["*-*-* 10:10:00"],
        ["Mon 10:10:00"],
        ["*-*-10 10:10:00"],
        ["*-*-10 10:00:00", "*-*-20 10:00:00"],
        [
            "Mon 09:30:00",
            "Mon 16:30:00",
            "Wed 09:30:00",
            "Wed 16:30:00",
            "Fri 09:30:00",
            "Fri 16:30:00",
        ],
        ["*-*~01 10:10:00"],
        ["*-*-10 10:00:00", "*-*-10 22:00:00", "*-*~01 10:00:00", "*-*~01 22:00:00"],
        ["Mon..Fri 09:30:00", "Mon..Fri 22:00:00"],
    ]


def test_every():
    intervals = ["10", "10mins", "@10", "monday@10:00pm"]
    output = [every(i) for i in intervals]
    assert output == [["*:*:0/10"], ["*:0/10"], ["*-*-* 10:00:00"], ["Mon 22:00:00"]]
