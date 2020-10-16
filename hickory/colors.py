from typing import Tuple


class Color:

    codes: Tuple[int, ...]

    def __init__(self, *codes: int):
        self.codes = codes

    def __str__(self):
        return f'\033[{";".join(map(str, self.codes))}m'

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Color(*self.codes, *other.codes)
        return other + str(self)

    def __call__(self, i):
        return str(self) + i + '\033[0m'


class Fore:
    RED = Color(91)
    GREEN = Color(92)
    YELLOW = Color(93)
    BLUE = Color(94)
    MAGENTA = Color(95)
    CYAN = Color(96)
    RESET = Color(39)


class Back:
    RED = Color(101)
    GREEN = Color(102)
    YELLOW = Color(103)
    BLUE = Color(104)
    MAGENTA = Color(105)
    CYAN = Color(106)
    RESET = Color(49)


class Style:
    RESET = Color(22)
    BRIGHT = Color(1)


RESET_ALL = Color()


if __name__ == "__main__":
    # import sys
    # __module__ = sys.modules[__name__]
    # print('a' @ __module__.Y_BOLD)
    print(f'{Fore.RED}%s{Fore.RESET}')
    print(Fore.RED('a'))
