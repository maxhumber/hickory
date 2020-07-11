<h3 align="center">
  <img src="https://raw.githubusercontent.com/maxhumber/hickory/master/logo/hickory.png" width="125px" alt="hickory">
</h3>
<p align="center">
  <a href="https://github.com/maxhumber/hickory"><img alt="GitHub" src="https://img.shields.io/github/license/maxhumber/hickory"></a>
  <a href="https://travis-ci.org/maxhumber/hickory"><img alt="Travis" src="https://img.shields.io/travis/maxhumber/hickory.svg"></a>
  <a href="https://pypi.python.org/pypi/hickory"><img alt="PyPI" src="https://img.shields.io/pypi/v/hickory.svg"></a>
  <a href="https://pepy.tech/project/hickory"><img alt="Downloads" src="https://pepy.tech/badge/hickory"></a>
</p>


### About

`hickory` is a command line tool for scheduling Python scripts. It is not a replacement for a Directed Acyclic Graph (DAG) workflow scheduler. But it is perfect for most *stand-alone* jobs!



### Support

`hickory` currently supports:

| Operating System | Support                                              |
| ---------------- | ---------------------------------------------------- |
| macOS            | ✅ • [launchd](https://en.wikipedia.org/wiki/Launchd) |
| Linux            | ❌                                                    |
| Windows          | ❌                                                    |



### Install

`hickory` is installed at the command line:

```sh
pip install hickory
```



### Quickstart

Create a python script called `foo.py`:

```python
# foo.py
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

Check the execution status of `foo.py`:

```sh
hickory status
```

Check the `stdout` and `stderr` logs for the `foo.py` script:

```
tail -f hickory.log
```

Kill (stop and delete) the schedule for `foo.py`:

```sh
hickory kill foo.py
```



### `--every=` Examples

English to schedule input:

| English                                                      |                          |
| ------------------------------------------------------------ | ------------------------ |
| Repeat every ten minutes                                     | `--every=10minutes`      |
| Repeat every day at 10:10 AM                                 | `--every=@10:10`         |
| Repeat every Monday at 10:10 AM                              | `--every=monday@10:10am` |
| Repeat every 10th day of the month at 10:10 AM               | `--every=10th@10:10am`   |
| Repeat every last day of the month at 10:10 AM               | `--every=eom@10:10am`    |
| Repeat every 10th and last day of the month at 10 AM and 10 PM | `--every=10,eom@10,10pm` |



### `--every=` Table

Schedule arguments:

| Interval         |                                             |
| ---------------- | ------------------------------------------- |
| 10 seconds       | `10`, `10s`, `10sec`, `10secs`, `10seconds` |
| 10 minutes       | `10m`, `10min`, `10mins`, `10minutes`       |
| 10 hours         | `10h`, `10hr`, `10hrs`, `10hours`           |
| **Time**         |                                             |
| 10:00 AM         | `@10`, `@10am`                              |
| 10:00 PM         | `@22`, `@10pm`                              |
| 10:10 AM         | `@10:10`, `@10:10am`                        |
| 10:10 PM         | `@22:10`, `@10:10pm`                        |
| **Weekday**      |                                             |
| Monday           | `m@`, `mon@`, `monday@`                     |
| Tuesday          | `t@`, `tue@`, `tues@`, `tuesday@`           |
| Wednesday        | `w@`, `wed@`, `weds@`, `wednesday@`         |
| Thursday         | `th@`, `thur@`, `thurs@`, `thursday@`       |
| Friday           | `f@`, `fri@`, `friday@`                     |
| Saturday         | `s@`, `sat@`, `saturday@`                   |
| Sunday           | `su@`, `sun@`, `sunday@`                    |
| **Calendar Day** |                                             |
| 1st              | `1@`, `1st@`                                |
| 2nd              | `2@`, `2nd@`                                |
| 3rd              | `3@`, `3rd@`                                |
| 4th              | `4@`, `4th@`                                |
| 15th             | `15@`, `15th@`                              |
| 31st             | `31@`, `31st@`                              |
| **Other Day**    |                                             |
| Every Day        | `day@`                                      |
| Every Weekday    | `weekday@`                                  |
| End of Month     | `eom@`                                      |
