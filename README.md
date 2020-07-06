### hickory

<h3 align="center">
  <img src="https://raw.githubusercontent.com/maxhumber/hickory/master/logo/hickory.png" width="300px" alt="hickory">
</h3>
<p align="center">
  <a href="https://github.com/maxhumber/hickory"><img alt="GitHub" src="https://img.shields.io/github/license/maxhumber/hickory"></a>
  <a href="https://travis-ci.org/maxhumber/hickory"><img alt="Travis" src="https://img.shields.io/travis/maxhumber/hickory.svg"></a>
  <a href="https://pypi.python.org/pypi/hickory"><img alt="PyPI" src="https://img.shields.io/pypi/v/hickory.svg"></a>
  <a href="https://pepy.tech/project/hickory"><img alt="Downloads" src="https://pepy.tech/badge/hickory"></a>
</p>


🕰 Hickory, dickory, dock. The snake ran up the clock.

Scheduling sucks. Or well, it did. Now it doesn't.

You get 3 commands. That's it. No restarting or pausing. Severely limited. But those limitations are clarifying. And well work for 98% of all cases

Just supports macos right now

### ⚠️ HEAVILY UNDER DEVELOPMENT ⚠️

**Current API** ... will definitely change



#### Schedule:

`hickory schedule tryme.py`

`hickory schedule tryme.py --interval=10 --run_at_load=True`

TODO: calendar interval, finalize command (start? load? run?)


#### To see all running scripts:

`hickory list`

TODO: would be nice to see number of times triggered, when it was started, uptime, if it's still running, id?, script path? maybe use rich...

See repeat rule?


#### To stop/kill/and delete:

`hickory kill tryme.py`


#### install for now:

Clone and cd into this repo, the run...

`pip install -e .`
