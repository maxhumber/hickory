from typing import Dict, List, Union


def _find_maxlens(info_dicts: List[Dict[str, Union[str, int]]]) -> Dict[str, int]:
    keys = info_dicts[0].keys()
    maxlens = {key: len(key) for key in keys}
    for info in info_dicts:
        for key in keys:
            current = maxlens[key]
            new = len(str(info[key]))
            if current < new:
                maxlens[key] = new
    return maxlens


def _build_strings(
    keys: List[str],
    info_dicts: List[Dict[str, Union[str, int]]],
    maxlens: Dict[str, int],
    spacer: int = 2,
) -> List[str]:
    strings = []
    for info in info_dicts:
        string = ""
        for key in keys:
            value = info[key]
            string_part = str(value).ljust(maxlens[key])
            string += string_part + " " * spacer
        strings.append(string.strip())
    return strings


def _build_terminal_string(
    keys: List[str], strings: List[str], maxlens: Dict[str, int], spacer: int = 2
) -> str:
    terminal_string = ""
    for key in keys:
        string_part = key.ljust(maxlens[key])
        terminal_string += string_part + " " * spacer
    terminal_string = terminal_string.upper().strip() + "\n"
    terminal_string += "\n".join(strings)
    return terminal_string


def format_status(info_dicts: List[Dict[str, Union[str, int]]], spacer: int = 2) -> str:
    maxlens = _find_maxlens(info_dicts)
    keys = ["id", "file", "state", "runs", "interval"]
    strings = _build_strings(keys, info_dicts, maxlens, spacer)
    return _build_terminal_string(keys, strings, maxlens, spacer)
