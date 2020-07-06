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


hickory list
hickory stop/pause/kill
hickory start/run/schedule
hickory delete/remove
hickory schedule demo.py --every 86400

# start calendar interval

Month 	Integer 	Month of year (1..12, 1 being January)
Day 	Integer 	Day of month (1..31)
Weekday 	Integer 	Day of week (0..7, 0 and 7 being Sunday)
Hour 	Integer 	Hour of day (0..23)
Minute 	Integer 	Minute of hour (0..59)

6000 / 60 / 60

import datetime
str(datetime.timedelta(seconds=6000))


#
