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



Interval:

> `--every=10mins` • repeat every 10 minutes

| Seconds     | Minutes     | Hours     |
| ----------- | ----------- | --------- |
| `10`        |             |           |
| `10s`       | `10m`       | `10h`     |
| `10sec`     | `10min`     | `10hr`    |
| `10secs`    | `10mins`    | `10hrs`   |
| `10seconds` | `10minutes` | `10hours` |



Timestamp:

> `--every=@10:10am` • repeat every day at 10:10 AM

| Input      | Time     |
| ---------- | -------- |
| `@10`      | 10:00 AM |
| `@22`      | 10:00 PM |
| `@10am`    | 10:00 AM |
| `@10pm`    | 10:00 PM |
| `@10:10`   | 10:10 AM |
| `@22:10`   | 10:10 PM |
| `@10:10am` | 10:10 AM |
| `@10:10pm` | 10:10 PM |



Weekday:

> `--every=monday@10:10am` • repeat every Monday at 10:10 AM

| Day       | Input    |
| ---------------- | --------------------------------- |
| Monday           | `m@`, `mon@`, `monday@`           |
| Tuesday          | `t@`, `tue@`, `tues@`, `tuesday@` |
| Wednesday        | `w@`, `wed@`, `weds@`, `wednesday@`       |
| Thursday         | `th@`, `thur@`, `thurs@`, `thursday@`     |
| Friday           | `f@`, `fri@`, `friday@`                 |
| Saturday         | `s@`, `sat@`, `saturday@`               |
| Sunday           | `su@`, `sun@`, `sunday@`               |



Calendar Day:

> `--every=10th@10:10am` • repeat every 10th day of the month at 10:10 AM

| Day  | Input          |
| ---- | -------------- |
| 1st  | `1@`, `1st@`   |
| 2nd  | `2@`, `2nd@`   |
| 3rd  | `3@`, `3rd@`   |
| 4th  | `4@`, `4th@`   |
| 15th | `15@`, `15th@` |
| 31st | `31@`, `31st@` |



Other Days:

>  `--every=eom@10:10am` • repeat every last day of the month at 10:10 AM

| Day       | Input                   |
| ---------------- | --------------------------------- |
| Every Day      | `day@`                              |
| Every Weekday  | `weekday@`                          |
| End of Month   | `eom@`                              |



Multiples:

> `--every=15,eom@9:00` • repeat every 15th and last day of the month at 10:10 AM

| Input                         |
| ----------------------------- |
| `@9:30am,4:30pm`              |
| `15,eom@10:10`                |
| `m,w,f@2pm,4pm`               |
| `<d1>,...,<dN>@<t1>,...,<tN>` |

