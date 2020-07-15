# Reference:
# https://wiki.archlinux.org/index.php/Systemd/Timers
# https://www.freedesktop.org/software/systemd/man/systemd.time.html
# https://www.freedesktop.org/software/systemd/man/systemd.timer.html#Description

#
# | Interval         |                                             |
# | ---------------- | ------------------------------------------- |
# | 10 seconds       | `10`, `10s`, `10sec`, `10secs`, `10seconds` |

[Timer]
OnUnitActiveSec=10s # OnUnitActiveSec 	Schedule the task relatively to the last time the service unit was active
AccuracySec=1s

# | 10 minutes       | `10m`, `10min`, `10mins`, `10minutes`       |

[Timer]
OnUnitActiveSec=10m

# | 10 hours         | `10h`, `10hr`, `10hrs`, `10hours`           |

[Timer]
OnUnitActiveSec=10h

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
