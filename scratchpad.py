  {
    "name": "bar.py",
    "run_interval": "10 seconds",
    "runs": "17",
    "state": "waiting",
    "script_path": "/Users/max/Library/LaunchAgents/hickory.bar.py.plist",
    "last_exit_code": "0",
    "program": "/Users/max/anaconda3/bin/python",
    "working_directory": "/Users/max/Repos/hickory",
    "environment_path": "/usr/bin:/bin:/usr/sbin:/sbin",
    "stdout": "/Users/max/Repos/hickory/hickory.log",
    "stderr": "/Users/max/Repos/hickory/hickory.log"
}

HID   FILE     RUNS   STATE    INTERVAL
3300  bar.py   17     waiting  10 seconds


Should there be an id?

schedule > info > kill

info/status
foo.py - waiting  - 10 runs  - every: 30 minutes
bar.py - runnning - 15 runs  - every: Monday @ 8:30
baz.py - error    - 140 runs - every: Weekday @ 9:30am

info foo.py
status foo.py

hickory schedule foo.py --every=30m
hickory info
hickory info foo.py
hickory kill foo.py


schedule > status > kill
schedule > info > kill
add > status > remove

SCHEDULE
--------
schedule
add
start
load
create
bootstrap
enable


LIST
----
status
info
inspect
list
enumerate
running
view
examine
sitrep
report


KILL
----
kill
remove
rm
terminate
bootout
drop
quit
cancel
disable
stop
nix
nullify
halt
delete
remove
cease
pause
eliminate
destroy




import os
import plistlib
import subprocess
from sys import platform

import sys
print(sys.executable)

os.path.abspath('')

str(Path.cwd())
#
# import platform
# platform.python_version()
# platform.mac_ver()
# platform.system()




# start calendar interval

Month 	Integer 	Month of year (1..12, 1 being January)
Day 	Integer 	Day of month (1..31)
Weekday 	Integer 	Day of week (0..7, 0 and 7 being Sunday)
Hour 	Integer 	Hour of day (0..23)
Minute 	Integer 	Minute of hour (0..59)

Likely API:

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
--every=2hour
--every=2hours

Day (will run every day)
--every=@4:00
--every=@4:00am
--every=@4:00pm
--every=@16:00

Weekday
--every=mon@4:00
--every=monday@4:00
--every=tues@4:000

Every Weekday
--every=weekday@9:00


—every=monday@8:30
—every=1st,2nd,3rd,15th@9:30,5:30pm
—every=30min


—every=*@00:00:00
—every=@10
—every=::1
—every=:2:


--day=1,2,3
--weekday=monday,1,tuesday,wednesday
--every=monday,tuesday,
--every=mon,tuesday
--every=@month:4
--every=@month:4,5
--every=@hour --at=*
--every=60:minutes
--every=2:hours
--every=weekday
--at=4:30pm
--at=4:30am
--at=4:30
--at=16:30

###

every minute
every 10 minutes
every 30 seconds
every 2 hours

every monday
every monday,tuesday
every weekday at 9:00am


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



6000 / 60 / 60

import datetime
str(datetime.timedelta(seconds=6000))


#
