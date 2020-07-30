info_dicts = [
    {
        "id": "427400",
        "file": "foo.py",
        "runs": "2826",
        "state": "waiting",
        "interval": 10,
    },
    {
        "id": "78ea00",
        "file": "longer_file_name.py",
        "runs": "2",
        "state": "running",
        "interval": "monday@8:30pm",
    },
]

spacer = 2
maxlens = find_maxlens(info_dicts)
keys = ["id", "file", "state", "runs", "interval"]
strings = build_strings(keys, info_dicts, maxlens, spacer)
terminal_string = build_terminal_string(keys, strings, maxlens, spacer)
print(terminal_string)
