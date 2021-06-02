<h3 align="center">
  <img src="https://raw.githubusercontent.com/maxhumber/hickory/master/logo/hickory.png" width="125px" alt="hickory">
</h3>
<p align="center">
  <a href="https://pypi.python.org/pypi/hickory"><img alt="PyPI" src="https://img.shields.io/pypi/v/hickory.svg"></a>
  <a href="https://pepy.tech/project/hickory"><img alt="Downloads" src="https://pepy.tech/badge/hickory"></a>
</p>




### About

`hickory` is a simple command line tool for scheduling Python scripts.



### Support

| Operating System | Scheduler                                        |
| ---------------- | ------------------------------------------------ |
| macOS            | [launchd](https://en.wikipedia.org/wiki/Launchd) |
| Linux            | [systemd](https://en.wikipedia.org/wiki/Systemd) |
| Windows          | ❌                                                |



### Install

```sh
pip install hickory
```



### Quickstart

<a href="https://asciinema.org/a/355543" target="_blank"><img src="https://asciinema.org/a/355543.svg" /></a>

Create a file called `foo.py`:

```python
import datetime
import time

stamp = datetime.datetime.now().strftime("%H:%M:%S")
time.sleep(5)

print(f"Foo - {stamp} + 5 seconds")
```

Schedule `foo.py` to execute every ten minutes:

```sh
hickory schedule foo.py --every=10minutes
```

Check the status of all queued schedules:

```sh
hickory status
```

Stop and delete the schedule for `foo.py`:

```sh
hickory kill foo.py
```



### Logs

macOS - logs are stored in the same directory as the scheduled script:

```sh
tail -f hickory.log
```

Linux - logs are written to the journal:

```sh
journalctl -f
```



### `--every` Examples

| Repeat                                                  |                          |
| ------------------------------------------------------- | ------------------------ |
| Every ten minutes                                       | `--every=10minutes`      |
| Every day at 10:10 AM                                   | `--every=@10:10`         |
| Every Monday at 10:10 AM                                | `--every=monday@10:10am` |
| Every 10th day of the month at 10:10 AM                 | `--every=10th@10:10am`   |
| Every last day of the month at 10:10 AM                 | `--every=eom@10:10am`    |
| Every 10th and last day of the month at 10 AM and 10 PM | `--every=10,eom@10,10pm` |



### `--every` Table

| Interval         |                                               |
| ---------------- | --------------------------------------------- |
| 10 seconds       | `10`, `10s`, `10sec`, `10secs`, `10seconds`   |
| 10 minutes       | `10m`, `10min`, `10mins`, `10minutes`         |
| 10 hours         | `10h`, `10hr`, `10hrs`, `10hours`             |
| **Time**         |                                               |
| 10:00 AM         | `@10`, `@10am`                                |
| 10:00 PM         | `@22`, `@10pm`                                |
| 10:10 AM         | `@10:10`, `@10:10am`                          |
| 10:10 PM         | `@22:10`, `@10:10pm`                          |
| **Weekday**      |                                               |
| Monday           | `m@`, `mon@`, `monday@`                       |
| Tuesday          | `t@`, `tue@`, `tues@`, `tuesday@`             |
| Wednesday        | `w@`, `wed@`, `weds@`, `wednesday@`           |
| Thursday         | `th@`, `thu@`, `thur@`, `thurs@`, `thursday@` |
| Friday           | `f@`, `fri@`, `friday@`                       |
| Saturday         | `s@`, `sat@`, `saturday@`                     |
| Sunday           | `su@`, `sun@`, `sunday@`                      |
| **Calendar Day** |                                               |
| 1st              | `1@`, `1st@`                                  |
| 2nd              | `2@`, `2nd@`                                  |
| 3rd              | `3@`, `3rd@`                                  |
| 4th              | `4@`, `4th@`                                  |
| 15th             | `15@`, `15th@`                                |
| 31st             | `31@`, `31st@`                                |
| **Other Day**    |                                               |
| Every Day        | `day@`                                        |
| Every Weekday    | `weekday@`                                    |
| End of Month     | `eom@`                                        |
