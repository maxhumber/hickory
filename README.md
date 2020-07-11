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

| Operating System | Support | Scheduler                                        |
| ---------------- | ------- | ------------------------------------------------ |
| macOS            | ✅       | [launchd](https://en.wikipedia.org/wiki/Launchd) |
| Linux            | ❌       |                                                  |
| Windows          | ❌       |                                                  |



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



### `--every=` Input

Schedule arguments lookup table:

| <u>Interval</u>         |                                             |
| ----------------------- | ------------------------------------------- |
| 10 seconds              | `10`, `10s`, `10sec`, `10secs`, `10seconds` |
| 10 minutes              | `10m`, `10min`, `10mins`, `10minutes`       |
| 10 hours                | `10h`, `10hr`, `10hrs`, `10hours`           |
| <u>**Time**</u>         |                                             |
| 10:00 AM                | `@10`, `@10am`                              |
| 10:00 PM                | `@22`, `@10pm`                              |
| 10:10 AM                | `@10:10`, `@10:10am`                        |
| 10:10 PM                | `@22:10`, `@10:10pm`                        |
| <u>**Weekday**</u>      |                                             |
| Monday                  | `m@`, `mon@`, `monday@`                     |
| Tuesday                 | `t@`, `tue@`, `tues@`, `tuesday@`           |
| Wednesday               | `w@`, `wed@`, `weds@`, `wednesday@`         |
| Thursday                | `th@`, `thur@`, `thurs@`, `thursday@`       |
| Friday                  | `f@`, `fri@`, `friday@`                     |
| Saturday                | `s@`, `sat@`, `saturday@`                   |
| Sunday                  | `su@`, `sun@`, `sunday@`                    |
| <u>**Calendar Day**</u> |                                             |
| 1st                     | `1@`, `1st@`                                |
| 2nd                     | `2@`, `2nd@`                                |
| 3rd                     | `3@`, `3rd@`                                |
| 4th                     | `4@`, `4th@`                                |
| 15th                    | `15@`, `15th@`                              |
| 31st                    | `31@`, `31st@`                              |
| <u>**Other Day**</u>    |                                             |
| Every Day               | `day@`                                      |
| Every Weekday           | `weekday@`                                  |
| End of Month            | `eom@`                                      |



Multiples:

| Input                    |
| ------------------------ |
| `--every=@9:30am,4:30pm` |
| `--every=15,eom@10:10`   |
| `--every=m,w,f@2pm,4pm`  |
