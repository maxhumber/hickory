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

`hickory` is a command line tool for scheduling Python scripts with [launchd](https://en.wikipedia.org/wiki/Launchd) on macOS 

Name and logo inspired by the [rhyme](https://en.wikipedia.org/wiki/Hickory_Dickory_Dock).



### Install

```sh
pip install hickory
```



### Usage

Schedule a script:

```sh
hickory schedule foo.py --every=10minutes
```

View running scripts:

```sh
hickory schedule info
```

Kill a running script:

```sh
hickory schedule kill foo.py
```

Note: 

`stdout` and `stderr` are sent to a `hickory.log` file in the same directory as the script.



### `every` Shorthand

**Interval**

> `--every=10mins` • repeat every 10 minutes

| Seconds     | Minutes     | Hours     |
| ----------- | ----------- | --------- |
| `10`        |             |           |
| `10s`       | `10m`       | `10h`     |
| `10sec`     | `10min`     | `10hr`    |
| `10secs`    | `10mins`    | `10hrs`   |
| `10seconds` | `10minutes` | `10hours` |

**Timestamp**

> `--every=@10:10am` • repeat every day at 10:00 AM

| Input      | Time     |
| ---------- | -------- |
| `@10`      | 10:00 AM |
| `@22`      | 10:00 PM |
| `@10:10`   | 10:10 AM |
| `@22:10`   | 10:10 PM |
| `@10am`    | 10:00 AM |
| `@10pm`    | 10:00 PM |
| `@10:10am` | 10:10 AM |
| `@10:10pm` | 10:10 PM |

**Weekday**

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

**Calendar Day**

> `--every=10th@10:10am` • repeat every 10th day of the month at 10:10 AM

| Day  | Input          |
| ---- | -------------- |
| 1st  | `1@`, `1st@`   |
| 2nd  | `2@`, `2nd@`   |
| 3rd  | `3@`, `3rd@`   |
| 4th  | `4@`, `4th@`   |
| 15th | `15@`, `15th@` |
| 31st | `31@`, `31st@` |

**Special? Day**

>  `--every=eom@10:10am` • repeat every last day of the month at 10:10 AM

| Day       | Input                   |
| ---------------- | --------------------------------- |
| Every Day      | `day@`                              |
| Every Weekday  | `weekday@`                          |
| End of Month   | `eom@`                              |

**Multiples**

| Input            |      |
| ---------------- | ---- |
| `@9:30am,4:30pm` |      |
| `15,eom@9:00`    |      |
| `m,w,f@2pm,4pm`  |      |
