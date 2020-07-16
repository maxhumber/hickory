import re

def interval_to_tuple(interval):
    # same as launchd
    c = re.findall(r"[A-Za-z]+|\d+", interval)
    try:
        value = int(c[0])
    except (ValueError, IndexError):
        raise HickoryError(f"Invalid interval: {interval}") from None
    unit = "s" if len(c) == 1 else c[1]
    return value, unit

def interval_to_oncalendar(interval):
    value, unit = interval_to_tuple(interval)
    if unit in ["s", "sec", "secs", "second", "seconds"]:
        string = f"*:*:0/{value}"
    elif unit in ["m", "min", "mins", "minute", "minutes"]:
        string = f"*:0/{value}"
    elif unit in ["h", "hr", "hrs", "hour", "hours"]:
        string = f"0/{value}:00:00"
    else:
        raise HickoryError(f"Invalid interval: {interval}")
    return {"OnCalendar": string}

interval_to_active_sec("10seconds")
interval_to_active_sec("10minutes")
interval_to_active_sec("10hours")

# Calendar

# | **Time**         |                                             |
# | 10:00 AM         | `@10`, `@10am`                              |
# | 10:00 PM         | `@22`, `@10pm`                              |
# | 10:10 AM         | `@10:10`, `@10:10am`                        |
# | 10:10 PM         | `@22:10`, `@10:10pm`                        |

t = '12:01pm'
def timestamp_to_string(t):
    rt = re.findall(r"[A-Za-z]+|\d+", t)
    try:
        hour = int(rt[0])
    except (ValueError, IndexError):
        raise HickoryError(f"Invalid time: {t}") from None
    minute = 0
    if len(rt) == 2:
        if rt[1] == "pm":
            hour += 12
        elif rt[1] == "am":
            pass
        else:
            minute = int(rt[1])
    if len(rt) == 3:
        minute = int(rt[1])
        if rt[2] == "am":
            pass
        elif (rt[2] == "pm") & (rt[0] != "12"):
            hour += 12
        else:
            raise HickoryError(f"Invalid time: {t}")
    if not ((0 <= hour <= 23) and (0 <= minute <= 59)):
        raise HickoryError(f"Invalid time: {t}")
    return f'{hour}:{minute}:00'



# FORMAT
# DayOfWeek Year-Month-Day Hour:Minute:Second

[Timer]
OnCalendar=*-*-* 10:10:00


# | **Weekday**      |                                             |
# | Monday           | `m@`, `mon@`, `monday@`                     |
# | Tuesday          | `t@`, `tue@`, `tues@`, `tuesday@`           |
# | Wednesday        | `w@`, `wed@`, `weds@`, `wednesday@`         |
# | Thursday         | `th@`, `thur@`, `thurs@`, `thursday@`       |
# | Friday           | `f@`, `fri@`, `friday@`                     |
# | Saturday         | `s@`, `sat@`, `saturday@`                   |
# | Sunday           | `su@`, `sun@`, `sunday@`                    |

[Timer]
OnCalendar=*-*-* 10:10:00

OnCalendar=Mon 10:10:00
OnCalendar=Tue 10:10:00
OnCalendar=Wed 10:10:00
OnCalendar=Thu 10:10:00
OnCalendar=Fri 10:10:00
OnCalendar=Sat 10:10:00
OnCalendar=Sun 10:10:00

# | **Calendar Day** |                                             |
# | 1st              | `1@`, `1st@`                                |
# | 2nd              | `2@`, `2nd@`                                |
# | 3rd              | `3@`, `3rd@`                                |
# | 4th              | `4@`, `4th@`                                |
# | 15th             | `15@`, `15th@`                              |
# | 31st             | `31@`, `31st@`                              |
# | **Other Day**    |                                             |
# | Every Day        | `day@`                                      |

OnCalendar=*-*-01 02:00:00


[Timer]
OnCalendar=*-*-* 10:10:00

# | Every Weekday    | `weekday@`                                  |

[Timer]
Mon..Fri 22:30

# | End of Month     | `eom@`                                      |

# Multiples:

OnCalendar=Mon..Fri 22:30
OnCalendar=Sat,Sun 20:00
