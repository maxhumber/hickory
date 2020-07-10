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

Weekday (MTWThF)
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

Last Day of Month
--every=eom@8:30

Multiple Intervals
--every=15,eom@9:30pm
--every=weekday@9:00am,4:30pm
--every=5,15,20@9:30,5:30pm

# Fooling around with codes

 1009  launchctl dumpstate | grep hickory
 1010  dtrace | grep hickory
 1011  dtruss
 1012  dtruss -n hickory.tryme.py
 1013  launchctl print
 1014  launchctl list | grep hickory
 1015  launchctl print hickory.tryme.py
 1016  launchctl print hickory
 1017  uid
 1018  launchctl print-disabled user/uid
 1019  id -u
 1020  launchctl print-disabled user/uid
 1021  launchctl print-disabled user/501
 1022  launchctl print gui/501
 1023  launchctl print gui/501 | grep hickory
 1024  launchctl print gui/501/hickory.tryme.py
 1024  launchctl print gui/501/hickory.tryme.py | grep state
