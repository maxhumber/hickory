import os
import plistlib
import subprocess

from sys import platform

import sys
print(sys.executable)

s = subprocess.run('which python', capture_output=True, shell=True)
output = s.stdout.decode('utf-8').strip()
print(output)

os.path.abspath('')

str(Path.cwd())
#
# import platform
# platform.python_version()
# platform.mac_ver()
# platform.system()



d = {
    "Label": "com.hickory.example", # use filename
    "WorkingDirectory": "/Users/max/Repos/hickory", # add w
    "ProgramArguments": ["/Users/max/anaconda3/bin/python", "demo.py"],
    "StartInterval": 10,
    "RunAtLoad": True,
    "StandardErrorPath": "/Users/max/Repos/hickory/stderr.log",
    "StandardOutPath": "/Users/max/Repos/hickory/stdout.log"
}

import io
f = io.BytesIO()

plistlib.dump(d, f)
f.getbuffer()
print(f.getvalue().decode('utf-8'))

with open("com.hickory.example.plist", "wb") as f:
    plistlib.dump(d, f)

#####

import hickory

@hickory.task(label="", schedule="")
def hello():
    print("hello world")


@hickory.task(every={"minute": 5})

hickory.run()

# possible command line tools

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
