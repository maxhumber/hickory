def _find_maxlens(info_dicts):
    keys = info_dicts[0].keys()
    maxlens = {key: len(key) for key in keys}
    for info in info_dicts:
        for key in keys:
            current = maxlens[key]
            new = len(str(info[key]))
            if current < new:
                maxlens[key] = new
    return maxlens


def _build_strings(keys, info_dicts, maxlens, spacer=2):
    strings = []
    for info in info_dicts:
        string = ""
        for key in keys:
            value = info[key]
            string_part = str(value).ljust(maxlens[key])
            string += string_part + " " * spacer
        strings.append(string.strip())
    return strings


def _build_terminal_string(keys, strings, maxlens, spacer=2):
    terminal_string = ""
    for key in keys:
        string_part = key.ljust(maxlens[key])
        terminal_string += string_part + " " * spacer
    terminal_string = terminal_string.upper().strip() + "\n"
    terminal_string += "\n".join(strings)
    return terminal_string


def format_status(info_dicts, spacer=2):
    maxlens = _find_maxlens(info_dicts)
    keys = ["id", "file", "state", "runs", "interval"]
    strings = _build_strings(keys, info_dicts, maxlens, spacer)
    return _build_terminal_string(keys, strings, maxlens, spacer)
