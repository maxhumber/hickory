import re

# Reference:
# https://linuxconfig.org/how-to-schedule-tasks-with-systemd-timers-in-linux
# https://wiki.archlinux.org/index.php/Systemd/Timers
# https://www.freedesktop.org/software/systemd/man/systemd.time.html
# https://www.freedesktop.org/software/systemd/man/systemd.timer.html#Description

#
# | Interval         |                                             |
# | ---------------- | ------------------------------------------- |
# | 10 seconds       | `10`, `10s`, `10sec`, `10secs`, `10seconds` |
# | 10 minutes       | `10m`, `10min`, `10mins`, `10minutes`       |
# | 10 hours         | `10h`, `10hr`, `10hrs`, `10hours`           |

def interval_to_components(interval):
    c = re.findall(r"[A-Za-z]+|\d+", interval)
    try:
        value = int(c[0])
    except (ValueError, IndexError):
        raise HickoryError(f"Invalid interval: {interval}") from None
    unit = "s" if len(c) == 1 else c[1]
    return value, unit

def interval_to_active_sec(interval):
    # https://www.freedesktop.org/software/systemd/man/systemd.time.html
    value, unit = interval_to_components(interval)
    if unit in ["s", "sec", "secs", "second", "seconds"]:
        unit = "s"
    elif unit in ["m", "min", "mins", "minute", "minutes"]:
        unit = "m"
    elif unit in ["h", "hr", "hrs", "hour", "hours"]:
        unit = "h"
    else:
        raise HickoryError(f"Invalid interval: {interval}")
    value = "".join([str(value), unit])
    return {"OnActiveSec": value}

interval_to_active_sec("10hours")


# Calendar

# | **Time**         |                                             |
# | 10:00 AM         | `@10`, `@10am`                              |
# | 10:00 PM         | `@22`, `@10pm`                              |
# | 10:10 AM         | `@10:10`, `@10:10am`                        |
# | 10:10 PM         | `@22:10`, `@10:10pm`                        |

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

[Timer]
OnCalendar=*-*-* 10:10:00

# | Every Weekday    | `weekday@`                                  |

[Timer]
Mon..Fri 22:30

# | End of Month     | `eom@`                                      |

# Multiples:

OnCalendar=Mon..Fri 22:30
OnCalendar=Sat,Sun 20:00
