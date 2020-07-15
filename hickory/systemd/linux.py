import configparser

## SERVICE

service = configparser.ConfigParser()
service.optionxform = str

service["Unit"] = {"Description": "Python Demo Service"}
service["Service"] = {
    "Type": "oneshot",
    "ExecStart": "/usr/bin/python path/to/your/python_demo_service.py",
    "WorkingDirectory": "$TODO$"
    "StandardOutput": "append:/home/user/log1.log"
    "StandardError": "append:/home/user/log2.log"
}

with open('example.service', 'w') as configfile:
    service.write(configfile)

## TIMER

timer = configparser.ConfigParser()
timer.optionxform = str

timer["Unit"] = {"Description": "Python Demo Service"}
timer["Timer"] = {
    "OnBootSec": "3min",
    "OnUnitActiveSec": "24h",
    "Unit": "example.service"
}
timer["Install"] = {"WantedBy": "multi-user.target"}

with open('example.timer', 'w') as configfile:
    timer.write(configfile)
