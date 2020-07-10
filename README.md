<h3 align="center">
  <img src="https://raw.githubusercontent.com/maxhumber/hickory/master/logo/hickory.png" width="125px" alt="hickory">
</h3>
<p align="center">
  <a href="https://github.com/maxhumber/hickory"><img alt="GitHub" src="https://img.shields.io/github/license/maxhumber/hickory"></a>
  <a href="https://travis-ci.org/maxhumber/hickory"><img alt="Travis" src="https://img.shields.io/travis/maxhumber/hickory.svg"></a>
  <a href="https://pypi.python.org/pypi/hickory"><img alt="PyPI" src="https://img.shields.io/pypi/v/hickory.svg"></a>
  <a href="https://pepy.tech/project/hickory"><img alt="Downloads" src="https://pepy.tech/badge/hickory"></a>
</p>


### 🚨 Warning

API subject to change - package under active development!



### About

Command line tool for scheduling Python scripts on macOS (linux coming soon)...

Name and logo inspired by the [rhyme](https://en.wikipedia.org/wiki/Hickory_Dickory_Dock).



### Usage

Schedule a script:

- `hickory schedule foo.py --every=10`

View running scripts:

- `hickory list`

Kill a running script:

- `hickory kill foo.py`




### Install

PyPI coming soon, but for now:

`pip install git+https://github.com/maxhumber/hickory`



----





# BASIC API
hickory schedule foo.py 10
hickory schedule foo.py --every=10

hickory schedule info
hickory schedule info 6s330d
hickory schedule info foo.py

hickory schedule kill 6s330d
hickory schedule kill foo.py

## Calendar Intervals for launchd

Month 	Integer 	Month of year (1..12, 1 being January)
Day 	Integer 	Day of month (1..31)
Weekday 	Integer 	Day of week (0..7, 0 and 7 being Sunday)
Hour 	Integer 	Hour of day (0..23)
Minute 	Integer 	Minute of hour (0..59)

## every api

Seconds
10
--every=10
--every=10s
--every=10sec
--every=10secs
--every=10seconds

Minutes
--every=30m
--every=30min
--every=30mins
--every=30minutes

Hours
--every=2h
--every=2hr
--every=2hour
--every=2hours

Day (will run every day)
--every=day@4:00
--every=day@4:00am
--every=day@4:00pm
--every=day@16:00
--every=@4:00
--every=@4

++++ Weekday (MTWThF)
--every=weekday@4:00

Specific Day
--every=mon@4:00
--every=monday@4:00
--every=tues@4:000

Specific Calendar Day
--every=1@8:30
--every=1st@8:30
--every=2@8:30
--every=2nd@8:30
--every=3@8:30
--every=3rd@8:30
--every=4@8:30
--every=4th@8:30
--every=13@8:30

++++ Last Day of Month
--every=eom@8:30

Multiple Intervals
--every=15,eom@9:30pm
--every=weekday@9:00am,4:30pm
--every=5,15,20@9:30,5:30pm
